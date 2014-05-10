# - * - coding: UTF-8 - * -

f = open('KeyWords_v002.csv','r')
c = f.read()
unic = c.decode('utf_8','ignore')
print unic.encode('utf_8','ignore')
f.close()