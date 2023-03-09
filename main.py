import tkinter
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ctypes
import os.path

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('AutoNote4.0 Pro')

user_state = True

if not os.path.isfile("C:/AutoNote4.0 Pro/account.txt"):
    f = open("C:/AutoNote4.0 Pro/account.txt", "w")
    f.write("請更改此檔案:\n第一行為您的帳號，第二行為您的密碼。\n更改後請重新開啟應用程式。")
    user_state = False
    f.close()

user_acc = open('C:/AutoNote4.0 Pro/account.txt', 'r').read().split('\n')
user_ID = user_acc[0]
user_PW = user_acc[1]
if (not user_ID.isdigit()) or (len(user_PW)<6):
    user_state = False


user_title = 'AutoNote 4.0 Pro'
window = tk.Tk()
window.geometry('200x300')
window.title(user_title)
#window.iconbitmap('C:/AutoNote4.0 Pro/icon.ico')


def validate(P):
    if str.isdigit(P) or P == '':
        return True


vcmd = (window.register(validate), '%P')
tx1 = tk.Label(window, text="Course ID:")
tx1.pack(pady=10)
in1 = tk.Entry(window, validate='key', validatecommand=vcmd)
in1.pack()
tx2 = tk.Label(window, text='Delay (ms):')
tx2.pack(pady=10)
in2 = tk.Entry(window, validate='key', validatecommand=vcmd)
in2.pack()


def button_event():
    window.quit()
    user_CL = in1.get()
    delay = int(in2.get()) / 1000
    print(delay)
    option = webdriver.ChromeOptions()
    option.binary_location = 'C:/AutoNote4.0 Pro/iron/chrome.exe'
    driver_path = 'C:/AutoNote4.0 Pro/chromedriver.exe'
    ir = webdriver.Chrome(executable_path=driver_path, options=option)
    clas_url = 'https://eclass2.nttu.edu.tw/media/doc/' + user_CL + '#doc-tabs-note'
    login_url = 'https://eclass2.nttu.edu.tw/index/login'
    ir.get(login_url)
    WebDriverWait(ir, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="account"]/div/input')))
    block_login1 = ir.find_element(By.XPATH, '//*[@id="account"]/div/input')
    block_login1.send_keys(user_ID)
    block_login2 = ir.find_element(By.XPATH, '//*[@id="password"]/div/div[1]/input')
    block_login2.send_keys(user_PW)
    block_login3 = ir.find_element(By.XPATH, '//*[@id="captcha"]/div/input')
    block_login3.click()
    find_save = 'url = {"save":'
    find_rsave = ',"get":"\\/ajax'
    rs = '<div style="font-size:0px">111111111111111111111111111111111111111111111111111</div>'
    js = "CKEDITOR.instances['note-textarea'].getData = function b(a)"
    js += " {return '" + rs + "';}"
    WebDriverWait(ir, 300).until(EC.url_to_be('https://eclass2.nttu.edu.tw/'))
    ir.get(clas_url)

    while WebDriverWait(ir, 100).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="doc-tabs-note"]/div/div[1]/div/div/div[1]/form/div[4]/div[2]/button[1]'))):
        time.sleep(delay)
        ir.execute_script(js)
        confirm = ir.find_element(By.XPATH,
                                  '//*[@id="doc-tabs-note"]/div/div[1]/div/div/div[1]/form/div[4]/div[2]/button[1]')
        confirm.click()

def button2_event():
    f = open("C:/AutoNote4.0 Pro/account.txt", "w")
    f.write("請更改此檔案:\n第一行為您的帳號，第二行為您的密碼。\n更改後請重新開啟應用程式。")
    f.close()
    osCommandString = "notepad.exe C:/AutoNote4.0 Pro/account.txt"
    os.system(osCommandString)

if not user_state:
    mybutton = tk.Button(window, text='請檢查帳密', command=button_event)
    mybutton["state"] = tk.DISABLED
else :
    mybutton = tk.Button(window, text='Start', command=button_event)
mybutton.pack(fill=tkinter.X, side=tkinter.BOTTOM, padx=60, pady=30)

mybutton2 = tk.Button(window, text='修改帳密', command=button2_event)
mybutton2.pack(fill=tkinter.X, side=tkinter.BOTTOM, padx=60, pady=0)

window.mainloop()
