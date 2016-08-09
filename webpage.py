from flask import Flask, render_template
from generator import SongGenerator
app = Flask(__name__)

song_gen = SongGenerator()

@app.route('/')
def print_song_page():
    title, sentences = song_gen.generate_song()
    return render_template("song.html", title = title, sentences = sentences)
