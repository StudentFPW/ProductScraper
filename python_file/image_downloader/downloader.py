import pandas as pd
import urllib.request


def url_to_jpg(i, url, file_path):
    filename = "image-{}.jpg".format(i)
    full_path = "{}{}".format(file_path, filename)
    urllib.request.urlretrieve(url, full_path)
    print("Downloaded = {}".format(filename))


FILENAME = "data.xlsx"
FILE_PATH = "images/"

urls = pd.read_excel(FILENAME, usecols="D")

for i, url in enumerate(urls.values, 2):
    url_to_jpg(i, url[0], FILE_PATH)
