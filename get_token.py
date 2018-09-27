#!/usr/bin/python
import boto3
import ConfigParser

def get_creds(mfaCode):
    config = ConfigParser.SafeConfigParser()
    config.read('account.cfg')
    configDict = dict(config.items('default'))
    client = boto3.client('sts')    
    response = client.assume_role(
        RoleArn=configDict['rolearn'],
        RoleSessionName='ScriptGenreated',
        SerialNumber=configDict['serialnumber'],
        TokenCode=mfaCode
    )
    return response

def config_file_updater(responseDict):
    config = ConfigParser.SafeConfigParser()
    awsFile = "/home/motes/.aws/credentials"
    config.read(awsFile)
    try: 
        config.add_section('swithRoleRoot')
    except ConfigParser.DuplicateSectionError:
        pass
    except:
        raise
    config.set('swithRoleRoot', 'output', 'text')
    config.set('swithRoleRoot', 'region', 'us-east-2')
    config.set('swithRoleRoot', 'aws_access_key_id', responseDict['Credentials']['AccessKeyId'])
    config.set('swithRoleRoot', 'aws_secret_access_key', responseDict['Credentials']['SecretAccessKey'])
    config.set('swithRoleRoot', 'aws_session_token', responseDict['Credentials']['SessionToken'])

    with open(awsFile, 'wb') as configfile:
        config.write(configfile)
  
if __name__ == "__main__":
    mfa_code = raw_input("enter security token: ")
    config_file_updater(get_creds(mfa_code))
   
