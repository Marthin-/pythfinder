from database import Database


def test_init():
    """ Basic and unnecessary. """
    db = Database()
    assert db.db is not None


def test_update():
    """ Test database updates. """

    db = Database(True)
    db.update_armors()
    db.update_weapons()

    # assert no throw
