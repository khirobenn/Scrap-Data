import time
import requests
import io
from PIL import Image
from selenium import webdriver


# options_chrome = webdriver.ChromeOptions()
# options_chrome.add_argument('-headless')
# options_chrome.add_argument('-no-sandbox')
# options_chrome.add_argument('-disable-dev-shm-usage')

wd = webdriver.Chrome()

def scroll(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHieght);")

def get_images(wd, delay, size):

    url = "https://www.google.com/search?q=Queen+chess&sca_esv=a931ccad8231bca2&source=hp&biw=1397&bih=663&ei=jxPiZ5_3HPaJkdUPjdzd4Ak&iflsig=ACkRmUkAAAAAZ-Ihn2Pi_5CMUGgb80ELiou8lN2rmfrV&ved=0ahUKEwjf-t-3lqSMAxX2RKQEHQ1uF5wQ4dUDCBc&uact=5&oq=Queen+chess&gs_lp=EgNpbWciC1F1ZWVuIGNoZXNzMgUQABiABDIFEAAYgAQyBRAAGIAEMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeMgQQABgeSIYdULsGWMobcAR4AJABAJgBJ6AB5gOqAQIxNLgBA8gBAPgBAYoCC2d3cy13aXotaW1nmAIQoAKlBKgCAMICDhAAGIAEGLEDGIMBGIoFwgILEAAYgAQYsQMYgwHCAggQABiABBixA5gDAZIHAjE2oAfoRLIHAjE0uAeeBA&sclient=img&udm=2#vhid=fLkcuxMOaHUaeM&vssid=mosaic"
    wd.get(url)
    wd.find_elements(webdriver.common.by.By.CLASS_NAME, "QS5gu")[2].click()
    time.sleep(delay)
    image_urls_set = set()

    while len(image_urls_set) < size :
        scroll(wd)
        thumbnails = wd.find_elements(webdriver.common.by.By.CLASS_NAME, "YQ4gaf")
        # print(thumbnails)
        for img in thumbnails[len(image_urls_set): size]:
            try:
                img.click()
                # print(wd.find_elements(webdriver.common.by.By.CLASS_NAME, "sFlh5c"))
                time.sleep(delay)
            except:
                continue


def download_image(url, file_name, folder):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = folder + '/' + file_name

        with open(file_path, 'wb') as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print("Failed :", e)


get_images(wd, 3, 5)
wd.quit()