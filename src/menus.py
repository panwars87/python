__author__ = 'shashant'

menus = {
    'breakfast': ['eggs', 'toast', 'poha', 'bhel'],
    'lunch': ['soups', 'salad', 'chicken', 'vegetables'],
    'dinner': ['soups', 'salad', 'fish', 'grill']
}
menu_price = {}


def set_menu_price():
    price = 0.50
    for menu in menus:
        # print(menu)
        for item in menus[menu]:
            # print(item)
            menu_price[item] = price
            price += 1


def get_menu_price():
    if len(menu_price) != 0:
        for name, price in menu_price.items():
            print(name.upper(), ': $', format(price, '.2f'), sep='')
    else:
        set_menu_price()
        get_menu_price()


def print_menu():
    print("Welcome to SpamVan, Our Menu")
    get_menu_price()