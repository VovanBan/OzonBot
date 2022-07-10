import json

def selection_price(files, price):
    items_list = []
    for file in files:
        with open(f'Laptops/{file}', 'r', encoding='utf-8') as file:
            items = json.loads(file.read())
            for item in items:
                if int(item['Price Bonus']) <= int(price):
                    items_list.append(item)
    return items_list
