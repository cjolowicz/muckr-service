import pytest

import muckr.extensions
import muckr.models


@pytest.mark.usefixtures('database')
class TestModels:
    def test_user(self):
        user = muckr.models.User(
            username='john',
            email='john@example.com',
            password_hash='xxxx')

        assert user.id is None
        assert user.username == 'john'
        assert user.email == 'john@example.com'
        assert user.password_hash == 'xxxx'

        muckr.extensions.database.session.add(user)
        muckr.extensions.database.session.commit()

        assert user.id == 1