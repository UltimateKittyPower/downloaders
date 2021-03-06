#!/usr/bin/env python3

#Copyright 2017 UltimateKittyPower

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Gallery downloader.
# Supported sites:
#    www.169ee.com
#    www.169mt.com

# Download images in current directory.

import requests  
import grequests  
from lxml import html  
import sys  
import re
from urllib.parse import urljoin, urlsplit

if len(sys.argv) < 2:
    sys.exit("Enter gallery URL.")

link = sys.argv[1]
xpath = "//div[@class='big_img']//img/@src"
req_count = 10

response = requests.get(link)  
parsed_body = html.fromstring(response.text)

# parse images' urls
images = parsed_body.xpath(xpath)
if not images:
    sys.exit("Found no images.")

# search for images' root
img_root = re.match(r".*/", images[0]).group(0)
print("Images' URL root: {}\n".format(img_root))

# image downloading loop
cur = 1
downloaded = 0
halt = False
urls = []
while not halt:
    for i in range(0, req_count):
        urls.append(urljoin(img_root, "{}.jpg".format(cur + i)))
    gets = (grequests.get(u) for u in urls)
    urls = []
    rs = grequests.imap(gets)

    for r in rs:
        if not r.ok:
            halt = True
            continue

        file_name = re.search(r"[0-9]*.jpg", r.url).group(0)
        try:
            f = open(file_name, mode='xb')
        except FileExistsError:
            sys.exit("File '{}' already exists.".format(file_name))
        except:
            sys.exit("Can not create file '{}'.".format(file_name))

        f.write(r.content)
        f.close

        print("Downloaded: {}".format(r.url))
        downloaded += 1
    cur += req_count

print("\n{} images have downloaded.".format(downloaded))
