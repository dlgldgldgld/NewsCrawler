from h11 import Data
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import max, current_date, to_date
from pyspark.sql.utils import AnalysisException

import sys
import os
import logging


class Converter:
    def __init__(
        self,
        inputfile_path: str,
        inputfile_format: str,
        outfile_path: str,
        outfile_name: str = None,
    ):
        self.__spark = SparkSession.builder.getOrCreate()
        self.__input_file_path = inputfile_path
        self.__input_file_format = inputfile_format
        self.__output_file_path = outfile_path
        self.__output_file_name = outfile_name
        self.__origin_data_frame = None

    def __fileopen(self):
        filepath = self.__input_file_path
        file_format = self.__input_file_format

        if True == os.path.isdir(filepath):
            filepath = os.path.join(filepath, str("*." + file_format))

        try:
            self.__origin_data_frame = (
                self.__spark.read.format(file_format)
                .option("header", "true")
                .option("mode", "PERMISSIVE")
                .option("inferSchema", "true")
                .option("delimiter", "\t")
                .load(filepath)
            )
        except AnalysisException as e:
            logging.error(e)
            return False

        return True

    def __remove_duprecords(self):
        base_col = self.__origin_data_frame.drop("interest_cnt", "comm_cnt").distinct()
        group_inter_comm = self.__origin_data_frame.groupBy(["link"]).agg(
            max("interest_cnt").alias("interest_cnt"), max("comm_cnt").alias("comm_cnt")
        )
        res = base_col.join(group_inter_comm, "link", "inner").withColumn(
            "date", to_date(current_date(), "yyyy-MM-dd")
        )
        return res

    def __write_resultfile(self, out: DataFrame, fileformat: str = "parquet"):
        filepath = os.path.join(self.__output_file_path, self.__output_file_name)
        out.write.format(fileformat).mode("overwrite").save(filepath)
        return True

    def exec(self):
        if False == self.__fileopen():
            logging.error("[error] file open error")
            return False

        newsDF = self.__remove_duprecords()

        if False == self.__write_resultfile(out=newsDF):
            logging.error("[error] write result file.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        logging.error(
            "This program needs 4 input parameters. [1] = inputfile_path, [2] = inputfile_format [3] = outfile_path, [4] = outfile_name"
        )
        exit(0)

    inputfile_path = sys.argv[1]
    inputfile_format = sys.argv[2]
    outfile_path = sys.argv[3]
    outfile_name = sys.argv[4]

    t = Converter(
        inputfile_path=inputfile_path,
        inputfile_format=inputfile_format,
        outfile_path=outfile_path,
        outfile_name=outfile_name,
    )
    t.exec()
