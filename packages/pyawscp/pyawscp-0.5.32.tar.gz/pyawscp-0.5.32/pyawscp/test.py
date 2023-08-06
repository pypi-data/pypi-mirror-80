def main():
    AWS_CREDENTIALS_DIR = "~/.aws/"
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
    print("")
    print("")

if __name__ == '__main__':
    main()    
    