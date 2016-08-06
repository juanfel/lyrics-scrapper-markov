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
    lyric_gen.text_data = []
    lyric_gen.markovify_songs(limit=100)
    sentence = lyric_gen.get_generated_sentence()
    print(sentence)
    assert sentence != None
def title_generator_test():
    title_gen = generator.TitleGenerator()
    title_gen.markovify_songs()

    sentence = title_gen.get_generated_sentence()
    print("titulo:" + sentence)
    assert sentence != None
    assert sentence != ""
