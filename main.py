from microbit import *
import os
import sys 
import math

Bool_cmd = True
users = [ ]
logs =[ ]
current_state = ""
current_user = ""
current_time = 0
disarm_time=0
time_arm = 1
code_pin = ""


# PIN_function:
def call_pin():
    nbr = 0
    display.show(str(nbr))
    pin = [ ]
    while len(pin) < 4:
        code_pin = ""
        if button_a.is_pressed():
            nbr += 1
            if nbr == 10:
                nbr = 0
            display.show(str(nbr))
            sleep(300)
        if button_b.is_pressed():
            nbr += 0 - 1
            if nbr == -1:
                nbr = 9
            display.show(str(nbr))
            sleep(300)
        if pin_logo.is_touched():
            pin.append(nbr)
            for index in pin:
                code_pin = "" + code_pin + ("" + str(index))
                sleep(300) 
            #print(code_pin)
            #display.show(code_pin)

# display_time_function:
def display_time():
    time=current_time
    hour=int(time/3600000)
    min=int(time%3600000)/60000
    if min < 10 and hour < 10:
        texte='0'+ str(hours) +':'+'0'+ str(minutes)
    if min >= 10 and hour < 10:
        texte='0'+ str(hours) +':'+ str(minutes)
    if min < 10 and hour >= 10:
        texte=str(hours) +':'+'0'+ str(minutes)
    if min >= 10 and hour >= 10:
        texte=str(hours) +':'+ str(minutes)

    return texte

# runningtime_update:
files = os.listdir()
if "r_timt_save.txt" in files:
    f1=open("r_timt_save.txt","r")
    RT_read=f1.read()
    #print(RT_read)
    current_time = int(RT_read) + running_time()*60000
    f1.close()


while True:
    #print(args)
    a = uart.read()
    if a != None:
        while True :
            instr=input("alarm cmd> ")
            args=instr.split()

            # exit:
            if args[0] == "exit":
                if len(args) == 1:
                    break
                else:
                    print("Invalid command.")

            # add:
            if args[1] == "add":
                if len(args[3]) != 4:
                        print("Could not save profile. Invalid pin.")
                        continue
                if len(users) == 0:
                    users.append(args[2])
                    users.append(args[3])
                elif len(users)!=0 :
                    user_bool = 0
                    if len(users) >= 0 and len(users) <= 3:
                        for i in range(0,len(users)):
                            if users[i] == args[2]:
                                user_bool=1
                                users[i+1] = args[3]
                                break
                        if user_bool == 0:
                            users.append(args[2])
                            users.append(args[3])
                    elif len(users) >= 6:
                        user1_bool = 0
                        for i in range(0,len(users)):
                            if users[i] == args[2]:
                                user1_bool=1
                                users[i+1] = args[3]
                                break
                        if user1_bool == 0:
                            print("Could not save profile. Limit exceeded.")
            # delete:               
            if args[1] == "delete":
                user_bool=0
                for i in range(0,len(users)):
                    if users[i] == args[2]:
                        user_bool=1
                        users.pop(i)
                        users.pop(i)
                        break
                if user_bool == 0:
                    print("Could not delete profile. Profile "+args[2]+" does not exist.")
            
            # time:
            if args[0] == "arm" and args[1] == "time":
                time_arm = args[2] 

            # read && delete:
            if args[0] == "log":
                if args[1] == "print": 
                    f=open("logs.txt","r")
                    logs_read=f.read()
                    print(logs_read)
                    f.close()
                if args[1] == "delete":
                    os.remove("logs.txt")
                    print("Logs deleted.")
    
    #arm && desarm:
    if button_a.is_pressed() and button_b.is_pressed():
        if len(logs) == 0:
            call_pin()
            face_bool=False
            for i in range(1,len(users),2):
                if str(code_pin) == str(users[i]):
                    face_bool=True
                    current_user=users[i-1]
            if face_bool == True:
                display.show(Image.SMILE)
                current_time=  current_time + running_time()*60000
                current_state="armed"
                disarm_time=current_time
                logs.append(str(current_time))
                logs.append(current_user)
                logs.append(current_state)
                #time_display
                temps=display_time()
                text=temps+" "+current_user+" "+current_state+" the system."
                Nf=open("logs.txt", 'w')
                Nf.write(text)
                Nf.close  
                #print(temps+" "+current_user+" "+current_state+" the system.")
            else:
                display.show(Image.SAD)
        else:
            if current_state == "armed":
                call_pin()
                face_bool=False
                for i in range(1,len(users),2):
                    if code_pin == users[i]:
                        print("true")
                        face_bool=True
                if face_bool == True:
                    display.show(Image.SMILE)
                    sleep(3000)
                    display.clear()
                    current_time= current_time + running_time()*60000
                    current_state= "disarmed"
                    logs.append(str(current_time))
                    logs.append(current_user)
                    logs.append(current_state)
                    #time_display
                    temps=display_time()
                    text=temps+" "+current_user+" "+current_state+" the system."
                    Nf=open("logs.txt", 'w')
                    Nf.write(text)
                    Nf.close  
                    #print(temps+" "+current_user+" "+current_state+" the system.")
                    current_user=""
                else:
                    display.show(Image.SAD)
                    sleep(3000)
                    display.clear()
            elif current_state == "disarmed":
                call_pin()
                face_bool=False
                for i in range(1,len(users),2):
                    if code_pin == users[i]:
                        face_bool=True
                        current_user=users[i-1]
                if face_bool == True:
                    display.show(Image.SMILE)
                    current_time=  current_time + running_time()*60000
                    current_state="armed"
                    disarm_time=current_time
                    logs.append(str(current_time))
                    logs.append(current_user)
                    logs.append(current_state)
                    #time_display
                    temps=display_time()
                    text=temps+" "+current_user+" "+current_state+" the system."
                    Nf=open("logs.txt", 'w')
                    Nf.write(text)
                    Nf.close  
                    #print(temps+" "+current_user+" "+current_state+" the system.")
                else:
                    display.show(Image.SAD)
    
    # disarm automatic:
    if disarm_time - running_time()*60000 == time_arm:
        display.show(Image.DUCK)
        sleep(3000)
        display.clear()
        current_time= current_time + running_time()*60000
        current_state= "disarmed"
        logs.append(str(current_time))
        logs.append(current_state)
        #time_display
        temps=display_time()
        text=temps+" Automatic disarmed system."
        Nf=open("logs.txt", 'w')
        Nf.write(text)
        Nf.close  
        #print(temps+" Automatic disarmed system.")
        current_user=""

    # alarm:
    if accelerometer.current_gesture() == "shake":
        sleep(2000)
        if current_state == "armed":
            while current_state == "armed":
                music.play(music.NYAN)
                display.show(Image(
                "99999:"
                "99999:"
                "99999:"
                "99999:"    
                "99999:"))
                sleep(1000)
                display.show(Image(
                "00000:"
                "00000:"
                "00000:"
                "00000:"    
                "00000:"))

    # save time:
    if running_time()%60000==0:
        # runningtime save:
        rt=open("r_timt_save.txt", 'w')
        text=str(running_time()*60000)
        rt.write(text)
        rt.close
                
    #print(users)
