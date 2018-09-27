#!/usr/bin/python
import boto3
import json
import sys

def get_code():
    return_value = raw_input("enter security token: ")
    return return_value
    
def get_creds(mfaCode):
    client = boto3.client('sts')    

if __name__ == "__main__":
    mfa_code = get_code()
    get_creds(mfa_code)
   
