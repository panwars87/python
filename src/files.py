__author__ = 'shashant'


def read_file(file):
    for line in file:
        print(line.strip())


def write_file(file, message):
    file.write('\n' + message)


def main():
    print('Files modules')
    try:
        file = open('testfile.txt', 'a')
        write_file(file, 'New line entered from code')
        file = open('testfile.txt', 'r')
        read_file(file)
        file.close()
    except:
        print('Exception while reading/writing file')


main()
