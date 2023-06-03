import csv
import datetime

data_file = "posts.csv"

def read_data():
    with open(data_file, "r") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            date_elements = row["date"].split(" ")
            date_elements[0] = date_elements[0][:-2]
            row["date"] = datetime.datetime.strptime(" ".join(date_elements), "%d %b %Y")
            data.append(row)

        data.sort(key=lambda x: x["date"])

        return data
    
def write_data(data):
    fieldnames = data[0].keys()

    for row in data:
        row["date"] = row["date"].strftime("%Y-%m-%d")

    with open(data_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

write_data(read_data())