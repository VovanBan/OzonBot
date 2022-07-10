import undetected_chromedriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import lxml
import time
import json
import re

def parseozon(page: int):
    global driver
    total = 0

    for i in range(page):
        try:
            driver = undetected_chromedriver.Chrome()
            driver.get(f'https://www.ozon.ru/category/igrovye-noutbuki-15821/?page={i+1}')
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            list_of_item = driver.find_elements(by=By.CLASS_NAME, value='j2u')

            data = []
            for item in list_of_item:
                soup = BeautifulSoup(item.get_attribute("outerHTML"), 'lxml')
                item_name = soup.find('span', class_='d9m m9d dn0 n1d tsBodyL s4j').get_text()
                item_photo = soup.find('div', class_='u2j').find('a')['href']

                if soup.find('span', class_='ui-r2') is not None:
                    item_price = soup.find('span', class_='ui-r2').get_text()
                else:
                    item_price = soup.find('span', class_='ui-q5').get_text()

                if soup.find('span', class_='ui-q5') is not None:
                    item_price_bonus = soup.find('span', class_='ui-q5').get_text()
                else:
                    item_price_bonus = soup.find('span', class_='ui-r2').get_text()

                item_info = [i.get_text() for i in soup.find('span', class_='d9m m9d n2d tsBodyM').find_all('font')]
                item_info.extend(['Отсутствует', 'Отсутствует', 'Отсутствует', 'Отсутствует', 'Отсутствует'])
                item_processor = item_info[0]
                item_memory = item_info[1]
                item_ssd = item_info[2]
                item_video = item_info[3]
                item_oc = item_info[4]

                item_price = re.sub(r'\s', '', str(item_price))
                item_price = re.sub(r'₽', '', str(item_price))
                item_price_bonus = re.sub(r'\s', '', str(item_price_bonus))
                item_price_bonus = re.sub(r'₽', '', str(item_price_bonus))

                data.append(
                    {
                        'Name': item_name,
                        'Photo': item_photo,
                        'Price': item_price,
                        'Price Bonus': item_price_bonus,
                        'Processor': item_processor,
                        'Memory': item_memory,
                        'SSD': item_ssd,
                        'Video Сard': item_video,
                        'OC': item_oc
                    }
                )

            with open(f'Laptops\laptops-{i+1}.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            total += 1
            print(f'{i+1}')

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()
    return total
