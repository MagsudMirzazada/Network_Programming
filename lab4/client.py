import requests

BASE = 'http://127.0.0.1:5000/flights'

class User:
    def __init__(self):
        self.token = None
        self.usrname = None
        self.password = None

    def get(self):
        res = requests.get(BASE)
        return res
        
    def post(self):
        pass
    def AUT_A(self):
        self.username = input('Admin Username: ')
        self.password = input('Admin password: ')
        res = requests.get(BASE + '/authentication_authorization',
                    {'username': self.username, 'password': self.password})
        return res
    def end_session(self):
        pass

def main():
    user = User()
    user.AUT_A()

if __name__ == '__main__':
    main()