from . import models
from .views import app

# Connect sqlalchemy to app
models.db.init_app(app)


@app.cli.command()
def init_db():
    models.init_db()


@app.cli.command()
def populate_db():
    models.populate_db()
