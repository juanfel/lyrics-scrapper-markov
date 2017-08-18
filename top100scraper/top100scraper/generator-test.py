import top100scraper.generator as generator
def setup_module():
    print("Setup")
    global lyric_gen, title_gen
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
    lyric_gen.get_lyrics_from_db(limit=100, tags="Metal")
    assert len(lyric_gen.text_data) == 100
def get_generated_sentence_test():
    lyric_gen.text_data = []
    lyric_gen.markovify_songs(limit=100, text_type = generator.markovify.NewlineText)
    sentence = lyric_gen.get_generated_sentence()
    print(sentence)
    assert sentence != None

def title_fetching_test():
    title_gen = generator.TitleGenerator()
    title_gen.get_titles_from_db(limit=100);
    print(title_gen.text_data[1:10])
    assert len(title_gen.text_data) == 100

def title_generator_test():
    title_gen = generator.TitleGenerator()
    title_gen.markovify_songs(limit=100, text_type=generator.markovify.NewlineText,states=1)
    sentence = title_gen.get_generated_sentence()
    print("titulo:" + sentence)
    assert sentence != None
def song_generator_test():
    song_gen = generator.SongGenerator(lyric_limit = 100, title_limit = 100)
    assert song_gen != None

    title, sentences = song_gen.generate_song(sentence_number = 4)
    assert isinstance(title, str)
    assert isinstance(sentences, list)

    print("titulo:" + title)
    for sentence in sentences:
        print(sentence )
