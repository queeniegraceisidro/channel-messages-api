import pytest


def pytest_collection_modifyitems(items):

    # Mark integration and functional as okay to have db access
    for item in items:
        path = str(item.fspath)
        if "integration" or "functional" in path:
            item.add_marker(pytest.mark.django_db)
