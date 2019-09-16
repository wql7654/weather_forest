from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv

#starting a new browser session
browser = webdriver.Chrome('C:\\Users\\noteland\\ansel\\chromedriver.exe')
browser.maximize_window() #For maximizing window
browser.implicitly_wait(20) #gives an implicit wait for 20 seconds
#navigating to a webpage
browser.get('https://www.instagram.com/')

# make sure the browser stays open for 5sec
sleep(5)

#clean exit


#find Log in link
login_elem = browser.find_element_by_xpath(
	'//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a')

#clicks log in
login_elem.click()

# find form inputs and enter data
inputs = browser.find_elements_by_xpath(
	'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/div/input')

inputs2 = browser.find_elements_by_xpath(
	'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/input')
ActionChains(browser)\
.move_to_element(inputs[0]).click()\
.send_keys('mtheory101')\
.move_to_element(inputs2[0]).click()\
.send_keys('Alliswithin1')\
.perform()

# find the log in button and click it
login_button = browser.find_element_by_xpath(
	'//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button')

#could have been part of the above actionchain
ActionChains(browser)\
.move_to_element(login_button)\
.click().perform()
    
search = browser.find_element_by_css_selector(
	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

ActionChains(browser)\
.move_to_element(search).click()\
.send_keys('dylanwerneryoga')\
.perform()

name = browser.find_element_by_xpath(
	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

ActionChains(browser)\
.move_to_element(name)\
.click().perform()


sleep(5)
post = browser.find_element_by_class_name('_si7dy')
post.click()




load= browser.find_element_by_xpath(
	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

while True:
	try:
		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
        	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
	except TimeoutException:
		break  # no more wines
	button.click()  # load more comments



csv_file = open('insta2.csv', 'wb')
writer = csv.writer(csv_file)
writer.writerow(['hashtag'])


hash_dict = {}



tag = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[4]/span").text
hash_dict["hashtag"] = tag
writer.writerow(hash_dict.values()) 


browser.back()


	


sleep(5)

search = browser.find_element_by_css_selector(
	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

ActionChains(browser)\
.move_to_element(search).click()\
.send_keys('laurasykora')\
.perform()

name = browser.find_element_by_xpath(
	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

ActionChains(browser)\
.move_to_element(name)\
.click().perform()



sleep(5)
post = browser.find_element_by_class_name('_si7dy')
post.click()




load= browser.find_element_by_xpath(
	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

while True:
	try:
		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
        	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
	except TimeoutException:
		break  # no more wines
	button.click()  # load more comments






tag = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]").text
hash_dict["hashtag"] = tag
writer.writerow(hash_dict.values())



browser.back()


#############################



sleep(5)

search = browser.find_element_by_css_selector(
	'#react-root > section > nav > div._s4gw0._1arg4 > div > div > div._5ayw3._ohiyl > input')

ActionChains(browser)\
.move_to_element(search).click()\
.send_keys('laurasykora')\
.perform()

name = browser.find_element_by_xpath(
	'//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div')

ActionChains(browser)\
.move_to_element(name)\
.click().perform()



sleep(5)
post = browser.find_element_by_class_name('_si7dy')
post.click()




load= browser.find_element_by_xpath(
	'/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a')

while True:
	try:
		button = WebDriverWait(load, 5).until(EC.visibility_of_element_located((By.XPATH, 
        	"/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]/a")))
	except TimeoutException:
		break  # no more wines
	button.click()  # load more comments



tag = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/article/div[2]/div[1]/ul/li[2]").text
hash_dict["hashtag"] = tag
writer.writerow(hash_dict.values())



browser.back()


	
csv_file.close()