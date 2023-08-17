import sys 
import datetime
import os

args = sys.argv
users = ["yassir","1234","majid","8888","hamid","8999","hamza","9999","babo","2222"]

face_bool=False
code_pin=input("pin: ")
for i in range(1,len(users),2):
    if code_pin == users[i]:
        face_bool=True
        current_user=users[i-1]
if face_bool == True:
    print("true1")



'''
text="yassir 1"
text2="yassir 2"
Nf=open(logs, 'w')
Nf.write(text)
Nf.write(text2)
Nf.close 

f=open("logs",'r')
text8=f.readlines()
print(text8)

'''