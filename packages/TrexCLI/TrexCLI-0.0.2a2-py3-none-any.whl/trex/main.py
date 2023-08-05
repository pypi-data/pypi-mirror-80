import argparse 
import requests
from getpass import getpass

authService = 'https://authmservice.herokuapp.com/account/'
authLoginService = authService + 'account/login'

def userExists(username):
    r = requests.get(authService + username)
    if (r.status_code == 200): return True
    return False

def printGreetingMessage():
    print ('=' * 40)
    print("Welcome to the TReX CLI !!\n" \
          "Please continue to Login: ") 
    print ('=' * 40)

def getUserPass():
    username = input("Username: ") 
    password = getpass()
    return username, password

def authenticate(username, password):
    r = requests.post(authLoginService, data ={'username': username,
                                          'password': password})
    if (r.status_code == 201): return True
    return False

def signup(username, password):
    email = input ('Email: ')
    r = requests.post(authService, data ={'username': username,
                                                'password': password,
                                                'email'   : email})
    if (r.status_code == 201): return True
    return False


def main(): 
    printGreetingMessage()
    username, password = getUserPass()
    if not authenticate(username, password):
        print ("Please check your username/password!\n" \
               "You are making Trex angry!")
        isSignup = input ('Do you want to Sign up? (y/n): ').lower() == 'y'
        if not isSignup: exit(1)
        elif userExists(username): 
            print ('Trex will eat you up! There\'s a user already with this name!')
            exit(1)
        signup(username, password)


    while True:
        command = input ('>>> ')
        if command == 'username': print (username)
        if command == 'exit': exit(1)

if __name__ == "__main__":
    main()
