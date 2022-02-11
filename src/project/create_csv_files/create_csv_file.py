import csv
from datetime import datetime
from bson import ObjectId

from generation_fake_data.generators import generator_fake_data
from proj import settings
from create_csv_files.for_views import list_cleaner
from proj.utils import collection


def create_files(rows):
    url = settings.MEDIA_ROOT
    data_set = list_cleaner()
    for data in data_set:
        data['datenow'] = datetime.now()
        data['processing'] = 'Processing'
        data['color'] = 'grey'
        collection.replace_one({"_id": ObjectId(data['_id'])}, data)
        with open(f'{url}/{data["name"]}.csv', 'w') as f:
            write = csv.writer(f, delimiter=data['separator'], quoting=csv.QUOTE_ALL, quotechar=data['quote'])
            generated_data = generator_fake_data(rows, data)
            title = [f'{i["ORDER"]}{i["title"]}' for i in data['schema']]
            write.writerow(title)
            for i in generated_data.values():
                row = i.split(",")
                write.writerow(row)
            data['link'] = f'{url}/{data["name"]}.csv'
            data['processing'] = 'Ready'
            data['color'] = 'lightgreen'
            collection.replace_one({"_id": ObjectId(data['_id'])}, data)
    return None
