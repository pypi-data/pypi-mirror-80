import boto3
import os
from os.path import expanduser

class Config:

    def __init__(self):
        self.awsProfile               = ""
        self.awsRegion                = ""
        self.awsTags                  = {}
        self.command                  = ""
        self.commandArguments         = ""
        self.tableLineSeparator       = True
        self.interactive              = False
        self.printResults             = False
        self.uploadChunkSizeMultipart = 10
        self.uploadThresholdMultipart = 100

    def awsTagsToFilter(self):
        if self.awsTags and len(self.awsTags) > 0:
            return True
        return False

    def botoSession(self):
        if not self.awsProfile and not self.awsRegion:
           session = boto3.Session()
        elif not self.awsProfile and     self.awsRegion:    
           session = boto3.Session(region_name=self.awsRegion)
        elif     self.awsProfile and not self.awsRegion:   
           session = boto3.Session(profile_name=self.awsProfile)
        else:
           session = boto3.Session(profile_name=self.awsProfile,region_name=self.awsRegion) 
        return session

    def isThereAwsCredentials(self):
        AWS_CREDENTIALS_DIR  = expanduser("~") + "/.aws/"
        AWS_CREDENTIALS_FILE = AWS_CREDENTIALS_DIR + "credentials"
        if not os.path.exists(AWS_CREDENTIALS_DIR) or not os.path.exists(AWS_CREDENTIALS_FILE):
           print("") 
           print("")
           print("\033[31m ---> Ops!\033[33m AWS CREDENTIALS NOT FOUND!")
           print("") 
           print("") 
           print("\033[34m ---> \033[33mPlease, configure your AWS Credentials:")
           print("\033[34m      \033[33m1. Create the folder \033[35m{}\033[0m".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[33m2. Create the file \033[35m{}credentials\033[33m with the  content:".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[94m   [default]")
           print("\033[34m      \033[94m   aws_access_key_id = YOUR_ACCESS_KEY")
           print("\033[34m      \033[94m   aws_secret_access_key = YOUR_SECRET_KEY")
           print("\033[34m      \033[33m3. Optionally, create the file \033[35m{}config\033[33m with your default region:".format(AWS_CREDENTIALS_DIR))
           print("\033[34m      \033[94m   [default]")
           print("\033[34m      \033[94m   region=us-east-1")
           print("\033[0m")
           print("")
           return False
        return True


    

