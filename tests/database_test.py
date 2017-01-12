from database import Database


def test_init():
    """ Basic and unnecessary. """
    db = Database()
    assert db.db is not None
