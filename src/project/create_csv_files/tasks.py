from celery import shared_task
from .create_file import create_files


@shared_task
def start_create_files(user_id, rows):
    create_files(user_id, rows)
