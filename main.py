from microbit import *
import os
import sys 
import math

users = {}  
current_time = 0
disarm_time = 0
time_arm = 1

def display_time(milliseconds):
    total_seconds = milliseconds // 1000
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def load_time():
    if "r_time_save.txt" in os.listdir():
        with open("r_time_save.txt", "r") as f:
            return int(f.read())
    return 0

def save_time(time):
    with open("r_time_save.txt", "w") as f:
        f.write(str(time))

def add_user(username, pin):
    if len(pin) == 4:
        users[username] = pin

def delete_user(username):
    if username in users:
        del users[username]

def main():
    global current_time, disarm_time

    current_time = load_time()

    while True:
        uart_data = uart.read()
        if uart_data:
            instr = uart_data.decode("utf-8")
            args = instr.split()

            if args[0] == "exit":
                break

            if args[1] == "add":
                add_user(args[2], args[3])

            if args[1] == "delete":
                delete_user(args[2])

            if args[0] == "arm" and args[1] == "time":
                time_arm = int(args[2])

            if args[0] == "log":
                if args[1] == "print":
                    with open("logs.txt", "r") as f:
                        print(f.read())
                if args[1] == "delete":
                    os.remove("logs.txt")
                    print("Logs deleted.")

        if button_a.is_pressed() and button_b.is_pressed():
            if len(logs) == 0:
                call_pin()
                face_bool = False
                for i in range(1, len(users), 2):
                    if str(code_pin) == str(users[i]):
                        face_bool = True
                        current_user = users[i - 1]
                if face_bool:
                    display.show(Image.SMILE)
                    current_time = current_time + running_time() * 60000
                    current_state = "armed"
                    disarm_time = current_time
                    logs.append(str(current_time))
                    logs.append(current_user)
                    logs.append(current_state)
                    # time_display
                    temps = display_time(current_time)
                    text = f"{temps} {current_user} {current_state} the system."
                    with open("logs.txt", 'w') as Nf:
                        Nf.write(text)
                    current_user = ""
                else:
                    display.show(Image.SAD)
            else:
                if current_state == "armed":
                    call_pin()
                    face_bool = False
                    for i in range(1, len(users), 2):
                        if code_pin == users[i]:
                            print("true")
                            face_bool = True
                    if face_bool:
                        display.show(Image.SMILE)
                        sleep(3000)
                        display.clear()
                        current_time = current_time + running_time() * 60000
                        current_state = "disarmed"
                        logs.append(str(current_time))
                        logs.append(current_user)
                        logs.append(current_state)
                        # time_display
                        temps = display_time(current_time)
                        text = f"{temps} {current_user} {current_state} the system."
                        with open("logs.txt", 'w') as Nf:
                            Nf.write(text)
                        current_user = ""
                    else:
                        display.show(Image.SAD)
                        sleep(3000)
                        display.clear()
                elif current_state == "disarmed":
                    call_pin()
                    face_bool = False
                    for i in range(1, len(users), 2):
                        if code_pin == users[i]:
                            face_bool = True
                            current_user = users[i - 1]
                    if face_bool:
                        display.show(Image.SMILE)
                        current_time = current_time + running_time() * 60000
                        current_state = "armed"
                        disarm_time = current_time
                        logs.append(str(current_time))
                        logs.append(current_user)
                        logs.append(current_state)
                        # time_display
                        temps = display_time(current_time)
                        text = f"{temps} {current_user} {current_state} the system."
                        with open("logs.txt", 'w') as Nf:
                            Nf.write(text)
                        current_user = ""
                    else:
                        display.show(Image.SAD)

        if disarm_time - running_time() * 60000 == time_arm:
            display.show(Image.DUCK)
            sleep(3000)
            display.clear()
            current_time = current_time + running_time() * 60000
            current_state = "disarmed"
            logs.append(str(current_time))
            logs.append(current_state)
            # time_display
            temps = display_time(current_time)
            text = f"{temps} Automatic disarmed system."
            with open("logs.txt", 'w') as Nf:
                Nf.write(text)
            current_user = ""

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

                if running_time() % 60000 == 0:
                    save_time(running_time() * 60000)

if __name__ == "__main__":
    main()

