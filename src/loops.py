__author__ = 'shashant'

total = 0
print('for loop example \n')
prices = [1.25, 3.0, 4.0, 4.5, 5.0]
for price in prices:
    # print('Price is : ' + str(price))
    total += price

avg = total/len(prices)
print('total is : ' + str(total))
print('avg is : ' + str(avg))

for i in range(3):
    print(i)

for i in range(2005, 2017, 3):
    print(i)

menus = {
    'breakfast': ['eggs', 'toast', 'poha', 'bhel'],
    'lunch': ['soups', 'salad', 'chicken', 'vegetables'],
    'dinner': ['soups', 'salad', 'fish', 'grill']
}

price = 0.50
menu_price = {}
for menu in menus:
    # print(menu)
    for item in menus[menu]:
        # print(item)
        menu_price[item] = price
        price += 1

print(menu_price)
print(menu_price.keys())
print(menu_price.values())

for name, price in menu_price.items():
    print(name, ': $', format(price, '.2f'), sep='')



