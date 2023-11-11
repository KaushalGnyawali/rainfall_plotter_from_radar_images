from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import base64
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from PIL import Image



def scraper(website_url):
    output_folder='images'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    driver = webdriver.Edge()
    driver.get(website_url)

    current_iteration = 0
    max_iterations = 100
    while current_iteration < max_iterations:
        try:

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")

            gif_tags = soup.find_all('img', class_='img-responsive mrgn-bttm-md')
            name_element = soup.find("div", class_="animation-info")
            text = name_element.get_text()

            d = gif_tags[0]['src'].split(',')[1]
            gif_url = urljoin(website_url, gif_tags[0]['src'])
            date = text.split(', ')[0][-10:]
            gif_filename = text.split(', ')[1] 
            gif_filename= date.split('-')[0] + date.split('-')[1] + date.split('-')[2] +'_'+ gif_filename.split(' ')[0].split(':')[0] + gif_filename.split(' ')[0].split(':')[1]  + '.png'
        
            output_path = os.path.join(output_folder,gif_filename)

            image_data = base64.b64decode(d)
        
            image = Image.open(BytesIO(image_data))
            image.save(output_path, format="PNG")
            current_iteration += 1
            
            button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "previousimage")))
            button.click()
            
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.TAG_NAME, "img")))
        except:
            break
            
    driver.quit()

    print("Images download done!")