import csv
import matplotlib.pyplot as plt
import datetime

data_file = "posts.csv"

def read_data():
    with open(data_file, "r") as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            row["author_karma"] = int(row["author_karma"])
            row["length"] = int(row["length"])
            row["date"] = datetime.datetime.strptime(row["date"], "%Y-%m-%d")
            row["comments"] = int(row["comments"])
            row["votes"] = int(row["votes"])
            row["score"] = int(row["score"])
            data.append(row)

        return data

def plot_average_over_time(data, field):
    buckets = {}
    for row in data:
        date = row["date"]
        value = int(row[field])
        if date not in buckets:
            buckets[date] = []
        buckets[date].append(value)

    averages = {date: (sum(values)/len(values)) for (date, values) in buckets.items()}

    plt.plot(averages.keys(), averages.values())
    plt.xlabel("Date")
    plt.ylabel(f"Average {field}")
    plt.show()

def plot_average_ratio_over_time(data, field1, field2):
    buckets = {}
    for row in data:
        date = row["date"]
        value1 = int(row[field1])
        value2 = int(row[field2])
        if date not in buckets:
            buckets[date] = []
        buckets[date].append(value1/value2)

    averages = {date: (sum(values)/len(values)) for (date, values) in buckets.items()}

    plt.plot(averages.keys(), averages.values())
    plt.xlabel("Date")
    plt.ylabel(f"Average {field1}/{field2}")
    plt.show()


data = read_data()
# plot_average_over_time(data, "length")
# plot_average_over_time(data, "comments")
# plot_average_over_time(data, "votes")
# plot_average_ratio_over_time(data, "comments", "votes")