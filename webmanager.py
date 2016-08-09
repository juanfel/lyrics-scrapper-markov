from flask_script import Manager, Server
from webpage import app_generator

manager = Manager(app_generator)

manager.add_option("-l", "--lyric-limit", dest="lyric_limit", default = 0)
manager.add_option("-t", "--title-limit", dest="title_limit", default = 0)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

if __name__ == "__main__":
    manager.run()
