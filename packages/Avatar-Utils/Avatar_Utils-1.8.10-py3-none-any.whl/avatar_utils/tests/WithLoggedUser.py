from logging import getLogger

from avatar_utils.sso_helper import SSOHelper
from avatar_utils.tests.BaseUnitTest import BaseUnitTest

logger = getLogger(__name__)


class UnitTestWithLoggedUser(BaseUnitTest):
    # real SSO credentials
    username = None
    password = None

    sso_id = None
    sso_access_token = None
    # actual user id in the backend database
    avatar_user_id = None

    def setUp(self):
        super().setUp()

        self.__sso_helper = SSOHelper(client_id=self.app.config['SSO_CLIENT_ID'],
                                      client_secret=self.app.config['SSO_CLIENT_SECRET'],
                                      verify_token=True)

        logger.debug('Get real sso token')
        self.sso_access_token = self.__sso_helper.get_access_token(self.username, self.password)

        # add a token to headers
        auth_header = {'Authorization': f'Bearer {self.sso_access_token}'}
        self.headers = {**self.headers, **auth_header}
