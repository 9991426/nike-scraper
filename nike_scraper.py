import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from twilio.rest import Client



### SET UP WITH PERSONAL TWILIO ACCOUNT AND OTHER VARIABLES ###

account_sid = ""    # Include personal Twilio account SID here
auth_token = ""     # Include personal Twilio auth token here
twilio_phone = ""   # Include Twilio phone number
client = Client(account_sid, auth_token)
numbers_to_message = []     # Include the list of phone numbers here. 
                            # Include it in the proper format as a string (EX: '+19876543210').
                            
url_item_avail = "https://www.nike.com/t/air-max-90-mens-shoes-6n3vKB/CN8490-002"       # Include URL of available item
url_item_unavail = "https://www.nike.com/u/custom-nike-air-force-1-unlocked-by-you-10001230/8294575982"     # Include URL of unavailable item
unavail_test_str = "Great choice, but"      # Include a long enough string that is used on unavailable items.



### SET UP WEBDRIVER OPTIONS ###
# "--headless" allows the browser to run in the background... It is also necessary for Heroku.
# "--disable-dev-shm-usage" allows for rendering larger web pages.
# "--no-sandbox" disables a Chrome feature that is not included with Heroku's Linux.
# "GOOGLE_CHROME_BIN" and "CHROMEDRIVER_PATH" lines are for storing Heroku's environment variables 
# (essentially needed so that Heroku can provide its version of Chrome).

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage") 
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)



### TEST CODE TO MAKE SURE THAT THE PROGRAM WILL CONSISTENTLY WORK ###
# First, the test code uses the scraper on a product that is available for certain.
# Second, the test code uses the scraper on the URL of the desired product that is currently unavailable.

driver.get(url_item_avail)
print(driver.title)

el = driver.find_element(By.TAG_NAME, 'body')
str = el.text 

if(str.find(unavail_test_str) != -1):
    print("Not Available")
    for number in numbers_to_message:
        client.messages.create(
            body = 'This is a test: the item is not available! :^(',
            from_ = twilio_phone,
            to = number
        )
else: 
    print("Available")
    for number in numbers_to_message:
        client.messages.create(
            body = 'This is a test: the item is available! :^)',
            from_ = twilio_phone,
            to = number
        )   
time.sleep(150)

driver.get(url_item_unavail)
print(driver.title)

el = driver.find_element(By.TAG_NAME, 'body')
str = el.text 

if(str.find(unavail_test_str) != -1):
    print("Not Available")
    for number in numbers_to_message:
        client.messages.create(
            body = 'This is a test: item is not available! :^(',
            from_ = twilio_phone,
            to = number
        )
else: 
    print("Available")
    for number in numbers_to_message:
        client.messages.create(
            body = 'This is a test: the item is available! :^)',
            from_ = twilio_phone,
            to = number
        )    
time.sleep(150)

### End of Test Code ###



### Actual scraper on desired Nike product ###
# "status" variable ensures that designated phone numbers are not bombarded with notifications every 2.5 minutes!

status = 0

while(True):
    driver.get(url_item_unavail)
    el = driver.find_element(By.TAG_NAME, 'body')
    str = el.text 

    if(str.find(unavail_test_str) != -1):
        print("Not Available")
        if(status == 1):
            for number in numbers_to_message:
                client.messages.create(
                    body = 'The item was available but is now unavailable <:^(',
                    from_ = twilio_phone,
                    to = number
                )
        status = 0
    else: 
        print("Available")
        if(status == 0):
            for number in numbers_to_message:
                client.messages.create(
                    body = 'The item is now available! >:^)',
                    from_ = twilio_phone,
                    to = number
                )
        status = 1        
    time.sleep(150)