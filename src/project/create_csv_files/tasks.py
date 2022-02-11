from celery import shared_task
from .create_csv_file import create_files


@shared_task
def start_create_files(rows):
    create_files(rows)
