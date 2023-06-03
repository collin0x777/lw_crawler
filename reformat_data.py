import csv
import datetime

input_data_file = "posts_unformatted.csv"
output_data_file = "posts_formatted.csv"

def read_data():
    with open(input_data_file, "r") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            date_elements = row["date"].split(" ")
            date_elements[0] = date_elements[0][:-2]
            row["date"] = datetime.datetime.strptime(" ".join(date_elements), "%d %b %Y")
            row["title"] = row["title"].replace("\n", " ")
            row["comments"] = 0 if row["comments"]=="No" else row["comments"]
            data.append(row)

        data.sort(key=lambda x: x["date"])

        return data
    
def write_data(data):
    fieldnames = data[0].keys()

    for row in data:
        row["date"] = row["date"].strftime("%Y-%m-%d")

    with open(output_data_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

write_data(read_data())