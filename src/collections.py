__author__ = 'shashantp'

# list
namelist = ['nishu', 'kittu', 'shweta', 'adu']
print('Original list: ' + str(namelist))

# dictionary
occupation = {'nishu':'engineer', 'kittu':'analyst', 'shweta':'engineer', 'adu':'kid'}
print('Original dict:  ' + str(occupation))

print('\nlist operation\n')
namelist.append('shashant')
print(namelist)
namelist.remove(namelist[0])
print(namelist)
namelist.append('shubham')
del namelist[0]
print(namelist)

print('\ndictionary operations\n')
print(occupation['nishu'])
del occupation['adu'];
print(occupation.get('adu'))
print(occupation.get('nishu'))

print('\nDictionary of lists')
menus = {
    'breakfast': ['eggs', 'toast', 'poha', 'bhel'],
    'lunch': ['soups', 'salad', 'chicken', 'vegetables'],
    'dinner': ['soups', 'salad', 'fish', 'grill']
}

print(str(menus['breakfast']) + '\n' + str(menus['lunch']) + '\n' + str(menus['dinner']))


