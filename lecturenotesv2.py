#!/usr/bin/env pythoni

import requests
import json
import os
import img2pdf

dirName = "test"
imagenames = []

def getURL(noteid):
	
	for i in range(1,1000):
		url = "https://lecturenotes.in/material/v2/" + str(noteid) + "/page-" + str(i) + "?noOfItems=1000"
		response = requests.get(url)

		#If 404 occurs end of Note reached
		if response.status_code == 404:
			return

		data = response.json()

		createDir()

		#This block of code gets path for the images
		for j in data["page"]:
			#Ignoring some prime feature hence some pages will not be available
			if j["upgradeToPrime"] == True:
				continue
			else:
				getImage(j["path"],dirName,j["pageNum"])

def createDir():
	if not os.path.exists(dirName):
		os.makedirs(dirName + '/Images')
		os.makedirs(dirName + '/PDF')


def getImage(pic,dirname,i):
	#This block of code downloads images from the path locally
	pageLinks = "https://lecturenotes.in" + pic
	r = requests.get(pageLinks)
	print(i)
	with open(dirName + '/Images/' + str(i) + '.jpeg', 'wb') as f:
		f.write(r.content)
		f.close()
	imagenames.append(dirName + '/Images/' + str(i) + '.jpeg')


def makePDF():
	#This block of code converts the downloaded images to PDF
	with open(dirName + '/PDF/' + dirName + ".pdf","wb") as f:
		f.write(img2pdf.convert(imagenames))
		f.close

if __name__ == "__main__":

	print("Enter Note ID: ")
	noteid = input()
	print("Enter filename: ")
	dirName = input()
	getURL(noteid)
	makePDF()