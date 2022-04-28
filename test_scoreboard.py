
from scoreboard import HighScore
from fakeredis import FakeRedis
from pytest import fixture


# This code creates a "fixture", which is a method that we can
# tell pytest to run before any tests
@fixture
def mock_db():
    return FakeRedis()


# Note that mock_db is a parameter.  This is the name of the fixture
# above.  pytest will execute the function and pass the return value
# of that function as the parameter.  This allows us to use that
# return value inside the test function.
def test_empty_db(mock_db):
    hs = HighScore(mock_db)
    assert hs.name is None
    assert hs.score == 0


def test_new_score_replaces_empty(mock_db):
    # Create the object
    hs = HighScore(mock_db)

    # Exercise the object
    hs.submit('Ben', 10)

    # Test the state of the object
    assert hs.name == 'Ben'
    assert hs.score == 10


def test_higher_score_replaces_old(mock_db):
    # configure the db and create the HighScore
    mock_db.set('name', 'Ben')
    mock_db.set('score', 10)
    hs = HighScore(mock_db)

    # Exercise the object
    hs.submit('Seth', 20)

    # Test the state of the object
    assert hs.name == 'Seth'
    assert hs.score == 20


def test_lower_score_does_not_replace_old(mock_db):
    # configure the db and create the HighScore
    mock_db.set('name', 'Seth')
    mock_db.set('score', 20)
    hs = HighScore(mock_db)

    # Exercise the object
    hs.submit('Ben', 10)

    # Test the state of the object
    assert hs.name == 'Seth'
    assert hs.score == 20


def test_tie_score_does_not_replace_old(mock_db):
    # configure the db and create the HighScore
    mock_db.set('name', 'Seth')
    mock_db.set('score', 20)
    hs = HighScore(mock_db)

    # Exercise the object
    hs.submit('Ben', 20)

    # Test the state of the object
    assert hs.name == 'Seth'
    assert hs.score == 20
