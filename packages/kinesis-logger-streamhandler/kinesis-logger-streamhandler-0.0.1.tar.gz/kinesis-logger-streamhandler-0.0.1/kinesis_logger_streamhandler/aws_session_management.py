import logging
from botocore.exceptions import ClientError
from os import environ
import boto3
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)


class AwsSessionManagement:
    """
    AWS Session Management - creates AWS Session with Temp AWS Credentials by assuming a role and calls an optional function
    """
    aws_access_key_id = None
    aws_secret_access_key = None
    aws_session_token = None
    aws_region = None
    session_expirationdate = None
    client = None


    def __init__(self, role_arn, external_id=None, func=None, role_session_name="RoleSession"):
        """
        Constructor
        :param role_arn: a role to assume
        :param external_id: optional externalId, if required by the trust relation ship
        :param func: a function to execute after received/renewed aws temp credentials
                     aws credentials are passed to the func
        """
        if self.client is None:
            self.client = boto3.client('sts', region_name=self.aws_region)
        self.role_arn = role_arn
        self.external_id = external_id
        self.func = func
        self.func_res = None
        self.role_session_name = role_session_name
        self.set_params()

    def set_params(self):
        if self.role_arn is None:
            logger.warning("Parameter 'role_arn' is not set! Will not assume role!")
        else:
            if (any([self.aws_access_key_id is None, self.aws_secret_access_key is None, self.aws_session_token is None,
                     self.session_expirationdate is None])) or all(
                    [self.session_expirationdate is not None, self.session_expirationdate < pytz.utc.localize(datetime.now())]):
                try:
                    logger.info(f"AssumingRole '{self.role_arn}' ...")
                    if self.external_id:
                        response = self.client.assume_role(
                            DurationSeconds=3600,
                            ExternalId=self.external_id,
                            RoleArn=self.role_arn,
                            RoleSessionName=self.role_session_name,
                        )
                    else:
                        response = self.client.assume_role(
                            DurationSeconds=3600,
                            RoleArn=self.role_arn,
                            RoleSessionName=self.role_session_name,
                        )
                    self.aws_access_key_id = response["Credentials"]["AccessKeyId"]
                    self.aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
                    self.aws_session_token = response["Credentials"]["SessionToken"]
                    self.session_expirationdate = response['Credentials']['Expiration']
                    logger.debug("Temp Credentials: ")
                    logger.debug(f"AccessKeyId     : {str(self.aws_access_key_id)}")
                    logger.debug(f"SecretAccessKey : {str(self.aws_secret_access_key)}")
                    logger.debug(f"SessionToken    : {str(self.aws_session_token)}")
                    logger.debug(f"Session Exp Date: {str(self.session_expirationdate)}")
                    logger.info(f"Successfully assumed role '{self.role_arn}', got credentials.")

                    if self.func:
                        # run the function after credentials renewal
                        logger.info("Executing function after aws credentials renewal")
                        self.func_res = self.func(self.aws_access_key_id, self.aws_secret_access_key, self.aws_session_token)
                        logger.info("Executed function")

                except Exception as e:
                    logger.error("Failed AssumingRole: " + e)
                    raise e

    def get_aws_credentials(self):
        self.set_params()
        return self.aws_access_key_id, self.aws_secret_access_key, self.aws_session_token

    def get_func_res(self):
        self.set_params()
        return self.func_res
