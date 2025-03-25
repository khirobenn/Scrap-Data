
import time
import requests
import io
from PIL import Image
import base64
from selenium import webdriver
import sys

def scroll(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def get_images(wd, delay, size, url):
    wd.get(url)
    wd.find_elements(webdriver.common.by.By.CLASS_NAME, "QS5gu")[2].click()
    time.sleep(2)
    image_urls_set = set()
    last_height = wd.execute_script("return document.body.scrollHeight")
    while len(image_urls_set) < size:
        scroll(wd)
        time.sleep(delay)
        new_height = wd.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            break
        else:
            last_height = new_height

        thumbnails = wd.find_elements(webdriver.common.by.By.CLASS_NAME, "YQ4gaf")

        for img in thumbnails[len(image_urls_set): size]:
            try:
                src = img.get_attribute("src")
                if 'favicon' in src:
                    continue

                height = int(img.get_attribute("height"))
                width = int(img.get_attribute("width"))

                if height < 30 or width < 30:
                    continue

                if 'encrypted' not in src:
                    src = src.split(',')[1]

                image_urls_set.add(src)
            except:
                continue
    return image_urls_set


def download_image(url, folder, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = folder + '/' + file_name + '.jpg'

        with open(file_path, 'wb') as f:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image.save(f, "JPEG")

    except Exception as e:
        print("Failed :", e)

def convert_url_to_image(url, path, filename):
    if 'encrypted' in url:
        download_image(url, path, filename)
        return
    
    try:
        with open(path + '/' + filename + '.jpg', 'wb') as f:
            f.write(base64.decodebytes(url.encode()))
    except Exception as e:
        print("Error :", e)

def main():
    if len(sys.argv) != 5:
        print("Error : you should put 3 arguments!")
        print("arg1: url.")
        print("arg2: path to the folder you want to save your pictures.")
        print("arg3: start name of your pictures (for example : car, your files will be car1.jpg, car2.jpg,..)")
        print("arg4: the maximum of pictures you want.")
        return

    wd = webdriver.Chrome()
    url = sys.argv[1]
    path = sys.argv[2]
    filename = sys.argv[3]
    max_size = int(sys.argv[4])
    url_images = get_images(wd, 2, max_size, url)
    wd.close()
    i = 0
    for x in url_images:
        convert_url_to_image(x, path, filename + str(i))
        i = i + 1

main()