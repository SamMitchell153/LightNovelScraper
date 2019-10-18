# Import libraries
import requests
import urllib.request
import time
import os.path
import re
from bs4 import BeautifulSoup

save_path = 'C:/Users/Sam/Desktop/LightNovelScraper'

full_url = input("Enter link to scrape from: ")


if 'wuxiaworld' in full_url:
    base_url = 'https://www.wuxiaworld.com/novel'
else:
    print("unsupported website")
    exit()

splitUrl = full_url.split('/')
novel_name = splitUrl[4]
chapter_link = re.findall("\D+", splitUrl[5])[0]
currentChapter = int(re.findall("\d+", splitUrl[5])[0])


directory = os.path.join(save_path + '/' + novel_name)
if not os.path.exists(directory):
    os.makedirs(directory)


response = requests.get(full_url)


if response.status_code == 200:
    while response.status_code == 200:
        filePath = os.path.join(save_path + '/' + novel_name + '/' + str(currentChapter) + '.html')
        if not os.path.exists(filePath):
            currentFile = open(filePath, "w+")
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.findAll(id='chapter-content')

            currentFile.write(str(text))

        url = base_url + '/' + novel_name + '/' + chapter_link + str(currentChapter)
        print(url)
        response = requests.get(url)
        currentChapter += 1
        time.sleep(1)


