import time,sys,os
from selenium import webdriver

print(sys.argv[1])

driver = webdriver.Chrome(os.getcwd()+'\\chromedriver.exe')  # Optional argument, if not specified will onTableSearch path.
#driver.get('https://10.73.161.98/#/login')
driver.get(sys.argv[1])
time.sleep(2) # Let the user actually see something!
print('*'*20)
print (driver.current_url)


input_user = driver.find_element_by_name('userName')
input_user.send_keys('Nemuadmin')


input_pass = driver.find_element_by_name('password')
input_pass.send_keys('nemuuser')
input_pass.submit()




print('*'*20)
print(driver.current_url)

time.sleep(8)
driver.find_element_by_xpath('//div[@class="ui-modal"]//button[1]').click()
time.sleep(2)
driver.find_element_by_xpath('//div[@class="site-panel-tabs ng-isolate-scope"]//ul[@class="nav nav-tabs"]/li[2]/a').click()
time.sleep(1)
driver.find_element_by_xpath('//div[@class="details-panel-container"]//ui-button/button').click()

driver.execute_script("document.body.style.zoom='67%'")

driver.maximize_window()