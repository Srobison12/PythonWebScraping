#read CSV
import csv


with open("output.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        uniqueRows = []
        seen = set()
        for row in reader:
                row_tuple = tuple(row)
                if row_tuple not in seen:
                        seen.add(row_tuple)
                        uniqueRows.append(row)
with open("cleanOutput.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(uniqueRows)
#remove duplicates

