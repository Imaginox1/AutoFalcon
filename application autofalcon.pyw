from PIL import Image
import customtkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
from time import sleep

customtkinter.set_appearance_mode("System")  # Light/Dark/System
customtkinter.set_default_color_theme("blue")  # Theme: blue, dark-blue, green

# ---------------- ROOT ----------------
root = customtkinter.CTk()
root.title("Auto Falcon")
root.geometry("600x400")
root.iconbitmap('C:/Users/caleb/OneDrive/Documents/Caleb/Personal/a/falcon no bakground.ico')

# ---------------- TOGGLE PASSWORD ----------------
def toggle_password():
    if password_entry.cget("show") == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="Hide Password")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="Show Password")

# ---------------- LOGIN FUNCTION ----------------
def perform_login():
    gmailI = gmail_entry.get()
    gmailId = gmailI + "@fbcs.school"
    pwd = password_entry.get()

    status_label.configure(text="Processing...", text_color="black")
    root.update_idletasks()

    # Run Selenium in a background 
    
    def login_task():
        driver = webdriver.Edge()

        try:
            driver.get(r'https://faithkids.myschoolapp.com/app/?fromHash=login#login')
            driver.maximize_window()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Username')))
            driver.find_element(By.ID, 'Username').send_keys(gmailId)
            driver.find_element(By.ID, 'nextBtn').click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.sky-btn.sky-btn-primary.sky-btn-block.spa-auth-btn-primary')))
            driver.find_element(By.CSS_SELECTOR, 'button.sky-btn.sky-btn-primary.sky-btn-block.spa-auth-btn-primary').click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'identifierId')))
            driver.find_element(By.ID, 'identifierId').send_keys(gmailId)
            driver.find_element(By.ID, 'identifierNext').click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Passwd')))
            driver.find_element(By.NAME, 'Passwd').send_keys(pwd)
            driver.find_element(By.ID, 'passwordNext').click()

            status_label.configure(text="Login Successful!", text_color="green")
            root.update_idletasks()
            sleep(600000)
            driver.quit()

        except Exception as e:
            status_label.configure(text="Login Failed. Please check your email and password.", text_color="red")
            root.update_idletasks()
            driver.quit()
    threading.Thread(target=login_task, daemon=True).start()

# ---------------- HEADER ----------------
header_frame = customtkinter.CTkFrame(root, fg_color="#003366", height=70)
header_frame.pack(side="top", fill="x")

logo_image = customtkinter.CTkImage(Image.open("Faith long Logo.png"), size=(250, 50))
logo_label = customtkinter.CTkLabel(header_frame, image=logo_image, text="")
logo_label.pack(pady=10)
logo_label.image = logo_image  # Prevent garbage collection

# ---------------- LOGIN FRAME ----------------
login_frame = customtkinter.CTkFrame(root)
login_frame.pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="w")

# Username (left aligned)
gmail_label = customtkinter.CTkLabel(login_frame, text="BBID Username without @fbcs.school", anchor="w", justify="left")
gmail_label.pack(anchor="w")
gmail_entry = customtkinter.CTkEntry(login_frame, width=600)
gmail_entry.pack(pady=5, anchor="w")

# Password (left aligned)
password_label = customtkinter.CTkLabel(login_frame, text="Password", anchor="w", justify="left")
password_label.pack(anchor="w")
password_entry = customtkinter.CTkEntry(login_frame, show="*", width=600)
password_entry.pack(pady=5, anchor="w")

# Toggle Password Button (slightly higher, right under password field)
toggle_button = customtkinter.CTkButton(login_frame, text="Show Password", command=toggle_password, width=150)
toggle_button.pack(pady=(0, 10), anchor="w")

# Remember Me
# remember_var = customtkinter.StringVar(value="off")
# remember_checkbox = customtkinter.CTkCheckBox(login_frame, text="Remember me", variable=remember_var)
# remember_checkbox.pack(pady=10, anchor="e")

# Buttons (left aligned)
button_frame = customtkinter.CTkFrame(login_frame, fg_color="transparent")
button_frame.pack(pady=10, anchor="c")

next_button = customtkinter.CTkButton(button_frame, text="Next", command=perform_login)
next_button.grid(row=0, column=0, padx=5)
# Bind the Enter/Return key to perform_login
root.bind("<Return>", lambda event: perform_login())

cancel_button = customtkinter.CTkButton(button_frame, text="Cancel", fg_color="gray", hover_color="darkgray", command=root.quit)
cancel_button.grid(row=0, column=1, padx=5)

# Status Label (left aligned)
status_label = customtkinter.CTkLabel(login_frame, text="", text_color="black", anchor="e", justify="left")
status_label.pack(pady=10, anchor="e")

# ---------------- MAINLOOP ----------------
root.mainloop()
