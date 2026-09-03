import sys
import re
import operator as op
import requests
from bs4 import BeautifulSoup
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

#touch each website, scrap the site for additional links
responseFromWebsite = requests.get(userWebsite)
htmlData = responseFromWebsite.text

#Write to that file any uniques we find in CSV formatting