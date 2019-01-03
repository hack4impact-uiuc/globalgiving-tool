import mongomock

from globalgiving.commands.cmd_fillids import dev_fillids


def test_fill_no_unregistered_ngos():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    objects = [
        dict(name="ngo1", registration=["reg1"], country="Australia"),
        dict(name="ngo2", registration=["reg2"], country="Australia"),
    ]
    mock_collection.insert_many(objects)
    assert mock_collection.count_documents({}) == 2

    # Test fill ids (should not change state of db)
    dev_fillids(mock_collection)
    assert mock_collection.count_documents({}) == 2
    
    cursor = mock_collection.find({})
    ngos = [doc for doc in cursor]
    assert len(ngos[0]['registration']) == 1
    assert ngos[0]['registration'][0] == "reg1"
    assert len(ngos[1]['registration']) == 1
    assert ngos[1]['registration'][0] == "reg2"


def test_fill_mixed_registered_ngos():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    objects = [
        dict(name="ngo1", registration=None, country="Australia"),
        dict(name="ngo2", registration=["reg2"], country="Australia"),
    ]
    mock_collection.insert_many(objects)
    assert mock_collection.count_documents({}) == 2

    # Test fill ids (should not change state of db)
    dev_fillids(mock_collection)
    assert mock_collection.count_documents({}) == 2
    
    cursor = mock_collection.find({})
    ngos = [doc for doc in cursor]
    # First entry will be deleted and then updated version will be inserted
    # So the tests will flip the order of assertions
    assert len(ngos[0]['registration']) == 1
    assert ngos[0]['registration'][0] == "reg2"
    assert len(ngos[1]['registration']) == 1
    assert ngos[1]['registration'][0] != ""


def test_fill_no_registration_site():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    objects = [
        dict(name="ngo1", registration=None, country="Vietnam"),
        dict(name="ngo2", registration=["reg2"], country="Australia"),
    ]
    mock_collection.insert_many(objects)
    assert mock_collection.count_documents({}) == 2

    # Test fill ids (should not change state of db)
    # Currently Vietnam does not have any listed registration office sites
    # If this test fails, then the site has likely changed.
    dev_fillids(mock_collection)
    assert mock_collection.count_documents({}) == 2
    
    cursor = mock_collection.find({})
    ngos = [doc for doc in cursor]
    assert ngos[0]['registration'] is None
    assert len(ngos[1]['registration']) == 1
    assert ngos[1]['registration'][0] == "reg2"