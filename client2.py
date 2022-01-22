import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import mysql.connector
import _thread
import socket
import sys


class Login_System:
    def __init__(self, root):
        self.root = root

        self.root.title("Login")
        self.root.geometry("1350x700+0+0")
        self.uname = tk.StringVar()
        self.paswd = tk.StringVar()


        # Images
        self.bg = ImageTk.PhotoImage(file="C:/Users/Tejas/PycharmProjects/cnsproj/images/bg.jpg")
        self.user = ImageTk.PhotoImage(file="C:/Users/Tejas/PycharmProjects/cnsproj/images/user.png")
        self.passw = ImageTk.PhotoImage(file="C:/Users/Tejas/PycharmProjects/cnsproj/images/pass.png")
        self.logo = ImageTk.PhotoImage(file="C:/Users/Tejas/PycharmProjects/cnsproj/images/logo.png")

        self.bg_labl = tk.Label(self.root, image=self.bg)
        self.bg_labl.pack()
        self.title = tk.Label(text="LOGIN", font=("Times new roman", 40, "bold"), bg="blue", fg="white", bd=10,
                         relief=GROOVE)
        self.title.place(x=0, y=0, relwidth=1)

        self.login_frame = tk.Frame(self.root, bg="white")
        self.login_frame.place(x=400, y=150)

        logolbl = tk.Label(self.login_frame, image=self.logo, bd=0)
        logolbl.grid(row=0, columnspan=2, pady=20)
        usrlbl = tk.Label(self.login_frame, text="Username:", image=self.user, compound=LEFT,
                          font=("Times new roman", 20, "bold"), bg="white")
        usrlbl.grid(row=1, column=0, padx=20, pady=10)
        usr_entry = tk.Entry(self.login_frame, bd=5, textvariable=self.uname, relief=GROOVE, font=("comic sans", 15))
        usr_entry.grid(row=1, column=1, padx=20, pady=10)

        pwdlbl = tk.Label(self.login_frame, text="Password:", image=self.passw, compound=LEFT,
                          font=("Times new roman", 20, "bold"), bg="white")
        pwdlbl.grid(row=2, column=0, padx=20, pady=10)
        pwd_entry = tk.Entry(self.login_frame, bd=5, relief=GROOVE, textvariable=self.paswd, font=("comic sans", 15))
        pwd_entry.grid(row=2, column=1, padx=20, pady=10)

        btn = tk.Button(self.login_frame, text="Login", command=lambda: self.login(Win2), width=15,
                        font=("times new roman", 12, "bold"), relief=GROOVE, bg="light gray", fg="black")
        btn.grid(row=3, columnspan=2, padx=20, pady=10)

    def login(self, _class):
        mydb = mysql.connector.connect(host="localhost", username="root", password="Root@123", database="cns")
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM login")
        result = cursor.fetchall()
        print(result)
        for i in result:
            if self.uname.get() == i[0] and self.paswd.get() == i[1]:
                messagebox.showinfo("Successful", f"welcome {self.uname.get()}")
                self.login_frame.destroy()
                self.title.destroy()
                self.bg_labl.destroy()

                # use `root` with another class
                self.another = Win2(self.root)
                # self.new = tk.Toplevel(self.root)
                # _class(self.new)
                break
        if self.uname.get() != i[0] or self.paswd.get() != i[1]:
            messagebox.showerror("Error", "Invalid username and password")


class Win2:


    def __init__(self, root):
        self.root = root
        self.root.title("Chat Window")
        self.root.geometry("700x400+0+0")
        frame = tk.Frame(self.root)


        # self.bg1 = ImageTk.PhotoImage(file="C:/Users/Tejas/PycharmProjects/cnsproj/images/bg.jpg")
        # bg_labl1 = tk.Label(self.frame, image=self.bg1)
        # bg_labl1.pack()
        frame.pack()

        txt = tk.Entry(frame, bd=5, relief=GROOVE, font=("comic sans", 15))
        txt['width'] = 50
        txt['relief'] = tk.GROOVE
        txt['bg'] = '#f5f6f7'
        txt['fg'] = 'red'
        txt['font'] = ("Courier", 12)
        txt.grid(column=0, row=1, padx=5, pady=15)
        # Button
        send = tk.Button(frame, text="Send")
        send['relief'] = tk.GROOVE
        send['bg'] = 'red'
        send['fg'] = 'white'
        send['activebackground'] = '#404040'
        send['padx'] = 3
        send['font'] = ("Courier", 10)
        send.grid(column=1, row=1, padx=5, pady=15)

        global i
        i = 3
        global client
        client = 0
        global start
        start = True

        def sendMessage():
            msg = txt.get()
            client.send(msg.encode('ascii'))

        def recievingMessage(c):
            global i
            while True:
                msg = c.recv(2048).decode('ascii')
                if not msg:
                    sys.exit(0)
                global start
                if (start):
                    start = False
                    # tkinter codes starts
                    root.title(msg)
                    continue
                print(msg)
                # output_label = tk.Label(frame, fg="blue")
                # output_label.grid(column=0, row=5, columnspan=3)
                # output_label.config(text=msg)
                msglbl = tk.Label(frame, text=msg)
                msglbl['font'] = ("Courier", 10)
                msglbl['bg'] = 'black'
                msglbl['fg'] = '#0aff43'
                msglbl['width'] = 50
                msglbl.grid(columnspan=8, column=0, row=i, padx=10)
                i += 1

        # Socket Creation
        def socketCreation():
            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            c.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Local Host
            # import all functions /
            #  everthing from chat.py file
            host = '127.0.0.1'
            port = 5000
            c.connect((host, port))
            global client
            client = c
            send['command'] = sendMessage
            _thread.start_new_thread(recievingMessage, (c,))

        _thread.start_new_thread(socketCreation, ())


root = tk.Tk()
obj = Login_System(root)
root.mainloop()