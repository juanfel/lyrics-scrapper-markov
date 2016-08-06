import generator
def setup_module():
    print("Setup")
    global lyric_gen
    lyric_gen = generator.LyricsGenerator()
def preprocess_lyric_test():
    lyric = lyric_gen.preprocess_lyric("lyric\rlyric")
    print(lyric)
    assert lyric == "lyric\nlyric" 
