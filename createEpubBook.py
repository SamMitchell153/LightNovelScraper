# Import libraries
import requests
import urllib.request
import time
import os.path
import re
from bs4 import BeautifulSoup
from tkinter import *

import ebooklib
from ebooklib import epub

def createEpub ():

    save_path = 'C:/Users/Sam/Desktop/LightNovelScraper'

    full_url = txtUrl.get()


    if 'wuxiaworld' in full_url:
        base_url = 'https://www.wuxiaworld.com/novel'
        print("supported website")
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

    #create book
    book = epub.EpubBook()



    #load preexisting book
    filePath = os.path.join(save_path + '/' + novel_name + '.epub')
    if os.path.exists(filePath):
        book = epub.read_epub(save_path + '/' + novel_name + '.epub')
        currentChapter = len(book.spine)
        strMessage.set = "Updating Epub"
    else:
        # set metadata
        book.set_identifier('id' + novel_name)
        book.set_title(novel_name)
        book.set_language('en')
        book.add_author('wuxiaworld')
        currentChapter = 1

        # init spine(chapter locations list)
        book.spine = ['nav']
        strMessage.set = "Creating Epub"

    response = requests.get(full_url)

    for x in range(6):
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.find(id='chapter-content')
            title = 'Chapter ' + str(currentChapter)
            newChapter = epub.EpubHtml(title=title, file_name='chap_' + str(currentChapter) + '.xhtml', lang='en')

            newChapter.content = str(text)
            # add chapter to book
            book.add_item(newChapter)
            # add chapter location in book
            book.spine.append(newChapter)
            # add chapter to TOC
            book.toc += (epub.Link(newChapter.file_name, newChapter.title, newChapter.title),
                    )

            currentChapter += 1

            url = base_url + '/' + novel_name + '/' + chapter_link + str(currentChapter)
            response = requests.get(url)

            time.sleep(1)

    # add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = 'BODY {color: white;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

    # add CSS file
    book.add_item(nav_css)

    # write to the file
    epub.write_epub(novel_name + '.epub', book, {})

    strMessage.set = "Epub created at: " + str(filePath)

    
#create window
window = Tk()
window.title('eBook Scraper')
window.geometry('500x500')
lblTitle = Label(window, text="Please enter full URL")
lblTitle.pack()
#create text field
txtUrl = Entry(window, width=50)
txtUrl.pack()
Button(window, text='Scrape', width=25, command = createEpub).pack()
strMessage = StringVar()
strMessage.set("")
Label(window, textvariable=strMessage).pack()
mainloop()
