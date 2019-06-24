from bs4 import BeautifulSoup
import img2pdf 
from PIL import Image 
import requests
import re
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

imagenames = []
print(bcolors.BOLD + "Enter the URL of the note you want to download: ")
url = input()

site = requests.get(url)
soup = BeautifulSoup(site.content,'lxml')

aTag = soup.select_one("#left")
UnStrippedlink = aTag['href']
link = UnStrippedlink.strip('0')

totalPagesDiv = soup.find('div','book_buttom')
totalPagesSpan = [span for span in totalPagesDiv.findAll('span')]
totalPages = int(totalPagesSpan[2].text.strip(' / ')) + 1

print(bcolors.BOLD + "Enter the name of the PDF file")
dirName = input()

#Creating Directories
if not os.path.exists(dirName):
	os.makedirs(dirName + '/Images')
	os.makedirs(dirName + '/PDF')

print(bcolors.OKBLUE + "[+] Total Number of Pages are " + str(totalPages-1))
for i in range(1,totalPages):
	siteA = requests.get("https://lecturenotes.in" + link + str(i))
	soupA = BeautifulSoup(siteA.content,'lxml')

	a = soupA.select_one("#pic" + str(i))

	pic = a['style']
	pic = pic.strip("background-image: url( ); background-size:cover;")
	pic = re.sub("\).*?px","",pic)
	pageLinks = "https://lecturenotes.in" + pic 
	print(bcolors.OKGREEN + "[+] Page " + str(i) + " added to PDF")

	#Downloading Images
	r = requests.get(pageLinks)
	with open(dirName + '/Images/' + str(i) + '.jpeg', 'wb') as f:
		f.write(r.content)
		f.close()
	imagenames.append(dirName + '/Images/' + str(i) + '.jpeg')


#Converting Image to PDF
with open(dirName + '/PDF/' + dirName + ".pdf","wb") as f:
	f.write(img2pdf.convert(imagenames))
	f.close

print(bcolors.BOLD + "Sucessfully Downloaded PDF")
