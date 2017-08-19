from flask import Flask, render_template, url_for
from generator import SongGenerator, POSNewlineText

def app_generator(lyric_limit = "16000", title_limit = "16000"):

    app = Flask(__name__)

    lyric_lim = int(lyric_limit)
    title_lim = int(title_limit)
    song_gen = SongGenerator(lyric_limit=lyric_lim,
                                title_limit=title_lim,
                                lyric_type=POSNewlineText,
                                title_type=POSNewlineText)

    @app.route('/')
    def print_song_page():
        title, sentences = song_gen.generate_song()
        return render_template("song.html", title = title.capitalize(), sentences = sentences)

    @app.route('/tags/<tag>')
    def print_tag_page(tag):
        """
        A diferencia de la version vanilla éste genera un generador nuevo por tag.
        Como los tags tienden a ser menos no hay problema de que tengan un limite grande.
        """
        tag_gen = SongGenerator(lyric_limit=lyric_lim,
                                title_limit=title_lim,
                                lyric_type=POSNewlineText,
                                title_type=POSNewlineText,
                                tags=tag)

        title, sentences = tag_gen.generate_song()
        return render_template("song.html", title = title.capitalize(), sentences = sentences)

    return app 
