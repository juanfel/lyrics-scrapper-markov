import generator
def setup_module():
    print("Setup")
    global lyric_gen
    lyric_gen = generator.LyricsGenerator()
def preprocess_lyric_test():
    lyric = lyric_gen.preprocess_lyric("lyric\rlyric")
    print(lyric)
    assert lyric == "lyric\nlyric\n" 
def join_lyrics_test():
    lyric_gen.join_lyrics()
    assert lyric_gen.text == ""

    lyric_gen.text_data = ["lyrics\n","data"]
    lyric_gen.join_lyrics()
    print(lyric_gen.text)
    assert lyric_gen.text == "lyrics\ndata"
def get_lyrics_test():
    lyric_gen.text_data = []
    lyric_gen.get_lyrics_from_db(limit = 100)

    assert len(lyric_gen.text_data) == 100
def get_generated_sentence_test():
    lyric_gen.join_lyrics()
    lyric_gen.feed_lyrics_to_model()
    sentence = lyric_gen.get_generated_sentence()
    print(sentence)
    assert sentence != None
