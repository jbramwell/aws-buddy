import boto3
import os


class Account:
    _profile_name = ''
    _session = None
    _user_groups_cache = None

    def __init__(self, profile_name, region_name):
        self._user_groups_cache = {}
        self.profile_name = profile_name

        if (self.profile_name is None):
            # Get credentials from env config settings
            self._region_name = region_name

            self.session = boto3.session.Session(
                region_name=self._region_name,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
        else:
            # Use the pre-defined AWS connection settings
            self._region_name = region_name
            self.session = boto3.session.Session(profile_name=profile_name,
                                                 region_name=self._region_name)

        sts = self.session.client("sts")
        self._account_id = sts.get_caller_identity()["Account"]

    @property
    def profile_name(self):
        return self._profile_name

    @profile_name.setter
    def profile_name(self, value):
        self._profile_name = value

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value

    @property
    def account_id(self):
        return self._account_id

    @property
    def region_name(self):
        return self._region_name