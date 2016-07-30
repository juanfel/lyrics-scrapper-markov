import db_manager
import json
from nose.tools import assert_equal

def setup_module():
    print("Setup")
    global test_db
    test_db = db_manager.LyricDatabase()
    test_db.connect()
    assert test_db is not None
def teardown():
    test_db.delete_collection()
    print("Done")
def database_connection_test():
    assert test_db.connected == True
def database_format_lyric_test():
    lyric = test_db.format_lyric("cantante", "titulo", "letra")
    print(lyric)
    assert_equal(json.dumps(lyric), json.dumps({"Cantante":"cantante", "Titulo":"titulo", "Letra":"letra"}))
def database_add_lyric_test():
    result = test_db.add_lyric("cantante", "titulo", "letra")
    print(result.inserted_id)
    
