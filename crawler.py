import base64
import io
import os
import subprocess
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from path import *

# check folders
for folder_name in ["pdf", "temp"]:
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# open chrome
session = subprocess.Popen(chrome_path + f" --remote-debugging-port=9222 --user-data-dir={os.getcwd()}\\temp")

# chrome event handler
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_file(uri: str) -> bytes:
    result = driver.execute_async_script("""
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
    """, uri)
    if type(result) is int:
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)


def filename(name: str) -> str:
    return name.translate({ ord(letter): chr(ord(letter) + 0xFEE0) for letter in r'\/:*?"<>|' })


def click(xpath: str, timeout: float = 1.0):
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.find_element(By.XPATH, xpath).click()


def get_text(xpath: str, timeout: float = 1.0) -> str:
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_element(By.XPATH, xpath).text


def poll_url(url: str):
    while True:
        current_url = driver.current_url
        if current_url and current_url[:len(url)] == url:
            break
        sleep(0.01)


def poll_xpath(xpath: str, timeout: float = 5.0):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))


def main_stream():
    # login
    driver.get(google_play_books_url)
    try:
        click(account_button, 10)
        click(login_button)
        print("Login.")
        poll_url(google_play_books_url)
    except TimeoutException:
        pass

    # open book
    driver.get(library_url)
    print("Open the book.")
    poll_url(book_reader_url)

    # switch frame
    driver.switch_to.frame(driver.find_element(By.XPATH, iframe_tag))

    # set view
    click(display_setting_button)
    try:
        click(reading_dropdown)
        click(option_first_button)
    except TimeoutException:
        pass
    click(zoom_dropdown)
    click(option_last_button)
    try:
        click(scroll_toggle)
    except:
        pass
    click(layout_checkbox)
    click(display_setting_button)

    # get book info
    click(more_button)
    click(info_button)
    book_title = filename(get_text(book_title_tag))
    book_author = filename(get_text(author_tag))
    book_publisher = filename(get_text(publisher_tag))
    click(info_close_button)
    print()
    print("title: " + book_title)
    print("author: " + book_author)
    print("publisher: " + book_publisher)
    print()

    # open first page
    click(content_table_button)
    click(first_page_button)
    click(content_table_button)

    # reload page
    driver.refresh()
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, iframe_tag))

    # start downloading
    print("Processing..")
    result = []
    while True:
        try:
            book_page_container = book_page_containers + f"[@id='page-{len(result)}-0']"
            poll_xpath(book_page_container, 10)
            while True:
                container = driver.find_element(By.XPATH, book_page_container)
                image_uri = container.find_element(By.TAG_NAME, "img").get_attribute("src")
                if image_uri[:4] == "blob":
                    break
                sleep(0.01)
            image = get_file(image_uri)
            image_bytesio = io.BytesIO(image)
            image_pil = Image.open(image_bytesio)
            result.append(image_pil)
            click(next_page_button)
        except TimeoutException:
            print("Page ended.")
            break
        except Exception as e:
            print(e)
            print(f"Exception has occured. Work is ended at page {len(result)}.")
            break

    print("Saving...")
    result[0].save(f"pdf/{book_title}-{book_author}-{book_publisher}.pdf", save_all=True, append_images=result[1:])
    print("Done.")

    print("Exiting..")
    driver.quit()
    session.kill()
    exit()


if __name__ == "__main__":
    main_stream()
