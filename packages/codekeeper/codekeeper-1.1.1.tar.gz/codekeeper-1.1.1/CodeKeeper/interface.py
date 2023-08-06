import boto3
from botocore.exceptions import ClientError


class CodeKeeper:
    '''
    Interface for getting your saved code from AWS S3 straingt into the module - like import but for anything non-local
    Can be configured with .configure file containing your AWS credentials
    or by passing access_key_id and secret_access_id to constructor
    '''
    def __init__(self, access_key_id=None, secret_access_key=None):
        if access_key_id is None and secret_access_key is None:
            configuration_status = self._check_configuration()
            if configuration_status:
                self.credentials = (configuration_status[0], configuration_status[1])
            else:
                raise ValueError('Configuration has not been done succesfully! Configure your enviroment or init with credentials')
        else:
            self.credentials = (access_key_id, secret_access_key)

        self.client = boto3.client(
            's3',
            aws_access_key_id=self.credentials[0],
            aws_secret_access_key=self.credentials[1]
        )

    # Make a descriptor for credentials attribute
    #napisac testy

    def upload_file(self, file_name, bucket, object_name=None):
        '''Function uploads a file to S3 bucket of specified name'''
        if object_name is None:
            object_name = file_name

        try:
            response = self.client.upload_file(file_name, bucket, object_name)
        except ClientError as ex:
            print(ex)
            return False
        return response


    def get_file(self, file_name, bucket, scope):

        response = self.client.get_object(
            Bucket=bucket,
            Key=file_name
        )

        data = response.get('Body')
        new_func = compile(data.read(), 'AWS S3', mode='exec')
        exec(new_func, scope)
        return scope.get(file_name[:-3], 'Requested element not found')


    @classmethod
    def _check_configuration(cls):
        results = []

        with open('.configure', 'r') as file:
            for index, line in enumerate(file):
                results.append(cls._check_line(index, line))

        return results if all(results) else False


    @staticmethod
    def _check_line(index, line):
        matches = ('ID=', 'SECRET=')

        if matches[index] in line:
            formatted_line = line.strip('\n').split(matches[index])[1]
            return formatted_line
        else:
            return False



    @staticmethod
    def configure(access_key_id, secret_access_key):
        '''
        .configure file format has to be :
        ID=<your access_key_id>
        SECRET=<your secret_access_key>
        Just like .env file format
        '''
        if isinstance(access_key_id, str) and isinstance(secret_access_key,str):
            with open('.configure', 'w') as f:
                f.write(f'ID={access_key_id}\n')
                f.write(f'SECRET={secret_access_key}')
            print('Configuration was succesfull')
        else:
            raise ValueError('Wrong Credentials')
