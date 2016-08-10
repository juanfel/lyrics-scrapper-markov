from flask import Flask, render_template, url_for
from generator import SongGenerator

def app_generator(lyric_limit, title_limit):

    app = Flask(__name__)

    song_gen = SongGenerator(lyric_limit = int(lyric_limit), title_limit = int(title_limit))

    @app.route('/')
    def print_song_page():
        title, sentences = song_gen.generate_song()
        return render_template("song.html", title = title.capitalize(), sentences = sentences)
    return app 
