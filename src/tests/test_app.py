import pytest


@pytest.mark.asyncio
async def test_print_db_name(db_session):
    print(db_session)
    pass
