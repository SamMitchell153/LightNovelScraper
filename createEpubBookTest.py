from ebooklib import epub

book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample book')
book.set_language('en')

book.add_author('Author Authorowski')
book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

# create chapter
x = 1
while x < 5:
    newChapter = epub.EpubHtml(title='Intro', file_name='chap_' + str(x) + '.xhtml', lang='hr')
    print(newChapter.file_name)
    newChapter.content='<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'

    # add chapter to book
    book.add_item(newChapter)
    # add chapter location in book
    book.spine.append(newChapter)
    # add chapter to TOC
    book.toc += (epub.Link(newChapter.file_name, newChapter.title, newChapter.title),
            )

    x +=1

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# write to the file
epub.write_epub('test.epub', book, {})