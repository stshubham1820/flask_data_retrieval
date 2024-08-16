from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from celery import Celery
from celery.schedules import crontab

db = SQLAlchemy()
redis_client = Redis(host='redis', port=6379)

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    app.config.update(
        CELERY_BROKER_URL='redis://redis:6379/0',
        CELERY_RESULT_BACKEND='redis://redis:6379/0',
        SQLALCHEMY_DATABASE_URI='sqlite:///data.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CELERYBEAT_SCHEDULE={
            'fetch-every-hour': {
                'task': 'tasks.fetch_and_store_data',
                'schedule': crontab(minute=0, hour='*'),  # Run every hour
            },
        }
    )

    db.init_app(app)
    celery = make_celery(app)

    return app, celery
app, celery = create_app()