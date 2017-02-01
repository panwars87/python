__author__ = 'shashant'

import menus

def take_order():
    orders = []
    meal = input("Which meal would you like to have B, L or D? (Q to Quit) : \n")
    if meal.upper() == 'Q':
        exit()

    order = input("What would you like to order? (Q to Quit) : \n")
    while True:
        if order.upper() == 'Q':
            break

        # Find the order and add it to the list if it exists
        if meal.upper() == 'B':
            if order in menus.menus['breakfast']:
                orders.append(order)
            else:
                print('Not a breakfast item, please choose : ' + str(menus.menus['breakfast']))

        order = input('Anything else? (Q to Quit) : \n')
        #  See if the customer wants to order anything else

    print('Your final order {}'.format(orders))