import sys
import hashlib
from ConfigParser import SafeConfigParser


def main():
    if len(sys.argv) < 3:
        sys.exit('Usage: AddUser.py <username> <password> \n Set password to "-" to delete a user')

    parser = SafeConfigParser()
    parser.read('users.ini')

    if not parser.has_section('users'):
        parser.add_section('users')

    try:
        if sys.argv[2] == "-":
            parser.remove_option('users', sys.argv[1])
        else:
            parser.set('users', sys.argv[1], hashlib.md5(sys.argv[2].strip()).hexdigest())
    except Exception as e:
        print(e)
        pass

    # prevent an empty file -- always have a default user if there is no other user
    if len(parser.options('users')) == 0:
        parser.set('users', 'default', hashlib.md5('default').hexdigest())

    with open('users.ini', 'w') as f:
        f.write('#This is the list of users/encrypted passwords for the Linux CNC Web Server\n\n')
        f.write('#Use the included python script AddUser to add users\n')
        f.write('#Users can be removed by deleting the entries in this file with their user name\n')
        f.write('#This file will be auto-generated and overwritten by the AddUser program\n\n')
        parser.write(f)


# auto start if executed from the command line
if __name__ == "__main__":
    main()
