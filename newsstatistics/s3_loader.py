import logging
import boto3
import os
import sys
from datetime import datetime

from botocore.exceptions import ClientError


class NewsS3Loader:
    def __init__(self, bucket_name, infile_path: str, file_format: str, file_key: str):
        self.__infile_path = infile_path
        self.__s3_client = boto3.client("s3")
        self.__bucket_name = bucket_name
        self.__file_format = "." + file_format
        self.__file_key = file_key

        response = self.__s3_client.list_buckets()

        # if bucket dosen't exist, create new bucket.
        for bucket in response["Buckets"]:
            if bucket["Name"] == bucket_name:
                break
        else:
            self.__s3_client.create_bucket(Bucket=bucket_name)

        result = self.__s3_client.get_bucket_acl(Bucket=bucket_name)

    def exec(self):

        filelist = list()
        if True == os.path.isdir(self.__infile_path):
            child = os.listdir(self.__infile_path)
            for i in child:
                split_ext = os.path.splitext(i)
                if len(split_ext) > 1 and self.__file_format == split_ext[1]:
                    c_filepath = os.path.join(self.__infile_path, i)
                    filelist.append(c_filepath)
        else:
            filelist.append(self.__infile_path)

        for fpath in filelist:
            if False == self.__file_to_s3(fpath):
                return False

        return True

    def __file_to_s3(self, file_name):
        key = self.__file_key
        try:
            response = self.__s3_client.upload_file(file_name, self.__bucket_name, key)
        except ClientError as e:
            logging.error(e)
            return False
        return True


if __name__ == "__main__":
    if len(sys.argv) < 5:
        logging.error("parameter error.")
        exit(0)

    bucket_name = sys.argv[1]
    infile_path = sys.argv[2]
    file_format = sys.argv[3]
    key_value = sys.argv[4]

    t = NewsS3Loader(
        bucket_name=bucket_name,
        infile_path=infile_path,
        file_format=file_format,
        file_key=key_value,
    )
    t.exec()
