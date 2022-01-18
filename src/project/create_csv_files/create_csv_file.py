import csv


a = ['name', 9, 6, 3]

with open("media/fake_data.csv", "w") as fd:
    writer = csv.writer(fd)
    writer.writerow(a)
