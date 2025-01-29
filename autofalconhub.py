from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from getpass import getpass
from time import sleep
import os

def get_autofalcon_path():
    return os.path.join(os.path.expanduser('~'), 'Downloads', 'AutoFalcon-main')

def find_file_in_autofalcon(filename):
    autofalcon_path = get_autofalcon_path()
    for root, dirs, files in os.walk(autofalcon_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

gmailId = input('Enter the gmailid: ')
pwd = getpass('Enter Password: ')
#driver = webdriver.Edge(r"C:\edgedriver_win64 (1)\msedgedriver.exe")
##driver_path = os.path.join(get_downloads_path(), 'msedgedriver.exe')
driver_path = find_file_in_autofalcon('msedgedriver.exe')
if not driver_path:
    print('WebDriver file not found in AutoFalcon-main directory.')
    exit()
service = Service(driver_path)
driver = webdriver.Edge(service=service)
try:
    #driver = webdriver.Edge(executable_path=r"C:\edgedriver_win64 (1)\msedgedriver.exe")
    driver.get(r'https://faithkids.myschoolapp.com/app/?fromHash=login#login')
    driver.maximize_window()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Username')))
    
    loginBox = driver.find_element(By.ID, 'Username')
    loginBox.send_keys(gmailId)
    
    nextButton = driver.find_element(By.ID, 'nextBtn')
    nextButton.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'primary-button')))
    
    nextButton = driver.find_element(By.ID, 'primary-button')
    nextButton.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
    
    loginBox = driver.find_element(By.ID, 'identifierId')
    loginBox.send_keys(gmailId)
    
    nextButton = driver.find_element(By.ID, 'identifierNext')
    nextButton.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
    
    passWordBox = driver.find_element(By.NAME, 'Passwd')
    passWordBox.send_keys(pwd)
    
    nextButton = driver.find_element(By.ID, 'passwordNext')
    nextButton.click()
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'assignment-center-btn')))
    
    nextButton = driver.find_element(By.ID, 'assignment-center-btn')
    nextButton.click()
    
    print('Login Successful...!!')
    sleep(10)
    driver.quit()
except Exception as e:
    print('Login Failed:', str(e))
    driver.quit()
