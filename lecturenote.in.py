from bs4 import BeautifulSoup
import requests
import re
import os

print("Enter the URL of the note you want to download: ")
url = input()

site = requests.get(url)
soup = BeautifulSoup(site.content,'lxml')

aTag = soup.select_one("#left")
UnStrippedlink = aTag['href']
link = UnStrippedlink.strip('0')

totalPagesDiv = soup.find('div','book_buttom')
totalPagesSpan = [span for span in totalPagesDiv.findAll('span')]
totalPages = int(totalPagesSpan[2].text.strip(' / ')) + 1

#for i in range(1,totalPages):
siteA = requests.get("https://lecturenotes.in" + link + str(1))
soupA = BeautifulSoup(siteA.content,'lxml')

a = soupA.select_one("#pic" + str(1))

pic = a['style']
pic = pic.strip("background-image: url( ); background-size:cover;")
pic = re.sub("\).*?px","",pic)

pageLinks = "https://lecturenotes.in" + pic

print("Enter the name of the PDF file")
dirName = input()

if not os.path.exists('my_folder'):
	os.makedirs(dirName)




