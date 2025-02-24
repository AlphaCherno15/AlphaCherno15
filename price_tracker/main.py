import smtplib, requests, os, json, time
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
SMTP_ADRESS = os.environ.get('SMTP_ADRESS')
port = 587

# https://httpbin.org/headers
# https://myhttpheader.com
headers1 = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Opera\";v=\"115\", \"Not?A_Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0",
  }

headers2 ={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        }
debug = ""
text = ""
send = False
write_log = False
def read_file(file):
    global debug, write_log
    # try:
    #     response = requests.get("https://api.npoint.io/45ab6e888e31b49b41c1")
    #     file_data = response.json()
    # except Exception as e:
    #     write_log = True
    #     debug += f'Looking for the {response} the error "{e}" orccured\n'
    #     with open(f'price_tracker/{file}.json', "r") as data:
    #         file_data = json.load(data)
    with open(f'price_tracker/{file}.json', "r") as data:
            file_data = json.load(data)
    return file_data
def error_report(report):
    with open(f'price_tracker/log.txt', "w") as log:
        log.write(report)
def get_price(link, store, product):
    global text, write_log, debug
    result = 1000000
    if store == "wait":
        sleep = 5 * 60
        time.sleep(sleep)
    elif store == "amazon":
        response = requests.get(link, headers=headers1)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.find(name='span', class_='a-offscreen').getText()
            price_edit = float(price.replace('$', ''))
            print("Tried once")
        except:
            try:
                soup = BeautifulSoup(response.content, 'html.parser')
                price = soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole').getText()
                price_edit = float(price.replace('$', ''))
                print("Tried twice")
            except:
                try:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    price = soup.find(name='span', class_='aok-offscreen').getText()
                    price_edit = float(price.replace('$', ''))
                    print("Last try")
                except Exception as e:
                    write_log = True
                    debug += f'Looking for the {product} the error "{e}" orccured\n'
            
        else:
            result = price_edit
    elif store == "newegg":
        response = requests.get(link, headers=headers1)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.select_one('#newProductPageContent > div > div > div > div.row-side > div.product-buy-box.is-product-blackfriday-first > div.product-pane > div.product-price > ul > div > div.price-current > strong').getText()
            price_edit = float(price.replace('$', ''))
            print("Tried once")
        except Exception as e:
            write_log = True
            debug += f'Looking for the {product} the error "{e}" orccured\n'
            
        else:
            result = price_edit
        
    return result

list = read_file("items")

for item in list:
    sleep = 30
    time.sleep(sleep)
    item_value = get_price(list[item]["url"], list[item]["store"], item )
    print(f'item price: {item_value}', f'target price: {list[item]["price"]}')
    if item_value < list[item]["price"]:
        text += f'The price of the {item} is now ${item_value}! Buy now! {list[item]["url"]}\n\n'
        send = True
    print(text)

if send:
    print('Sending email...')
    with smtplib.SMTP(SMTP_ADRESS, port) as connection:
         # connection.ehlo()
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs="alphacherno15@gmail.com",
            msg=f"Subject:Shooping Price Alert!\n\n{text}")

if write_log:
    error_report(debug)