import tkinter as tk
import tkinter.font as fnt
import random
import string
from twilio.rest import Client
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

#for text message stuffs
account_sid = "ACa9d8176a3a0f06c1f1529b978ab105d2"
auth_token = "6e8f2b1d48280ab9ba624b99ad8c7668"

twilio_num = "+18556592189"
target_num = "+12144498784"



class PasswordApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password App")
        self.master.geometry("500x300")
        
        self.home_screen()

        self.random_passwords = []
        self.names = []
    
    #sets the first screen that the delivery person sees and where the owner would type in the password
    def home_screen(self):
        self.clear_screen()
        
        self.label1 = tk.Label(self.master, font = fnt.Font(size = 36),text="Enter Password:")
        self.label1.pack()
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.master, font = fnt.Font(size = 36),textvariable=self.password_var, show="")
        self.password_entry.pack()
        self.create_number_keyboard()
        self.password_entry.bind("<KeyRelease-asterisk>", self.show_new_password_screen)

    #creates the screen that only the owner can access with the correct password, calles all the other functions for buttons, ect
    def show_new_password_screen(self, password):
        if password == "1234":
            self.clear_screen()
            self.master.geometry("500x300")
            
            self.label2 = tk.Label(self.master, font = fnt.Font(size = 36),text="Enter Name:")
            self.label2.pack()
            
            self.name_var = tk.StringVar()
            self.name_entry = tk.Entry(self.master, font = fnt.Font(size = 36),textvariable=self.name_var)
            self.name_entry.pack()
            
            self.create_letter_keyboard()

            self.button = tk.Button(root, font = fnt.Font(size = 25), text="Generate Random Number", command=self.random_pass)
            self.button.pack()

            self.label = tk.Label(root, text="")
            self.label.pack()

            self.name_entry.bind("<KeyRelease-asterisk>", self.home_screen)
            

    #creates the keyboard with numbers for the package delivery people to use
    def create_number_keyboard(self):
        keyboard_frame = tk.Frame(self.master)
        keyboard_frame.pack()
        for i in range(1, 10):
            button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text=str(i), width=10, height=2, command=lambda x=i: self.add_to_password(x))
            button.grid(row=(i-1)//3, column=(i-1)%3)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text="0", width=10, height=2, command=lambda x=0: self.add_to_password(x))
        button.grid(row=3, column=1)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text="Owner", width=10, height=2, command=lambda: self.show_new_password_screen(self.password_var.get()))
        button.grid(row=3, column=0)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text="Clear", width=10, height=2, command=self.clear_password)
        button.grid(row=3, column=2)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text="Enter", width=10, height=2, command=self.enter_password)
        button.grid(row = 4, column = 1)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text="Lock", width=10, height=2, command=self.lock_box)
        button.grid(row = 4, column = 2)

    #creates the keyboard with letters for the owner to use
    def create_letter_keyboard(self):
        keyboard_frame = tk.Frame(self.master)
        keyboard_frame.pack()
        letters = string.ascii_lowercase
        for i in range(26):
            button = tk.Button(keyboard_frame, font = fnt.Font(size = 36),text=letters[i], width=8, height=1, command=lambda x=letters[i]: self.add_to_name(x))
            button.grid(row=i//6, column=i%6)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36), text="Enter", width = 8, height = 2, command=self.names.append(self.name_var.get()))
        button.grid(row = 5, column=1)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36), text="Clear", width=8, height=2, command=self.clear_name)
        button.grid(row=5, column=3)
        button = tk.Button(keyboard_frame, font = fnt.Font(size = 36), text="Home", width=8, height=2, command=lambda x="Home": self.home_screen())#(x)
        button.grid(row=5, column=2)
        
    #function for when people click numbers, adds to where you can see it
    def add_to_password(self, digit):
        self.password_var.set(self.password_var.get() + str(digit))
        
    #function for clear button (main)
    def clear_password(self):
        self.password_var.set("")

    #function for clear button (owner)
    def clear_name(self):
        self.name_var.set("")

    #function for "enter" button
    def add_to_name(self, letter):
        self.name_var.set(self.name_var.get() + letter)
    
    #function for lock button
    def lock_box(self):
        print("locking!")
        
        #engineering way of locking the hook
        factory = PiGPIOFactory()
        servo = Servo(12, min_pulse_width=.5/1000, max_pulse_width= 2.5/1000, pin_factory=factory)
        #locked position
        servo.mid()
        sleep(2)
    
        servo.min()
        sleep(.28)
    
        servo.mid()
        sleep(2)
        servo.value = None
        
        
    #what happens when someone enters a number
    def enter_password(self):
        factory = PiGPIOFactory()
        servo = Servo(12, min_pulse_width=.5/1000, max_pulse_width= 2.5/1000, pin_factory=factory)
        for name in self.names:
            #running through the passwords and seeing which one matches with the one inputted
            if self.password_var.get() == str(self.random_passwords[self.names.index(name)]):
                print("unlocking")
                
                #all of the servo parts is the engineering way of turning the hook to unlock it
                servo.mid()
                sleep(2)
        
                servo.max()
                sleep(.275)
        
                servo.mid()
                sleep(2)
                servo.value = None

                #sends the text message abt delivery
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body= "your hat has been delivered!",
                    from_= twilio_num,
                    to= target_num
                )
                
                
    #creating the random password when button pressed, then adds to list of passwords
    def random_pass(self):
        random_num = random.randint(1000,9999)
        self.random_passwords.append(str(random_num))
        self.label.config(font = fnt.Font(size = 36), width = 8, height = 2, text = str(random_num))
    
    #clears the screen completely    
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

#runs the main function
root = tk.Tk()
app = PasswordApp(root)
root.attributes('-fullscreen', True)
root.bind("<Escape>", lambda e:root.quit())
root.mainloop()
