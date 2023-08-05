import logging

from avatar_utils.sso_helper import SSOHelper
from avatar_utils.tests.UnitTest import UnitTest

logger = logging.getLogger(__name__)

sso = SSOHelper(client_id='client_id')


class BaseUnitTest(UnitTest):
    from app import create_app, db

    app = create_app('testing')
    client = app.test_client()
    db = db

    sso_id = 'test'
    sso_access_token = None

    def setUp(self):
        super().setUp()

        self.sso_access_token = sso.make_token(sso_user_id=self.sso_id)

        auth_header = {'Authorization': f'Bearer {self.sso_access_token}'}
        self.headers = {**self.headers, **auth_header}
