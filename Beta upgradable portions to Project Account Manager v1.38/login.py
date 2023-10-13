import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import subprocess
import getpass
import ctypes
import random


conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS register (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               gender TEXT,
               birth_year INTEGER,
               birth_month TEXT,
               birth_day INTEGER,
               email TEXT,
               username TEXT UNIQUE,
               password TEXT,
               event_by_admin TEXT,
               register_date TEXT
)
""")
conn.commit()
cursor.execute("""CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            username TEXT,
            email TEXT,
            event_by_admin TEXT,
            login_date TEXT
)
""")
conn.commit()

try:
    cursor.execute("DELETE FROM captcha")
    conn.commit()
except sqlite3.OperationalError:
    pass

def login():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    username = username_entry_2.get()
    password = password_entry_2.get()
    capt1 = c_entry1.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Both fields must be filled in!")
        return
    
    if capt1 == "":
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        messagebox.showerror("Captcha", "You also have to click the captcha button!\nThen you can fill the captcha field and continue!")
        return

    capt = str(1)
    cursor.execute("SELECT captcha FROM captcha")
    captcha = cursor.fetchone()
    if captcha is None:
        captcha = str(captcha)
    else:
        captcha = list(captcha)
        for capt in captcha:
            capt = str(capt)
    c_entry1.delete(0, tk.END)

    def check_user():
        try:
            try:
                try:
                    conn = sqlite3.connect("accounts.db")
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM login_logs WHERE username=?", (username,))
                    Ids = cursor.fetchall()
                    if Ids is None:
                        Ids = str(Ids)
                    ids = max(Ids)
                    for Id in ids:
                        Id = int(Id)
                    cursor.execute("SELECT login_date FROM login_logs WHERE username=? AND id=?", (username, Id))
                    login_date = cursor.fetchone()
                    if login_date is None:
                        login_date = str(login_date)
                    else:
                        for date in login_date:
                            date = str(date)
                    date = date[:19]
                    datetime_date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                    current_datetime = datetime.datetime.now()
                    time_delta = current_datetime - datetime_date
                    time_delta = str(time_delta)
                    if time_delta[0] == "-":
                        ask = messagebox.askyesno("Faulty Timezone", "We have detected that your system's datetime is not well-adjusted to your network timezone!\nAre you sure your timezone is adjusted accordingly to your network?\n\n<<Apart from answering to this, Please also note that we're asking this to urge you to check your system's timezone and adjust it as it deems it necessary | You may also want to ignore this as you wish!>>")
                        if ask:
                            pass
                        else:
                            return "0"
                    if "days" in time_delta:
                        return
                    if time_delta[1] != ":":
                        if time_delta[0:2] == "00":
                            pass
                        else:
                            return
                    else:
                        if time_delta[0] == "0":
                            pass
                        else:
                            return
                    start_index = int(0)
                    dot_index_end = time_delta.index(".")
                    sliced_delta = time_delta[start_index:dot_index_end]
                    rest = sliced_delta[sliced_delta.index(":")+1:]
                    minutes = int(sliced_delta[sliced_delta.index(":")+1:rest.index(":")+sliced_delta.index(":")+1])
                    random_set = list(set([rand for rand in range(15,31)]))
                    rand = int(random.choice(random_set))

                    if minutes < rand:
                        messagebox.showerror("Flood Detected", f"Please wait for {rand-minutes} minute(s)!\nAlso note that the duration in which you must wait can vary in your next try.\n\nIt's best to wait an hour after each successful login attempt from the current network/system/OS/account!")
                        return "0"
                except(ValueError , TypeError):
                    pass
            except UnboundLocalError:
                pass
        except sqlite3.OperationalError:
            pass
    if check_user() == "0":
        return
    else:
        pass

    if capt == capt1:
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        pass
    else:
        messagebox.showerror("Captcha Error", "Wrong answer inputted! Please press the captcha button and type it down in the appropriate entry field and try submitting again!\n\nPlease also note that the captcha could have been revoked too!\nHence, try regenerating another one using the button below!")
        cursor.execute("DELETE FROM captcha")
        conn.commit()
        return
    try:
        cursor.execute("SELECT password FROM register WHERE username=?", (username,))
        correct_password = cursor.fetchone()
        if correct_password is None:
            correct_password = str(correct_password)
        else:
            correct_password = list(correct_password)
            for i in correct_password:
                i = str(i)
        try:
            if i == str(password):
                # username_entry_2.delete(0, tk.END)
                password_entry_2.delete(0, tk.END)
                confirm = messagebox.askyesno("Success", "You have been successfully authenticated!\n\n__EXIT THE AUTHENTICATOR AND OPEN THE LIBRARY REGISTRY APP?__")
                if confirm:

                    cursor.execute("SELECT name FROM register WHERE username=?", (username,))
                    name = cursor.fetchone()
                    if name is None:
                        name = str(name)
                    else:
                        name = list(name)
                        for j in name:
                            j = str(j)

                    cursor.execute("SELECT email FROM register WHERE username=?", (username,))
                    email = cursor.fetchone()
                    if email is None:
                        email = str(email)
                    else:
                        email = list(email)
                        for mail in email:
                            mail = str(mail)

                    conn = sqlite3.connect("accounts.db")
                    cursor = conn.cursor()
                    cursor.execute("""CREATE TABLE IF NOT EXISTS login_logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                username TEXT,
                                email TEXT,
                                event_by_admin TEXT,
                                login_date TEXT
                    )
                    """)
                    conn.commit()
                    current_username = getpass.getuser()
                    event_by_admin = current_username
                    cursor.execute("INSERT INTO login_logs (name, username, email, event_by_admin, login_date) VALUES (?, ?, ?, ?, ?)", (j, username, mail, event_by_admin, datetime.datetime.now()))
                    conn.commit()
                    conn.close()

                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    
                    messagebox.showinfo("READ ON TO THE END!", "The window you are now being redirected to, is just a Legacy portion from our previous project 'LIBRARY MANAGEMENT SYSTEM V2.74' & solely aims to outline the fact for anyone using this project that they can modify it with ease and replace this with any other sorta tasks like a 'Banking App' or an 'Email Management App' or anything else.\n\nOur modern user-authenticator tkinter project is made with love to help anyone when it comes down to handling user security, user account management and some database works that may at first seem tough to pull off the whole management work manually & personally!, and to illustrate that this open-source project can facilitate in handling all such hassle and further remove the burden of user management chore.\n\nThis part of code has been commented in the main codebase just inside login.py python file which can be further customized depending upon your own piece or pieces of work!\n\nDON'T FORGET TO ALWAYS INCLUDE THE LICENSE AS YOU USE THIS PROJECT AND SUPPORT US ON GITHUB!\n\nGOOD LUCK:)")
                    subprocess.Popen(['python', 'Library_Registry/Registry.py']) #You can modify the address to which user will be redirected!

                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    ################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
                    
                    window.destroy()
                else:
                    return
            else:
                messagebox.showerror("Authetnication Error", "Wrong Credentials provided including the username and password!")
        except UnboundLocalError:
            messagebox.showerror("Invalid Username", "User doesn't exist in the local database!")
            conn.close()
            return
    except sqlite3.OperationalError:
        messagebox.showinfo("Fresh/Empty", "The database is fresh and empty!\nNobody has registered themselves yet!\n\nYou can be the first one though by firing the REGISTER button on the left hand side!")
        return

show_it = "no"
def show_entry_text():
    global show_it
    if show_it != "yes":
        password_entry_2.configure(show="")
        show_pass_button.configure(text="Hide", bg="#333333", fg="white")
        show_it = "yes"
    elif show_it == "yes":
        password_entry_2.configure(show="*")
        show_pass_button.configure(text="Show", bg="red", fg="yellow")
        show_it = "no"

def go_to_register():
    confirm = messagebox.askyesno("Confirmation", "Go to the register window?")
    if confirm:
        subprocess.Popen(['python', 'register.py'])
        conn.close()
        window.destroy()
    else:
        return

def exit_button():
    confirm = messagebox.askyesno("Confirmation", "SURE TO EXIT THE AUTHENTICATOR?")
    if confirm:
        conn.close()
        window.destroy()
        exit()
    else:
        return

lightness = "bright"
def dark_bright():
    global lightness
    if lightness == "bright":
        window.configure(bg="#333333")
        login_frame.configure(bg="#333333")
        hyphen_label.configure(bg="#333333")
        username_entry_2.configure(bg="lightblue")
        password_entry_2.configure(bg="#bbbbbb")
        caps_lock_label_left.configure(bg="#333333")
        caps_lock_label_right.configure(bg="#333333")
        brightness_button_left.configure(bg="orange", fg="darkgreen", text="Light ", width=3, font="arial 7 bold")
        brightness_button_right.configure(bg="orange", fg="darkgreen", text="Light ", width=3, font="arial 7 bold")
        captcha_label1.configure(bg="#333333")
        brightness_button_left.place(relx=0.022, rely=0.97, anchor=tk.N)
        brightness_button_right.place(relx=0.975, rely=0.97, anchor=tk.N)
        lightness = "dark"
    elif lightness == "dark":
        window.configure(bg="green")
        login_frame.configure(bg="green")
        hyphen_label.configure(bg="green")
        username_entry_2.configure(bg="white")
        password_entry_2.configure(bg="#dddddd")
        caps_lock_label_left.configure(bg="green")
        caps_lock_label_right.configure(bg="green")
        brightness_button_left.configure(bg="#333333", fg="orange", text="Dark", width=3, font="arial 7 bold")
        brightness_button_right.configure(bg="#333333", fg="orange", text="Dark", width=3, font="arial 7 bold")
        captcha_label1.configure(bg="green")
        brightness_button_left.place(relx=0.022, rely=0.97, anchor=tk.N)
        brightness_button_right.place(relx=0.975, rely=0.97, anchor=tk.N)
        lightness = "bright"

def check_caps_lock():
    keyboard_state = ctypes.windll.user32.GetKeyState(0x14)
    caps_lock_state = keyboard_state & 0x0001 != 0
    
    if caps_lock_state:
        caps_lock_label_left.configure(fg="red", text="CapsLock On!")
        caps_lock_label_right.configure(fg="red", text="CapsLock On!")
    else:
        caps_lock_label_left.configure(fg="green", text="")
        caps_lock_label_right.configure(fg="green", text="")
    window.after(1000, check_caps_lock)

def generate_captcha():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS captcha (captcha TEXT)""")
    conn.commit()
    cursor.execute("DELETE FROM captcha")
    conn.commit()
    captcha_text = ""
    for _ in range(12):
        captcha_text += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=|/><,.?':;~0123456789")
    cursor.execute("INSERT INTO captcha (captcha) VALUES (?)", (captcha_text,))
    conn.commit()
    try:
        captcha_label1.config(text=captcha_text)
    except NameError:
        pass

window = tk.Tk()
window.configure(bg="green")
window.geometry("570x640")
window.resizable(False, False)
window.title("Login")

login_frame = tk.Frame(window)
login_frame.configure(bg="green")
login_frame.place(relx=0.5, rely=0.004, anchor=tk.N)

main_label_2 = tk.Label(login_frame, text="Login ", bg="orange", font="impact 18 italic")
username_label_2 = tk.Label(login_frame, text="Enter your Username: ", font="arial 15 bold", bg="yellow")
username_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
password_label_2 = tk.Label(login_frame, text="Enter your Password: ", font="arial 15 bold", bg="yellow")
password_entry_2 = tk.Entry(login_frame, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*", bg="#dddddd")
submit_button2 = tk.Button(window, text="Login! - >", command=login, font="arial 15 bold", bg="blue", fg="yellow", relief="raised")
quit_button = tk.Button(window, text="QUIT ", font="lotus 9 italic", bg="red", fg="darkblue", command=exit_button, relief="ridge")
go_to_register_button = tk.Button(window, text="REGISTER", command=go_to_register, font="arial 15 italic", bg="darkblue", fg="yellow", relief="ridge")
hyphen_label = tk.Label(window, text="|  |", font="arial 15 bold", bg="green", fg="orange")
show_pass_button = tk.Button(window, text="Show", command=show_entry_text, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button.place(relx=0.92, rely=0.35, anchor=tk.N)

brightness_button_left = tk.Button(window, text="Dark", bg="#333333", fg="orange", font="arial 7 bold", width="3", relief="groove", command=dark_bright)
brightness_button_right = tk.Button(window, text="Dark", bg="#333333", fg="orange", font="arial 7 bold", width="3", relief="groove", command=dark_bright)
brightness_button_left.place(relx=0.022, rely=0.97, anchor=tk.N)
brightness_button_right.place(relx=0.975, rely=0.97, anchor=tk.N)

caps_lock_label_left = tk.Label(window, text="", bg="green", fg="green", font="arial 10 bold", height=1, width=11)
caps_lock_label_right = tk.Label(window, text="", bg="green", fg="green", font="arial 10 bold", height=1, width=11)
caps_lock_label_left.place(relx=0.18, rely=0.282, anchor=tk.N)
caps_lock_label_right.place(relx=0.82, rely=0.282, anchor=tk.N)
check_caps_lock()

c_label1 = tk.Label(login_frame, text="Solve the Captcha: ", bg="orange", fg="black", font="arial 15 bold", width=33)
c_entry1 = tk.Entry(login_frame, fg="blue", bg="lightblue", font="arial 18 italic", justify="center", width=23)
captcha_label1 = tk.Label(login_frame, font=("segoe script", 23), width=16, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=1)
generate_button1 = tk.Button(login_frame, text="Generate Another!\n&\ninput below:", width=30, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")

main_label_2.pack(pady=18)
username_label_2.pack(pady=10)
username_entry_2.pack(pady=5)
password_label_2.pack(pady=10)
password_entry_2.pack(pady=5)
c_label1.pack(pady=20)
captcha_label1.pack(pady=5)
generate_button1.pack(pady=15)
c_entry1.pack(pady=5)

submit_button2.place(relx=0.647, rely=0.85, anchor=tk.N)
quit_button.place(relx=0.5, rely=0.94, anchor=tk.N)
go_to_register_button.place(relx=0.343, rely=0.85, anchor=tk.N)
hyphen_label.place(relx=0.5, rely=0.86, anchor=tk.N)

window.mainloop()
conn.close()