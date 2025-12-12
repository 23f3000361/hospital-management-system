from celery import Celery, Task

# 1. Create the global instance
celery = Celery("HMS_App")

def celery_init_app(app):
    # 2. Define a Task class that wraps execution in the Flask App Context
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    # 3. Update the global instance with config from Flask
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone=app.config["CELERY_TIMEZONE"],
        beat_schedule=app.config["CELERY_BEAT_SCHEDULE"]
    )
    
    celery.Task = FlaskTask
    app.extensions["celery"] = celery
    
    return celery