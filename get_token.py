#!/usr/bin/python
import boto3
import botocore
import ConfigParser

def get_creds(mfaCode):
    config = ConfigParser.SafeConfigParser()
    config.read('account.cfg')
    configDict = dict(config.items('default'))
    client = boto3.client('sts')    
    try:
        response = client.assume_role(
            RoleArn=configDict['rolearn'],
            RoleSessionName='ScriptGenreated',
            SerialNumber=configDict['serialnumber'],
            TokenCode=mfaCode
        )
    except botocore.exceptions.ClientError as errorMessage:
        if errorMessage.response['Error']['Code'] == 'InvalidClientTokenId':
            print errorMessage
            print "Is AWS_DEFAULT_PROFILE corret?"
            exit(100)
        else:
             raise
    except:
        raise
    return response

def config_file_updater(responseDict):
    config = ConfigParser.SafeConfigParser()
    sectionName = "get_token"
    awsFile = "/home/motes/.aws/credentials"
    config.read(awsFile)
    try: 
        config.add_section(sectionName)
    except ConfigParser.DuplicateSectionError:
        pass
    except:
        raise
    config.set(sectionName, 'output', 'text')
    config.set(sectionName, 'region', 'us-east-2')
    config.set(sectionName, 'aws_access_key_id', responseDict['Credentials']['AccessKeyId'])
    config.set(sectionName, 'aws_secret_access_key', responseDict['Credentials']['SecretAccessKey'])
    config.set(sectionName, 'aws_session_token', responseDict['Credentials']['SessionToken'])

    with open(awsFile, 'wb') as configfile:
        config.write(configfile)
    print "validate with: \n\taws --profile " + sectionName + " s3 ls"
  
if __name__ == "__main__":
    mfa_code = raw_input("enter security token: ")
    config_file_updater(get_creds(mfa_code))
   
