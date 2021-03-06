"""Defines fixtures available to all tests."""
import pytest

import muckr_api.app
import muckr_api.extensions


def pytest_addoption(parser):
    parser.addoption(
        "--with-integration-tests",
        action="store_true",
        dest="integration_tests",
        default=False,
        help="enable integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "integration_test: mark integration test")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--with-integration-tests"):
        skip_integration_tests = pytest.mark.skip(
            reason="need --with-integration-tests option to run"
        )
        for item in items:
            if "integration_test" in item.keywords:
                item.add_marker(skip_integration_tests)


@pytest.fixture
def app():
    app = muckr_api.app.create_app("tests.config")
    context = app.test_request_context()
    context.push()  # type: ignore

    yield app

    context.pop()  # type: ignore


@pytest.fixture
def database(app):
    muckr_api.extensions.database.app = app
    with app.app_context():
        muckr_api.extensions.database.create_all()

    yield muckr_api.extensions.database

    muckr_api.extensions.database.session.close()
    muckr_api.extensions.database.drop_all()


@pytest.fixture
def client(app, database):
    return app.test_client()
