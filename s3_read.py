import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_NAME = "lightning-dashboard-raw-files"

class s3_read:
    def __init__(self, store_directory, dataset_name, BASE_PATH):
        print("hello world---------------")
        self.filenames = []
        self.bucket = None
        self.bucket_files = None
        self.s3r = None
        self.dataset_name = dataset_name
        self.bucket_name = BUCKET_NAME
        self.BASE_PATH = BASE_PATH

        self.setup_boto()

    def setup_boto(self):
        print("setup_boto----------------")
        s3 = boto3.client('s3')
        s3_client = boto3.client('s3')

        self.s3r = boto3.resource('s3')
        self.bucket = self.s3r.Bucket(self.bucket_name)
        self.bucket_files = list(self.bucket.objects.all())
        print("after setup_boto--------------")

    def get_paths(self):
        for file in self.bucket_files:
            if(file.key[0:len(self.dataset_name)] == self.dataset_name and len(file.key) > len(self.dataset_name) + 2):
                self.filenames.append(self.BASE_PATH+file.key)
        return self.filenames