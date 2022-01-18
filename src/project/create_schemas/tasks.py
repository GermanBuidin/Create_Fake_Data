from celery import shared_task
from proj.utils import collection



@shared_task
def get_number(x, y):
    collection.insert_one({"_id": x, "name": y})
