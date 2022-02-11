from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'start_date' : datetime( 2022, 2, 9, 23, 30, 00 ) ,
    'owner' : 'hsshin', 
}

with DAG( dag_id = 'naver-news-crawler', 
          default_args = default_args,
          tags = ['news-crawler'],
          schedule_interval = timedelta(days=1)
          ) as dag :

        crawler_path = "/home/hsshin/scrap_result"
        t1 = BashOperator ( 
         task_id = 'news_crawler1', 
         bash_command = 'python3 /home/hsshin/airflow/dags/NewsCrawler/newscrawler.py ' + crawler_path
        )

        t2 = BashOperator ( 
         task_id = 'news_crawler2', 
         bash_command = 'python3 /home/hsshin/airflow/dags/NewsCrawler/newscrawler.py ' + crawler_path 
        )

        conv_respath = "/home/hsshin/tmp"
        conv_filename = "conv_res.tmp"
    
        # "D:/01.Develop/02.PYTHON/05.NewsCrawler/tmp",
        # "hello.parquet"
        t3 = SparkSubmitOperator(
            application = "/home/hsshin/airflow/dags/NewsStatistics/converter.py",
            task_id = "spark_news_conv",
            conn_id = "spark_default", 
            application_args = [crawler_path, "csv", conv_respath, conv_filename]
        )

        bucket_name = "recommand.news.hsshin"
        file_format = "parquet"
        t4 = BashOperator (
            task_id = "s3_loader",
            bash_command = f'python3 /home/hsshin/airflow/dags/NewsStatistics/s3_loader.py {bucket_name} {conv_respath + "/" + conv_filename} {file_format}'
        )

        t5 = BashOperator(
            task_id = "result_path_clear",
            bash_command = f"rm {crawler_path}/*"
        )

        [t1, t2] >> t3
        t3 >> t4
        t4 >> t5
