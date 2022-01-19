import csv
from generation_fake_data.generators import generation_fake_data
from generation_fake_data.get_data import get_title


def create_file(name, separator=',', quot="'", number=10):
    with open(f'media/{name}.csv', 'w') as f:
        write = csv.writer(f, delimiter=separator, quoting=csv.QUOTE_ALL, quotechar=quot)
        data = generation_fake_data(number)
        title = get_title()
        write.writerow(title)
        for i in data.values():
            h = i.split(",")
            write.writerow(h)
    return None


file = create_file(name='screen', separator=';', quot='"', number=500)
