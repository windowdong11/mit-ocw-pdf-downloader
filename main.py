"""
input Example
https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-spring-2015/lecture-slides/
"""

import requests
from bs4 import BeautifulSoup
import os.path
import re

print("Target URL should be start with 'https://ocw.mit.edu'.")
print("Example Input : https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-042j-mathematics-for-computer-science-spring-2015/lecture-slides/")
target_url = input("Input target URL : ")

base_url = "https://ocw.mit.edu"
if target_url.startswith(base_url):
    url = target_url
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find(id="course_inner_section").find_all('tr')
        for tr in rows:
            if not (tr.find('th') or tr.find('strong')):
                # content 1 : unit
                # content 5 : pdf files link & name
                # unit-filenumber-pdf name
                # print(tr.contents[1])
                lectureNumber = tr.contents[1].string
                files = tr.contents[5].find_all('a')

                # Slice with "(PDF", leave only filename
                print(tr.contents[1].string)

                filesCount = 1
                for file in files:
                    # Remove *, |, /, :, ?, <, >, \
                    # To follow file naming rule in windows
                    regex = re.compile(r"[*|/:?<>\\\\]")
                    fileName = file.string.split(" (PDF")[0]
                    fileName = regex.sub('', fileName)
                    fileName = lectureNumber + '.' + str(filesCount) + '-' + fileName + '.pdf'
                    fileUrl = base_url + file['href']
                    print(fileName)
                    if not os.path.isfile(fileName):
                        # Download and write to file, if file not exist
                        response = requests.get(fileUrl)
                        with open(fileName, 'wb') as fd:
                            for chunk in response.iter_content(2048):
                                fd.write(chunk)
                    filesCount += 1
    else:
        print(response.status_code)
        print("Please retry. Or send me issue.")
else:
    print("Target URL : ", target_url)
    print("Target URL does not starts with ", base_url)
