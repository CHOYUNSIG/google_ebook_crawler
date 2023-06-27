import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import base64
import re
import pygame
import subprocess


root = os.getcwd()


pygame.init()

# pygame handler
screen = pygame.display.set_mode((640, 400))
clock = pygame.time.Clock()


def get_file_content_chrome(driver, uri):
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
  if type(result) == int :
    raise
  result = base64.b64decode(result)
  if len(result) < 100 :
    raise
  return result

  

# open chrome
try:
  session = subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="' + root + r'\temp"')
except:
  print("Cannot load Chrome.exe")
  exit()

# chrome event handler
chrome_options = Options()
chrome_options.add_experimental_option(r"debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)
def click(xpath):
  global driver, wait
  wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
  driver.find_element(By.XPATH, xpath).click()

# main stream
def main_stream():
  global driver, wait, session

  # open login page
  driver.get(r"https://play.google.com/store/books")
  click(r'/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[1]/button')
  if len(driver.find_elements(By.XPATH, r'/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[12]')) > 0:
    click(r'/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[12]')
  else:
    click(r'/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[1]')

  # retry until login done successfully
  print("Login.")
  while(True):
    if driver.current_url[0:35] == "https://play.google.com/store/books" and driver.find_elements(By.XPATH, r'/html/body/c-wiz[1]/header/nav/div/c-wiz/div/div/div[2]/div/ul/li[12]'):
      break

  # open library page
  print("Open the book.")
  click(r'/html/body/c-wiz[2]/div/div/c-wiz/div/div/div/div/div[4]')

  # retry until book is opened successfully
  while(True):
    if len(driver.window_handles) > 1:
      break
  driver.switch_to.window(driver.window_handles[1])
  while(True):
    if driver.current_url[0:36] == "https://play.google.com/books/reader":
      break

  driver.switch_to.frame(driver.find_element(By.XPATH, r'/html/body/iframe'))

  # click view setting menu
  click(r'//div[@class="nav-group end"]/button[3]')
  wait.until(EC.element_to_be_clickable((By.XPATH, r'//mat-dialog-container/reader-display-options/button')))

  # horizontal mode
  if driver.find_elements(By.XPATH, r'//label[@for="mat-mdc-slide-toggle-2-button"]/../button[@aria-checked="true"]'):
    click(r'//label[@for="mat-mdc-slide-toggle-2-button"]/../button[@aria-checked="true"]')

  # reading-mode-select
  if driver.find_elements(By.XPATH, r'//label[@for="reading-mode-select"]'):
    click(r'//label[@for="reading-mode-select"]/following-sibling::mat-form-field[1]/div/div[1]')
    click(r'//mat-option[1]')

  # zoom-select
  click(r'//label[@for="zoom-select"]/following-sibling::mat-form-field[1]/div/div[1]')
  click(r'//mat-option[5]')

  # page-layout
  click(r'//label[@for="page-layout"]/following-sibling::mat-button-toggle-group[1]/mat-button-toggle[3]/button')

  # reload page
  driver.refresh()
  driver.switch_to.default_content()
  driver.switch_to.frame(driver.find_element(By.XPATH, r'/html/body/iframe'))

  # open first page
  click(r'//div[@class="nav-group end"]/button[4]')
  click(r'//div[@class="mat-tab-labels"]/div[1]')
  click(r'//mat-nav-list/a[1]')
  click(r'//mat-dialog-container/reader-contents/button')

  # get resolution
  wait.until(EC.presence_of_all_elements_located((By.XPATH, r'//reader-page[@id="page-0-0"]/reader-rendered-page/img')))
  resolution = int(driver.find_element(By.XPATH, r'//reader-page[@id="page-0-0"]/reader-rendered-page/img').get_attribute("real-width"))

  # get total page
  click(r'//div[@class="nav-group end"]/button[7]')
  click(r'//mat-dialog-container/reader-overflow-menu/div/button[1]')
  while(len(driver.find_element(By.XPATH, r'//mat-dialog-container/info-dialog/mat-dialog-content/div/div/h3[2]').text) == 0):
    pass
  total_page = int(re.sub(r"[^0-9]", r"", driver.find_element(By.XPATH, r'//mat-dialog-container/info-dialog/mat-dialog-content/div/div/h3[2]').text))
  click(r'//mat-dialog-container/info-dialog/div/button')

  # final checking
  print("Total pages : " + str(total_page))
  print("Width resolution : " + str(resolution) + "px")
  input("Enter to process. (Monitoring is available in " + root + "\\img folder.)")

  # start downloading
  print("Processing..")
  count = 0
  while(True) :
    try :
      wait.until(EC.presence_of_all_elements_located((By.XPATH, r'//reader-page[@id="page-' + str(count) + r'-0"]/reader-rendered-page/img')))
      image = driver.find_element(By.XPATH, r'//reader-page[@id="page-' + str(count) + r'-0"]/reader-rendered-page/img')
      with open(root + r"/img/" + str(count) + r".jpg", r'wb') as f:
        while(True) :
          try :
            f.write(get_file_content_chrome(driver, image.get_attribute(r"src")))
            break
          except :
            sleep(0.1)
      count = count + 1
      if count == total_page:
        break
      click(r'//div[@class="scrubber-container"]/button[2]')
    except :
      break
  print("Done.")

  # end stream
  input("Check " + root + "\\img, then enter to exit.")
  session.kill()
  print("Exiting..")
  driver.quit()
  exit()



# start main stream
if __name__ == "__main__":
  main_stream()