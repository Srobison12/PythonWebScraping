import os
import sys
import re
import time
import operator as op
import requests
import csv
import urllib.parse
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
#Need to take in a valid website
print("Please enter in a starting website. Must be in http(s)://website.com format: \n")
#Need to create a CSV file
userWebsite = sys.stdin.readline().strip()
print(f"Website entered: , {userWebsite}")
#Validating
pattern = r"^https?://(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+(?:/.*)?$"
if not re.match(pattern, userWebsite): #If the website given doesn't match the expression, exit the program
    print("Wrong format... exiting...")
    exit()
#make sure we abide by the robots.txt....we don't need to get in trouble
robots = RobotFileParser()
robots.set_url(userWebsite.rstrip("/") + "/robots.txt")
robots.read()

if not robots.can_fetch("*", userWebsite):
    print("robots.txt does not allow this crawler.")
    exit()
#touch each website, scrap the site for additional links
responseFromWebsite = requests.get(userWebsite)
print(type(responseFromWebsite))
if responseFromWebsite.status_code == requests.codes.ok:
    htmlData = responseFromWebsite.text
    #print(htmlData[:210])
    soup = BeautifulSoup(htmlData, "html.parser")
    allLinks = soup.find_all("a")



#Write to that file any uniques we find in CSV formatting
    fileExists = os.path.exists("output.csv")
    with open("output.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not fileExists:
            writer.writerow(["site", "link"])
        for link in allLinks:
            href = link.get("href")
            #Converting url ends to join to the website entered
            if href:
                href = urllib.parse.urljoin(userWebsite, href)
                writer.writerow([userWebsite, href])

    
    #check CSV file for duplicates, if any, remove them and rewrite the file
    #Better restructure would be to create an entirely new program that reads the file and cleans up data for the ETL
    """with open("output.csv", "r") as f:
        reader = csv.reader(f)
        rows = list(reader)
        uniqueRows = []
        for row in rows:
            if row not in uniqueRows:
                uniqueRows.append(row)
    with open("output.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(uniqueRows)
else:
    print(f"Error: {responseFromWebsite.status_code} - {responseFromWebsite.reason}")"""