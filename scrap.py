
import time
import requests
import io
from PIL import Image
import base64
from selenium import webdriver

wd = webdriver.Chrome()

def scroll(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def get_images(wd, delay, size):
    url = "https://www.google.com/search?q=Queen+chess&sca_esv=a931ccad8231bca2&source=hp&biw=1397&bih=663&ei=jxPiZ5_3HPaJkdUPjdzd4Ak&iflsig=ACkRmUkAAAAAZ-Ihn2Pi_5CMUGgb80ELiou8lN2rmfrV&ved=0ahUKEwjf-t-3lqSMAxX2RKQEHQ1uF5wQ4dUDCBc&uact=5&oq=Queen+chess&gs_lp=EgNpbWciC1F1ZWVuIGNoZXNzMgUQABiABDIFEAAYgAQyBRAAGIAEMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeSIYdULsGWMobcAR4AJABAJgBJ6AB5gOqAQIxNLgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIQoAKlBKgCAMICDhAAGIAEGLEDGIMBGIoFwgILEAAYgAQYsQMYgwHCAggQABiABBixA5gDAZIHAjE2oAfoRLIHAjE0uAeeBA&sclient=img&udm=2"
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

url_images = get_images(wd, 2, 1000)

i = 0
for x in url_images:
    convert_url_to_image(x, './Queen', 'queen' + str(i))
    i = i + 1