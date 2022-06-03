from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from os import getenv

default_args = {
    "start_date": datetime(2022, 2, 9, 23, 30, 00),
    "owner": "hsshin",
}

with DAG(
    dag_id="naver-news-crawler",
    default_args=default_args,
    tags=["news-crawler"],
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    crawler_path = "/home/hsshin/scrap_result"
    t1 = BashOperator(
        task_id="news_crawler1",
        bash_command="python3 /home/hsshin/airflow/dags/NewsCrawler/newscrawler.py "
        + crawler_path,
    )

    t2 = BashOperator(
        task_id="news_crawler2",
        bash_command="python3 /home/hsshin/airflow/dags/NewsCrawler/newscrawler.py "
        + crawler_path,
    )

    conv_respath = "/home/hsshin/tmp"
    conv_filename = "conv_res.tmp"

    # "D:/01.Develop/02.PYTHON/05.NewsCrawler/tmp",
    # "hello.parquet"
    t3 = SparkSubmitOperator(
        application="/home/hsshin/airflow/dags/NewsStatistics/converter.py",
        task_id="spark_news_conv",
        conn_id="spark_default",
        application_args=[crawler_path, "csv", conv_respath, conv_filename],
    )

    bucket_name = "recommand.news.hsshin"
    file_format = "parquet"
    key_file_name = "news_scrap/" + datetime.today().strftime("%Y-%m-%d.") + file_format

    t4 = BashOperator(
        task_id="s3_loader",
        bash_command=f'python3 /home/hsshin/airflow/dags/NewsStatistics/s3_loader.py {bucket_name} {conv_respath + "/" + conv_filename} {file_format} {key_file_name}',
    )

    t5 = BashOperator(task_id="result_path_clear", bash_command=f"rm {crawler_path}/*")

    S3_BUCKET = getenv("S3_BUCKET", "recommand.news.hsshin")
    S3_KEY = getenv("S3_KEY", key_file_name)
    REDSHIFT_TABLE = getenv("REDSHIFT_TABLE", "newsitems")

    task_transfer_s3_to_redshift = S3ToRedshiftOperator(
        s3_bucket=S3_BUCKET,
        s3_key=S3_KEY,
        schema="PUBLIC",
        table=REDSHIFT_TABLE,
        copy_options=["parquet"],
        task_id="transfer_s3_to_redshift",
    )

    [t1, t2] >> t3
    t3 >> t4
    t4 >> t5
    t5 >> task_transfer_s3_to_redshift
