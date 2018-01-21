import os
from flask_script import Manager

from app import create_app

CONFIG_NAME = os.environ.get('FLASK_CONFIG') or 'default'

app = create_app(CONFIG_NAME)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()


