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
#touch each website, scrape the site for additional links
session = requests.Session()
session.headers.update({
    "User-Agent": "Srobison12ETLCrawler/1.0"
})

toVisit = [userWebsite]
visitedSites = set()
maxDepth = 5



#print(htmlData[:210])
    



#Write to that file any uniques we find in CSV formatting
fileExists = os.path.exists("output.csv")
with open("output.csv", "a", newline="") as f:
    writer = csv.writer(f)
    if not fileExists:
        writer.writerow(["Site", "Link", "Status Code", "Respone Time"])

    while toVisit and len(visitedSites) < maxDepth:
        currentSite = toVisit.pop(0)
        if currentSite in visitedSites:
            continue
        print(f"Crawling: {currentSite}")
        visitedSites.add(currentSite)
        robots = RobotFileParser()
        robots.set_url(userWebsite.rstrip("/") + "/robots.txt")
        try:
            robots.read()

            if not robots.can_fetch("*", userWebsite):
                print("robots.txt does not allow this crawler.")
                exit()
        except Exception as e:
            print(f"Error reading robots.txt: {e}")
            continue
        try:
            startTime = time.perf_counter()
            responseFromWebsite = session.get(currentSite, timeout=5)
            endTime = time.perf_counter()
            responseTime = endTime - startTime
        except requests.RequestException as e:
            print(f"Error fetching {currentSite}: {e}")
            continue
        statusCode = responseFromWebsite.status_code
        if statusCode != requests.codes.ok:
            continue
        if "text/html" not in responseFromWebsite.headers.get("Content-Type", ""):
            continue
        htmlData = responseFromWebsite.text
        soup = BeautifulSoup(htmlData, "html.parser")
        allLinks = soup.find_all("a")
        
    for link in allLinks:
        href = link.get("href")
        #Converting url ends to join to the website entered
        if not href:
            continue
        href = urllib.parse.urljoin(userWebsite, href)
        href = urllib.parse.urldefrag(href)[0]  # Remove fragment
        parsedUrl = urllib.parse.urlparse(href)
        if parsedUrl.scheme not in ["http", "https"]:
            continue
        startingDomain = urllib.parse.urlparse(userWebsite).netloc

        linkDomain = parsedUrl.netloc
        if startingDomain != linkDomain:
            continue
        if href not in visitedSites and href not in toVisit:
            toVisit.append(href)
        responseFromWebsite = session.get(href, timeout=5) 
        
        writer.writerow([userWebsite, href, statusCode, responseTime])
        time.sleep(2)

print("Crawling complete. Check output.csv for results.")
print(f"Pages crawled: {len(visitedSites)}")   
    #check CSV file for duplicates, if any, remove them and rewrite the file
    #Better restructure would be to create an entirely new program that reads the file and cleans up data for the ETL