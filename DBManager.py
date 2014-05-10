# - * - coding: UTF-8 - * -
from datetime import datetime
import pymysql
from FileHandler import *
import urllib2

db_name = 'autoleadfinder'
uname = 'root'
password = 'root'
host = '127.0.0.1'

class DBWraper:
    def __init__(self):
        try:
            self.dbconn = conn = pymysql.connect(charset='utf8', init_command='SET NAMES UTF8',host=host, port=3306, user=uname, passwd=password, db=db_name)
            #self.dbconn.set_character_set('utf8') #cur = self.dbconn.cursor()
            #cur.execute('SET NAMES utf8;')
            print 'Database connection successfull.'
            #print self.dbconn
        except Exception,msg:
            self.dbconn = None

    def init_db(self):
        data = CSVFileReader.read_file()
        if self.dbconn:
            with self.dbconn:
                for each_data in data:
                    try:
                        cursor = self.dbconn.cursor()
                        query = "insert into lead_details(full_name,name2,name3,a1,a2,tel,fax,email,web,last_update) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (pymysql.escape_string(each_data.get('full_name')),pymysql.escape_string(each_data.get('name2')),pymysql.escape_string(each_data.get('name3')),pymysql.escape_string(each_data.get('address1')),pymysql.escape_string(each_data.get('address2')),pymysql.escape_string(each_data.get('tel')),pymysql.escape_string(each_data.get('fax')),pymysql.escape_string(each_data.get('email')),pymysql.escape_string(each_data.get('web')),str(datetime.now()))
                        cursor.execute(query)
                        cursor.close()
                    except Exception,msg:
                        print 'Exception Occured Inside init_db'
                        print msg
                        print each_data

    def update_last_state(self,lead_id):
        if self.dbconn:
            with self.dbconn:
                query = 'delete from last_crawled_state'
                cursor = self.dbconn.cursor()
                cursor.execute(query)
                query = 'insert into last_crawled_state(lead_id) values(%s)' % str(lead_id)
                cursor.execute(query)
                cursor.close()

    def update_lead_info(self,lead_info_row):
        if self.dbconn:
            with self.dbconn:
                query = ''
                try:
                    cursor = self.dbconn.cursor()
                    query = "update lead_details set full_name='%s',name2='%s',name3='%s',a1='%s',a2='%s',tel='%s',fax='%s',email='%s',web='%s',last_update='%s' where id=%s" % (urllib2.quote(lead_info_row[1].encode('utf8')),urllib2.quote(lead_info_row[2].encode('utf8')),urllib2.quote(lead_info_row[3].encode('utf8')),urllib2.quote(lead_info_row[4].encode('utf8')),urllib2.quote(lead_info_row[5].encode('utf8')),lead_info_row[6],lead_info_row[7],lead_info_row[8],lead_info_row[9],datetime.now(),str(lead_info_row[0]))
                    cursor.execute(query)
                    cursor.close()
                except Exception,msg:
                    print 'Exception Occured Inside Update Lead Info'
                    print msg
                    print query

    def read_last_state(self):
        if self.dbconn:
            query = 'select * from last_crawled_state'
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            cursor.close()
            return data

    def read_lead_info(self,start=0,count=20):
        results = []
        if self.dbconn:
            #last_state = self.read_last_state()
            #start = 0
            #if last_state:
            #    start = last_state[0]
            query = 'select * from lead_details order by id limit %s,%s' % (str(start),str(start+count))
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results += [row]
            cursor.close()
        return results

    def read_info_page_not_fetched(self,start=0,count=20):
        results = []
        if self.dbconn:
            #last_state = self.read_last_state()
            #start = 0
            #if last_state:
            #    start = last_state[0]
            query = 'select * from lead_details where page_fetched=0 order by id limit %s,%s' % (str(start),str(start+count))
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results += [row]
            cursor.close()
        return results

    def read_lead_info_all(self):
        results = []
        if self.dbconn:
            #last_state = self.read_last_state()
            #start = 0
            #if last_state:
            #    start = last_state[0]
            query = 'select * from lead_details order by id'
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results += [row]
            cursor.close()
        return results

    def save_page_content(self,content_row):
        if self.dbconn:
            try:
                with self.dbconn:
                    query = "insert into page_content(content_text,content_html,lead_id) values('%s','%s',%s)" % (urllib2.quote(content_row[1]),urllib2.quote(content_row[2]),str(content_row[3]))
                    cursor = self.dbconn.cursor()
                    cursor.execute(query)
                    cursor.close()
            except Exception,msg:
                print 'Exception Occured Inside save_page_content() method'
                print 'Exception Message: '
                print msg
                print 'Exception Message Print Done.'

    def save_last_page_fetched_state(self,lead_id):
        if self.dbconn:
            with self.dbconn:
                query = 'delete from last_url_fetched'
                cursor = self.dbconn.cursor()
                cursor.execute(query)
                query = 'insert into last_url_fetched(lead_id) values(%s)' % str(lead_id)
                cursor.execute(query)
                cursor.close()

    def read_last_page_fetched_state(self):
        if self.dbconn:
            query = 'select * from last_url_fetched'
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            cursor.close()
            return data
    def mark_lead_as_read(self,lead_id):
        if self.dbconn:
            query = 'update lead_details set page_fetched=1 where id=%s' % str(lead_id)
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            cursor.close()

    def read_page_contents(self,start=0,limit=999999999999):
        results = []
        if self.dbconn:
            query = 'select * from page_content limit %s,%s' % (str(start),str(limit))
            cursor = self.dbconn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                results += [row]
            cursor.close()
        return results

    def reset_db(self):
        if self.dbconn:
            try:
                with self.dbconn:
                    query = 'delete from lead_details;delete from last_crawled_state;alter table lead_details auto_increment=1;delete from last_url_fetched;delete from page_content;alter table page_content auto_increment=1;'
                    cursor = self.dbconn.cursor()
                    cursor.execute(query)
                    cursor.close()
            except Exception,msg:
                print 'Exception Inside reset_db();'
                print msg
                pass

    def close(self):
        if self.dbconn:
            self.dbconn.close()

#DBWraper()