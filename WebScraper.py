import sys
import re
import time
import operator as op
import requests
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
    print(htmlData[:210])
    soup = BeautifulSoup(htmlData, "html.parser")
    allLinks = soup.find_all("a")
    for link in allLinks:
        print(link.get("href"))
        time.sleep(2)
#Write to that file any uniques we find in CSV formatting