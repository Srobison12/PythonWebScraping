#read CSV
import csv

uniqueRows = []
seen = set()
with open("output.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
                if not row:
                       continue
                if row[0] == "Site":
                        uniqueRows.append(row)
                        continue
                link = row[1]
                if link not in seen:
                        seen.add(link)
                        uniqueRows.append(row)
with open("cleanOutput.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(uniqueRows)
#remove duplicates

