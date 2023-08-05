from pprint import pprint
import boto3, base64, json

class Lambda:
    '''
      for invoking lambda functions
    '''
    def __init__(self, user=None, pw=None, region = 'ap-southeast-1'):
      self.lambdaClient = boto3.client(
          'lambda',
          aws_access_key_id=user,
          aws_secret_access_key=pw,
          region_name = region
        )
    def invoke(self, functionName, input):
      result = self.lambdaClient.invoke(
        FunctionName = functionName,
        InvocationType= 'RequestResponse',
        LogType='Tail',
        ClientContext= base64.b64encode(json.dumps({'caller': 'sdk'}).encode()).decode(),
        Payload= json.dumps(input)
      )
      if 'Payload' in result.keys():
          return json.loads(result['Payload'].read())
      else:
          return result
