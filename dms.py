"""
dms means 'dormitory management system'. This file (dms.py) is the main script of this project.
"""
import os
from app import create_app, db
from flask_migrate import Migrate

from app.models import Role, User, Student, DormBuilding, Guest, DAdmin, Tools, Repair, Lost

app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # FLASK_CONFIG is a environment variable that should be configured. For details, those can be found in the dictionary config in the file config.py
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    When using the flask shell command, there is no needs to import db, User, Role...anymore.
    """
    return dict(db=db,
                Tools=Tools,
                User=User,
                Role=Role,
                Student=Student,
                DormBuilding=DormBuilding,
                Guest=Guest,
                DAdmin=DAdmin,
                Repair=Repair,
                Lost=Lost)


@app.cli.command()
def test():
    """
    This is for running the test by using 'flask test' in the terminal
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

