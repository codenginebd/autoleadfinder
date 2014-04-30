__author__ = 'Codengine'

from DBManager import *

db = DBWraper()

def main():
    print 'Initializing Database'
    db.init_db()
    print 'Database Initialization Done.'

if __name__ == '__main__':
    main()
