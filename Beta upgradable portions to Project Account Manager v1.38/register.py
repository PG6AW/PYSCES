import tkinter as tk
from tkinter import messagebox, ttk
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
cursor.execute("""CREATE TABLE IF NOT EXISTS register_logs (
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
)""")
conn.commit()

try:
    cursor.execute("DELETE FROM captcha")
    conn.commit()
except sqlite3.OperationalError:
    pass

def register():
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    name = name_entry.get()
    gender = selected_button.get()
    birth_year = year_menu.get()
    birth_month = month_menu.get()
    birth_day = day_menu.get()
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    confirm_password = confirm_password_entry.get()
    capt1 = c_entry1.get()

    if name == "" or username == "" or password == "" or email == "" or confirm_password == "":
        messagebox.showerror("Error", "All fields must be filled in!")
        return

    if gender == "" or str(gender) == "None" or gender == None:
        messagebox.showerror("Error", "Please choose your gender pronoun!")
        return

    if birth_year == "YEAR":
        messagebox.showerror("Error", "Please select your Year of Birth!")
        return

    if birth_month == "MONTH":
        messagebox.showerror("Error", "Please select your Month of Birth!")
        return

    if birth_day == "DAY":
        messagebox.showerror("Error", "Please select your Day of Birth!")
        return

    invalid_username_chars = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "=", "|", "\\", "{", "}", "[", "]", ":", ";", '"', "'", ">", "<", "/", "?", ",", " "]
    for char in invalid_username_chars:
        if char in username:
            messagebox.showerror("Invalid_Char", "Ambiguous Characters like '#', '@', '!' or even a 'space' & ... except for underscore, are not allowed for use in the Username field!\n\nTry a mix of numbers and regular characters instead.")
            return
        else:
            pass

    try:
        birth_year = int(birth_year)
    except(ValueError , TypeError):
        pass

    try:
        birth_day = int(birth_day)
    except(ValueError , TypeError):
        pass

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
                    cursor.execute("SELECT id FROM register_logs WHERE event_by_admin=?", (str(getpass.getuser()),))
                    Ids = cursor.fetchall()
                    if Ids is None:
                        Ids = str(Ids)
                    ids = max(Ids)
                    for Id in ids:
                        Id = int(Id)
                    cursor.execute("SELECT register_date FROM register_logs WHERE event_by_admin=? AND id=?", (str(getpass.getuser()), Id))
                    register_date = cursor.fetchone()
                    if register_date is None:
                        register_date = str(register_date)
                    else:
                        for date in register_date:
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
                        messagebox.showerror("Flood Detected", f"Please wait for {rand-minutes} minute(s)!\nAlso note that the duration in which you must wait can vary in your next try.\n\nIt's best to wait an hour after every successful register attempt from the current network/system/OS/account!")
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

    ambiguous_char = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", '"', "'", "|", "{", "}", "[", "]", ":", ";", "/", "?", ",", ".", ">", "<"]
    num_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    lower_case_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    upper_case_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ambiguous_check = []
    num_check = []
    lower_case_char_check = []
    upper_case_char_check = []

    if len(password) < 8:
        messagebox.showerror("error", "Password is too short!\nPassphrase must be at least 8 characters long!")
        return
    else:
        for amb in ambiguous_char:
            if amb in password:
                ambiguous_check.append("1")
            else:
                pass
        if len(ambiguous_check) > 0:
            for num in num_char:
                if num in password:
                    num_check.append("1")
                else:
                    pass
            if len(num_check) > 2:
                for lower in lower_case_char:
                    if lower in password:
                        lower_case_char_check.append("1")
                    else:
                        pass
                if len(lower_case_char_check) > 2:
                    for upper in upper_case_char:
                        if upper in password:
                            upper_case_char_check.append("1")
                        else:
                            pass
                    if len(upper_case_char_check) > 0:
                        pass
                    else:
                        messagebox.showerror("error", "You should at least include 1 upper-case letter in your password!")
                        return
                else:
                    messagebox.showerror("error", "You should at least include 3 different lower-case letters in your password!")
                    return
            else:
                messagebox.showerror("error", "You should at least include 3 different numbers in your password!")
                return
        else:
            messagebox.showerror("error", "You should at least include 1 ambiguous character in your password!")
            return

        if password != confirm_password:
            messagebox.showerror("Cfrm-P-N-M Error!", "PASSWORDS DO NOT MATCH! PLEASE CONFIRM YOUR PASSWORD FIRST!")
            return
        else:
            pass

    confirm_registration = messagebox.askyesno("Register Confirmation", "Have you double-checked the details before you register?\n\n__COMMIT & PROCEED?__")
    if confirm_registration:
        pass
    else:
        return

    cursor.execute("SELECT username FROM register")
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if (f"('{username}',)") in str(usernames):
        update = messagebox.askyesno("EXISTS!", "Usernames are unique & the provided username already exists in the local database!\n\nWant to update your details or even your password?")
        if update:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS cache (username TEXT)""")
            conn.commit()
            cursor.execute("INSERT INTO cache (username) VALUES (?)", (username,))
            conn.commit()
            subprocess.Popen(['python', 'update_login_info.py'])
            window.destroy()
            conn.close()
            return
        else:
            return
    else:
        pass

    current_username = getpass.getuser()
    event_by_admin = current_username
    cursor.execute("INSERT INTO register (name, gender, birth_year, birth_month, birth_day, email, username, password, event_by_admin, register_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, gender, birth_year, birth_month, birth_day, email, username, password, event_by_admin, datetime.datetime.now()))
    conn.commit()
    messagebox.showinfo("Success", "User successfully registered!")

    cursor.execute("""CREATE TABLE IF NOT EXISTS register_logs (
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
    )""")
    conn.commit()
    cursor.execute("INSERT INTO register_logs (name, gender, birth_year, birth_month, birth_day, email, username, password, event_by_admin, register_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (name, gender, birth_year, birth_month, birth_day, email, username, password, event_by_admin, datetime.datetime.now()))
    conn.commit()
    conn.close()

    name_entry.delete(0, tk.END)
    # username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    confirm_password_entry.delete(0, tk.END)
    day_menu.set("DAY")
    month_menu.set("MONTH")
    year_menu.set("YEAR")
    selected_button.set(None)

def real_time_password_status_label():
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    ambiguous_char = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", '"', "'", "|", "{", "}", "[", "]", ":", ";", "/", "?", ",", ".", ">", "<"]
    num_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    lower_case_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    upper_case_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ambiguous_check = []
    num_check = []
    lower_case_char_check = []
    upper_case_char_check = []

    ambiguous_perplexity = []
    num_perplexity = []
    lower_case_perplexity = []
    upper_case_perplexity = []
    for char in password:
        if char in ambiguous_char:
            if len(num_perplexity) == 0 and len(upper_case_perplexity) == 0:
                ambiguous_perplexity.append(1)
            elif len(num_perplexity) > 0 or len(upper_case_perplexity) > 0:
                ambiguous_perplexity.append(2)
                num_perplexity.clear()
        if char in num_char:
            if len(ambiguous_perplexity) == 0 and len(lower_case_perplexity) == 0:
                num_perplexity.append(1)
            elif len(ambiguous_perplexity) > 0 or len(lower_case_perplexity) > 0:
                num_perplexity.append(2)
                lower_case_perplexity.clear()
        if char in lower_case_char:
            if len(num_perplexity) == 0 and len(upper_case_perplexity) == 0:
                lower_case_perplexity.append(1)
            elif len(num_perplexity) > 0 or len(upper_case_perplexity) > 0:
                lower_case_perplexity.append(2)
                upper_case_perplexity.clear()
        if char in upper_case_char:
            if len(ambiguous_perplexity) == 0 and len(lower_case_perplexity) == 0:
                upper_case_perplexity.append(1)
            elif len(ambiguous_perplexity) > 0 or len(lower_case_perplexity) > 0:
                upper_case_perplexity.append(2)
                ambiguous_perplexity.clear()

    perplexity_level = "low"
    if 2 in ambiguous_perplexity:
        perplexity_level = "medium"
    if 2 in upper_case_perplexity:
        perplexity_level = "medium"
    if 2 in lower_case_perplexity:
        perplexity_level = "medium"
    if 2 in num_perplexity:
        perplexity_level = "medium"
    if (2 in ambiguous_perplexity) and (2 in lower_case_perplexity):
        perplexity_level = "high"
    if (2 in upper_case_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in ambiguous_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in upper_case_perplexity) and (2 in lower_case_perplexity):
        perplexity_level = "high"
    if (2 in lower_case_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in ambiguous_perplexity) and (2 in upper_case_perplexity):
        perplexity_level = "high"

    if len(password) == 0:
        stat = "Waiting for you ..."
    elif len(password) < 4:
        stat = "Weakest Passphrase ever!"
    elif len(password) < 8:
        stat = "Passphrase is quite Poor!"
    else:
        for amb in ambiguous_char:
            if amb in password:
                ambiguous_check.append("1")
            else:
                pass
        if len(ambiguous_check) > 0:
            for num in num_char:
                if num in password:
                    num_check.append("1")
                else:
                    pass
            if len(num_check) > 2:
                for lower in lower_case_char:
                    if lower in password:
                        lower_case_char_check.append("1")
                    else:
                        pass
                if len(lower_case_char_check) > 2:
                    for upper in upper_case_char:
                        if upper in password:
                            upper_case_char_check.append("1")
                        else:
                            pass
                    if len(upper_case_char_check) > 0:
                        stat = "Passphrase strength is Fair!"
                        if len(password) > 15 and len(num_check) > 4 and len(lower_case_char_check) > 6 and len(upper_case_char_check) > 1 and len(ambiguous_check) > 1:
                            stat = "Passphrase strength is Average!"
                        if len(password) > 21 and len(upper_case_char_check) > 2 and len(num_check) > 7 and len(lower_case_char_check) > 8 and len(ambiguous_check) > 1 and (perplexity_level == "medium" or perplexity_level == "high"):
                            stat = "Passphrase strength is Good!"
                        if len(password) > 35 and len(ambiguous_check) > 4 and len(upper_case_char_check) > 7 and len(lower_case_char_check) > 12 and len(num_check) > 8 and (perplexity_level == "medium" or perplexity_level == "high"):
                            stat = "Noice! Passphrase strength is now Great!"
                        if len(password) > 45 and len(ambiguous_check) > 7 and len(upper_case_char_check) > 9 and len(lower_case_char_check) > 15 and len(num_check) > 9 and (perplexity_level == "high"):
                            stat = "Great Job! The Passphrase is now Consolidated!"
                        if len(password) > 50 and len(ambiguous_check) > 9 and len(upper_case_char_check) > 11 and len(num_check) > 9 and len(lower_case_char_check) > 17 and (perplexity_level == "high"):
                            stat = "Excellent! This Passphrase is Fortified!"
                    else:
                        stat = "Passphrase is still Weak!"
                else:
                    stat = "Passphrase is still Weak!"
            else:
                stat = "Passphrase is still Weak!"
        else:
            stat = "Passphrase is still Weak!"
    if password != confirm_password and (stat == "Passphrase strength is Average!" or stat == "Passphrase strength is Fair!" or stat == "Passphrase strength is Good!" or stat == "Noice! Passphrase strength is now Great!" or stat == "Excellent! This Passphrase is Fortified!" or stat == "Great Job! The Passphrase is now Consolidated!"):
        stat_label.place(relx=0.5, rely=0.945, anchor=tk.N)
        stat = "PASSWORDS DO NOT MATCH!\nEventhough you may have almost passed some strict security measures,\nBUT PLEASE CONFIRM YOUR PASSWORD FIRST!"
    else:
        stat_label.place(relx=0.5, rely=0.958, anchor=tk.N)
        pass
    status_label.set(stat)

show_it = "no"
def show_entry_text():
    global show_it
    if show_it != "yes":
        password_entry.configure(show="")
        show_pass_button.configure(text="Hide", bg="#333333", fg="white")
        show_it = "yes"
    elif show_it == "yes":
        password_entry.configure(show="*")
        show_pass_button.configure(text="Show", bg="red", fg="yellow")
        show_it = "no"

show_it_2 = "no"
def show_entry_text_2():
    global show_it_2
    if show_it_2 != "yes":
        confirm_password_entry.configure(show="")
        show_pass_button_2.configure(text="Hide", bg="#333333", fg="white")
        show_it_2 = "yes"
    elif show_it_2 == "yes":
        confirm_password_entry.configure(show="*")
        show_pass_button_2.configure(text="Show", bg="red", fg="yellow")
        show_it_2 = "no"

def update_login():
    username = username_entry.get()
    if username == "":
        messagebox.showerror("E-F Error", "To get redirected to the credentials modification window, please fill at least the username field!")
        return
    else:
        pass
    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM register")
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if (f"('{username}',)") in str(usernames):
        confirm = messagebox.askyesno("Confirmation", "Update login info?")
        if confirm:
            conn = sqlite3.connect("accounts.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS cache (username TEXT)""")
            conn.commit()
            cursor.execute("INSERT INTO cache (username) VALUES (?)", (username,))
            conn.commit()
            subprocess.Popen(['python', 'update_login_info.py'])
            window.destroy()
            conn.close()
        else:
            return
    else:
        messagebox.showerror("Invalid User", "Sounds like this username doesn't exist in the local database!\n\nHowever, you need to first signup with this username here on the current window!")

def back_to_login():
    confirm = messagebox.askyesno("Confirmation", "Back to login window?")
    if confirm:
        subprocess.Popen(['python', 'login.py'])
        window.destroy()
        conn.close()
    else:
        return

def check_caps_lock():
    keyboard_state = ctypes.windll.user32.GetKeyState(0x14)
    caps_lock_state = keyboard_state & 0x0001 != 0
    
    if caps_lock_state:
        caps_lock_label_left.configure(fg="red", text="CapsLock On!")
        caps_lock_label_right.configure(fg="red", text="CapsLock On!")
        caps_lock_label_left_2.configure(fg="red", text="CapsLock On!")
        caps_lock_label_right_2.configure(fg="red", text="CapsLock On!")
    else:
        caps_lock_label_left.configure(fg="green", text="")
        caps_lock_label_right.configure(fg="green", text="")
        caps_lock_label_left_2.configure(fg="green", text="")
        caps_lock_label_right_2.configure(fg="green", text="")
    window.after(1000, check_caps_lock)

lightness = "bright"
def dark_bright():
    global lightness
    if lightness == "bright":
        window.configure(bg="#333333")
        radiobutton_frame.configure(bg="#333333")
        style1.configure("Graphical.TRadiobutton", background = "#333333")
        stat_label.configure(bg="#333333")
        dropdowns_frame.configure(bg="#333333")
        caps_lock_label_left.configure(bg="#333333")
        caps_lock_label_right.configure(bg="#333333")
        caps_lock_label_left_2.configure(bg="#333333")
        caps_lock_label_right_2.configure(bg="#333333")
        username_entry.configure(bg="lightblue")
        name_entry.configure(bg="lightblue")
        email_entry.configure(bg="lightblue")
        brightness_button_left.configure(bg="orange", fg="darkgreen", text="Light", width=4, font="arial 8 bold")
        brightness_button_right.configure(bg="orange", fg="darkgreen", text="Light", width=4, font="arial 8 bold")
        brightness_button_left.place(relx=0.033, rely=0.975, anchor=tk.N)
        brightness_button_right.place(relx=0.969, rely=0.975, anchor=tk.N)
        lightness = "dark"
    elif lightness == "dark":
        window.configure(bg="green")
        radiobutton_frame.configure(bg="green")
        style1.configure("Graphical.TRadiobutton", background = "green")
        stat_label.configure(bg="green")
        dropdowns_frame.configure(bg="green")
        caps_lock_label_left.configure(bg="green")
        caps_lock_label_right.configure(bg="green")
        caps_lock_label_left_2.configure(bg="green")
        caps_lock_label_right_2.configure(bg="green")
        username_entry.configure(bg="white")
        name_entry.configure(bg="white")
        email_entry.configure(bg="white")
        brightness_button_left.configure(bg="#333333", fg="orange", text="Dark", width=3, font="arial 7 bold")
        brightness_button_right.configure(bg="#333333", fg="orange", text="Dark", width=3, font="arial 7 bold")
        brightness_button_left.place(relx=0.022, rely=0.984, anchor=tk.N)
        brightness_button_right.place(relx=0.975, rely=0.984, anchor=tk.N)
        lightness = "bright"

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
window.geometry("570x1048")
window.resizable(False, False)
window.title("Register")

main_label = tk.Label(window, text="Register ", font="impact 17 italic", bg="orange")
name_label = tk.Label(window, text="Enter your Name & Last Name: ", font="arial 15 bold", bg="yellow")
name_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
email_label = tk.Label(window, text="Enter your Email: ", font="arial 15 bold", bg="yellow")
email_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
username_label = tk.Label(window, text="Enter your Username: ", font="arial 15 bold", bg="yellow")
username_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge")
password_label = tk.Label(window, text="Enter your Password: ", font="arial 15 bold", bg="yellow")
password_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*", bg="#dddddd")
confirm_password_label = tk.Label(window, text="Confirm your Password: ", font="arial 15 bold", bg="yellow")
confirm_password_entry = tk.Entry(window, font="arial 18 italic", justify="center", width=40, fg="purple", relief="ridge", show="*", bg="#dddddd")
dropdowns_frame = tk.LabelFrame(window, text="Choose your Date of Birth:", bg="green", fg="yellow", bd=3, highlightbackground="#00ff00", highlightthickness=1, font="arial 14 bold", width=230, pady=12, labelanchor="n")

month_menu = ttk.Combobox(dropdowns_frame, width=6, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_menu['values'] = (months)
month_menu.set("MONTH")
month_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
month_menu.state(['readonly'])
month_menu.pack(side="left", padx=44)

day_menu = ttk.Combobox(dropdowns_frame, width=4, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
days = [int(day) for day in range(1, 32)]
day_menu['values'] = (days)
day_menu.set("DAY")
day_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
day_menu.state(['readonly'])
day_menu.pack(side="left", padx=44)

year_menu = ttk.Combobox(dropdowns_frame, width=4, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
years = [int(year) for year in range(1870, 2024)]
year_menu['values'] = (years)
year_menu.set("YEAR")
year_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
year_menu.state(['readonly'])
year_menu.pack(side="left", padx=44)

style1 = ttk.Style()
style1.configure("Graphical.TRadiobutton", indicatorsize=25, background="green", foreground="orange", font="impact 15 italic")
radiobutton_frame = tk.LabelFrame(window, text="You'd rather be referred to as:", bg="green", fg="yellow", bd=3, highlightbackground="#00ff00", highlightthickness=1, font="arial 18 bold", width=230, pady=2, labelanchor="n")
selected_button = tk.StringVar()
radio_button1 = ttk.Radiobutton(radiobutton_frame, text="He", variable=selected_button, value="Male", style="Graphical.TRadiobutton")
radio_button1.pack(side="left", padx=55)
radio_button2 = ttk.Radiobutton(radiobutton_frame, text="She", variable=selected_button, value="Female", style="Graphical.TRadiobutton")
radio_button2.pack(side="left", padx=55)
radio_button3 = ttk.Radiobutton(radiobutton_frame, text="They", variable=selected_button, value="N/A", style="Graphical.TRadiobutton")
radio_button3.pack(side="left", padx=55)

brightness_button_left = tk.Button(window, text="Dark", bg="#333333", fg="orange", font="arial 7 bold", width="3", relief="groove", command=dark_bright)
brightness_button_right = tk.Button(window, text="Dark", bg="#333333", fg="orange", font="arial 7 bold", width="3", relief="groove", command=dark_bright)
brightness_button_left.place(relx=0.022, rely=0.984, anchor=tk.N)
brightness_button_right.place(relx=0.975, rely=0.984, anchor=tk.N)

caps_lock_label_left = tk.Label(window, text="", bg="green", fg="green", font="arial 11 bold", height=1, width=11)
caps_lock_label_right = tk.Label(window, text="", bg="green", fg="green", font="arial 11 bold", height=1, width=11)
caps_lock_label_left_2 = tk.Label(window, text="", bg="green", fg="green", font="arial 11 bold", height=1, width=11)
caps_lock_label_right_2 = tk.Label(window, text="", bg="green", fg="green", font="arial 11 bold", height=1, width=11)
caps_lock_label_left.place(relx=0.17, rely=0.343, anchor=tk.N)
caps_lock_label_right.place(relx=0.83, rely=0.343, anchor=tk.N)
caps_lock_label_left_2.place(relx=0.15, rely=0.43, anchor=tk.N)
caps_lock_label_right_2.place(relx=0.85, rely=0.43, anchor=tk.N)
check_caps_lock()

show_pass_button = tk.Button(window, text="Show", command=show_entry_text, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button.place(relx=0.92, rely=0.3855, anchor=tk.N)
show_pass_button_2 = tk.Button(window, text="Show", command=show_entry_text_2, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button_2.place(relx=0.92, rely=0.478, anchor=tk.N)
submit_button = tk.Button(window, text="Register!", command=register, font="arial 15 bold", bg="blue", fg="yellow", relief="raised")
update_login_info_button = tk.Button(window, text="Update info", command=update_login, font="arial 15 bold", bg="blue", fg="yellow", relief="ridge")
back_to_login_button = tk.Button(window, text="< - Back To Login", command=back_to_login, font="arial 15 bold", bg="darkblue", fg="yellow", relief="ridge")

c_label1 = tk.Label(window, text="Solve the Captcha: ", bg="orange", fg="black", font="arial 15 bold", width=38)
c_entry1 = tk.Entry(window, fg="blue", bg="lightblue", font="arial 18 italic", justify="center", width=30)
captcha_label1 = tk.Label(window, font=("segoe script", 15), width=15, relief="raised", bg="green", borderwidth=1, fg="#00ff00", height=1)
generate_button1 = tk.Button(window, text="Generate New Captcha!", width=35, command=generate_captcha, bg="#00ff00", fg="blue", font="arial 10 bold", relief="groove")

main_label.pack(pady=18)
name_label.pack(pady=10)
name_entry.pack(pady=5)
email_label.pack(pady=10)
email_entry.pack(pady=5)
username_label.pack(pady=10)
username_entry.pack(pady=5)
password_label.pack(pady=10)
password_entry.pack(pady=5)
confirm_password_label.pack(pady=10)
confirm_password_entry.pack(pady=10)
radiobutton_frame.pack(padx=20, pady=16)
dropdowns_frame.pack(padx=20, pady=7)
c_label1.pack(pady=18)
captcha_label1.pack(pady=3)
generate_button1.pack(pady=3)
c_entry1.pack(pady=8)
submit_button.place(relx=0.8, rely=0.9, anchor=tk.N)
update_login_info_button.place(relx=0.2, rely=0.9, anchor=tk.N)
back_to_login_button.place(relx=0.51, rely=0.9, anchor=tk.N)

status_label = tk.StringVar()
stat_label = tk.Label(window, textvariable=status_label, bg="green", fg="#00ff00", font="lotus 10 italic")
password_entry.bind('<KeyRelease>', lambda event: real_time_password_status_label())
confirm_password_entry.bind('<KeyRelease>', lambda event: real_time_password_status_label())
stat_label.place(relx=0.5, rely=0.958, anchor=tk.N)

window.mainloop()
conn.close()