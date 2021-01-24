'''
# h = 16
# z = 15

# msg = f'16              MAGSUDMIRZAZADAzzz'
# print(msg[:16])
# print(msg[16:(h+z)])

HEADERSIZE = 16

lens = "100000000000000"
msg = "MagsudMirzazada"
final = lens + ' '*(HEADERSIZE - len(lens)) + msg

print(final)
print(len(final))
'''
#======#

''' THREADING
import threading
import time

def func(x, y):
    time.sleep(5)
    return x*y

def func1(x, y):
    time.sleep(10)
    return x*y

thread = threading.Thread(target=func, args= (3, 5))
thread.start()

thread = threading.Thread(target=func1, args= (2, 5))
thread.start()


print(f'{threading.enumerate()} \n') #list of active threads
#print(f'{threading.main_thread()} \n') #showing main thread (thread in which whole python file works)
print(f'{threading.active_count()} \n')
#print(f'{threading.current_thread()} \n') #önemsiz
#print(f'{threading.get_ident()} \n')
#print(f'{threading.get_native_id()} \n')
'''
#=====#
''' BeautifulSoup
import requests
from bs4 import BeautifulSoup

url = requests.get("https://www.google.com/?client=safari").content
soup = BeautifulSoup(url, 'html.parser')
soup.prettify()

# print(soup.a['href'], soup.a.attrs['href'])  same things
# print(soup.a.string, soup.a.text)  same things
# print(soup.a, soup.a.name)
# print(soup.title.text)
# print(soup.div.div.nobr.prettify())
# print(soup.p)
# print(soup.find_all('a'))
# print(soup.a.attrs) #Shows all of the attribute given tag has
# soup.a.string.raplace_with("New string")  #replaces the content of string
'''
#=====#
''' REQUESTS
import requests
# HTTP Requests types: GET, POST, PUT, DELETE, HEAD, OPTIONS

# headers = {'': ''}

# req = requests.get('https://www.google.com/?client=safari')

payload = {'username': 'magsud', 'password': 'test'}
req = requests.get('https://httpbin.org/', data=payload, params={'lang': 'ru'})
print(req.text)

#req.content - raw bytes of response payload
#req.text - string or unicode format of response

# print(dir(req))
# print(req) #actually, shows status
# print(req.status_code)
# print(req.encoding)
# print(req.json())
# print(req.url) # returns url
print(req.headers, '\n')
'''
#=====#
''' FlaskRstful.py
import requests
from termcolor import colored

BASE = 'http://127.0.0.1:5000/'

# data = [
#     {"likes": 45000, "name": "FLASK", "views": 100000},
#     {"likes": 32000, "name": "RESTful", "views": 100000},
#     {"likes": 34000, "name": "SQL", "views": 100000}
# ]

# for i in range(len(data)):
#     res = requests.put(BASE + "video/" + str(i), data[i])
#     print(res.json())

res = requests.patch(BASE + "video/2", {"views": 70000, "likes": 80000, "name": "NoSQL"})
# res = requests.get(BASE + "video/6")
print(colored(res.json(), 'green'))
'''
''' NOTEs
fullUrl = 'google.com/account/'
url = 'https://' + fullUrl#\
                #fullUrl.split('//')[len(fullUrl.split('//')) - 1]
print(url)
'''
#=====#
'''
data = {
    "model_name": "M8",
    "company": "BMW",
    "vehicle_type": "Sedan",
    "transmission": "8-speed Automatic",
    "introduction_date": "2019"
}

import requests

BASE = 'http://127.0.0.1:5000/'
res = requests.post(BASE + "/car/1", data)
res1 = requests.get(BASE + "car/1")
print(res1.json())
'''


msg = 'zz'
data = f"short" + msg
print(data)