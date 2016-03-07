import os
from flask_script import Manager, Shell, Server
from src.main import create_app, db

app = create_app()
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app and db by default.
    """
    return {'app': app, 'db': db}

manager.add_command('server', Server(port=os.environ.get('PORT', 9000)))
manager.add_command('shell', Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
