import top100scraper.db_manager as db_manager
import json
from nose.tools import assert_equal

def setup_module():
    print("Setup")
    global test_db
    test_db = db_manager.LyricDatabase()
    test_db.connect()
    assert test_db is not None
def teardown():
    print("Done")
def database_connection_test():
    assert test_db.connected == True
def database_format_lyric_test():
    lyric = test_db.format_lyric("cantante", "titulo", "letra")
    print(lyric)
    assert_equal(json.dumps(lyric), json.dumps({"Cantante":"cantante", "Titulo":"titulo", "Letra":"letra"}))
def database_add_lyric_test():
    result = test_db.add_lyric("cantante", "titulo", "letra")
    print(result.upserted_id)
def database_get_lyric_test():
    result = test_db.get_lyric("cantante","titulo")
    print(result)
    assert(result == "letra")
def database_get_lyric_count_test():
    test_db.add_lyric("cantante2", "titulo2", "letra2")
    result = test_db.get_lyric_count()
    print(result)
    assert result > 1
def database_delete_lyric_test():
    test_db.delete_lyric("cantante","titulo")
    test_db.delete_lyric("cantante2","titulo2")
    
    result = test_db.get_lyric("cantante","titulo")
    result2 = test_db.get_lyric("cantante2", "titulo2")

    assert result != "letra"
    assert result2 != "letra2"
def database_get_iterator_test():
    cursor = test_db.get_lyric_iterator(limit = 10)

    assert cursor != None
    for song in cursor:
        print(song["Letra"])
