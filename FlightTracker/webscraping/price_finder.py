import time, smtplib, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
SMTP_ADRESS = os.environ.get('SMTP_ADRESS')

origin = "YYG" # Charllotetown
destination = "FLN" # Florianopolis

port = 587
days = [29,30,1,2,3]
months = [9,9,10,10,10]
year = 2025
price_target = 800

# create departure and return dates based on the days and month Lists
departure_dates = [datetime(year, month, day) for day, month in zip(days, months)]
return_dates = [departure + timedelta(days=14) for departure in departure_dates]

def get_prices(d, r):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver =  webdriver.Chrome(options=chrome_options)
    login_url = "https://www.aircanada.com/home/ca/en/aco/flights"
    # time sleeps to wait the page properly open
    login = driver.get(login_url)
    time.sleep(8)
    # print("here")
    time.sleep(0.3)
    cookies_button = driver.find_element(By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
    cookies_button.click()
    time.sleep(0.3)
    selct = driver.find_element(By.XPATH, value='//*[@id="flightsOriginLocationbkmgLocationContainer"]/div')
    time.sleep(0.3)
    selct.click()

    # set origin and destination at the website
    ogn_dst = driver.find_element(By.NAME, value='flightsOriginLocation')
    time.sleep(0.3)
    ogn_dst.send_keys(origin, Keys.TAB, Keys.TAB, Keys.TAB, destination, Keys.TAB, Keys.TAB, Keys.TAB, d, Keys.TAB, r)
    
    time.sleep(0.3)
    search_button = driver.find_element(By.ID, value='bkmg-desktop_findButton')
    search_button.click()
    time.sleep(10)
    all_prices = []

    # find all prices in economic class
    price_element = driver.find_elements(By.CSS_SELECTOR, 'span.cabin-price.font-size-24.font-weight-semi-bold.black.ng-star-inserted')
    for price in price_element:
        time.sleep(0.1)
        valor =price.text.replace("$","").replace(",", "")
        all_prices.append(int(valor))
        # print(valor)
    driver.quit()
    return min(all_prices)

def get_direct(dd, dm, rd , rm):
    # print(dd, dm, rd, rm)
    direct_url =f'https://www.aircanada.com/booking/ca/en/aco/search?org0={origin}&dest0={destination}&orgType0=A&destType0=A&org1={destination}&dest1={origin}&orgType1=A&destType1=A&departureDate0={dd}%2F{dm}%2F{year}&departureDate1={rd}%2F{rm}%2F{year}&adt=2&yth=0&chd=0&inf=0&ins=0&marketCode=INT&tripType=RoundTrip&isFlexible=false'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver =  webdriver.Chrome(options=chrome_options)
    driver.get(direct_url)
    time.sleep(10)
    all_prices = []

    # find all prices in economic class
    price_element = driver.find_elements(By.CSS_SELECTOR, 'span.cabin-price.font-size-24.font-weight-semi-bold.black.ng-star-inserted')
    for price in price_element:
        time.sleep(0.1)
        valor =price.text.replace("$","").replace(",", "")
        all_prices.append(int(valor))
        print(valor) if int(valor) < 999 else None
    driver.quit()
    return min(all_prices)


text = ""
send = False

# for dates check flights prices
for departure, return_date in zip(departure_dates, return_dates):
    # day_price = get_prices(departure.strftime('%d/%m'), return_date.strftime('%d/%m'))
    day_price = get_direct(departure.strftime('%d'),departure.strftime('%m') , return_date.strftime('%d'),return_date.strftime('%m'))
    if day_price < price_target:
        text += f'Fligh for {departure.strftime('%d/%m')} is ${day_price}\n'
        send = True
        print(text)

# if flights price is under a target, send an email
if send:
    print('Sending email...')
    with smtplib.SMTP(SMTP_ADRESS, port) as connection:
         # connection.ehlo()
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="alphacherno15@gmail.com",
            msg=f"Subject:Flight Price Alert!\n\n{text}")
