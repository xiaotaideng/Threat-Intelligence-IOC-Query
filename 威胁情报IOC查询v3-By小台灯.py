from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from tkinter import messagebox
import time

def get_screen_dimensions(window):
    # Function to get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    return screen_width, screen_height

def center_window(window, width, height):
    # Function to center the window on the screen
    screen_width, screen_height = get_screen_dimensions(window)
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f'{width}x{height}+{x_coordinate}+{y_coordinate}')

def start_browser():
    # Function to start the Chrome browser
    global driver
    driver = webdriver.Chrome(service=service)

def close_existing_windows():
    # Close all existing windows except the original one
    handles = driver.window_handles
    while len(handles) > 1:
        driver.switch_to.window(handles[-1])
        driver.close()
        handles = driver.window_handles
    driver.switch_to.window(handles[0])  # Switch back to the original window

def search():
    search_queries = entry.get("1.0", tk.END).strip().split("\n")
    search_queries = [query.strip() for query in search_queries if query.strip()]
    if not search_queries:
        messagebox.showerror("错误", "请先输入IP地址，点击可选项后再搜索。")
        return

    selected_engines = [i for i, var in enumerate(option_vars) if var.get() == 1]

    if not selected_engines:
        messagebox.showerror("错误", "请选择至少一个威胁情报查询引擎")
        return

    global driver
    try:
        # Check if the driver is already closed and restart if necessary
        driver.title
    except:
        start_browser()

    close_existing_windows()  # Close existing windows before opening new ones

    for query in search_queries:
        for i in selected_engines:
            try:
                if i == 0:  # 微步
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get('https://x.threatbook.com/')
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[4]/div[2]/div/div[1]/div[1]/div[2]/textarea')))
                elif i == 1:  # 鹰图
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get('https://hunter.qianxin.com/')
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/main/div[1]/div[2]/div[2]/div[1]/input')))
                elif i == 2:  # 奇安信
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get('https://ti.qianxin.com/v2/search')
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="block-content"]/div[1]/header/div[1]/div[2]/input')))
                elif i == 3:  # 钟馗
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get('https://www.zoomeye.org/')
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="appZoomEye"]/div/div/div[2]/div[2]/form/div/div/div/ul/li/div/input')))
                elif i == 4:  # Shodan
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[-1])
                    driver.get('https://www.shodan.io/')
                    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-query"]')))
                search_box.send_keys(query)
                search_box.send_keys(Keys.RETURN)
            except Exception as e:
                messagebox.showerror("错误", f"无法在威胁情报搜索引擎 {options[i]} 中搜索: {str(e)}")

def on_closing():
    try:
        driver.quit()
    except:
        pass
    root.destroy()

# 创建一个Chrome服务
chrome_driver_path = "./chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# 启动浏览器实例
start_browser()

# 创建tkinter窗口
root = tk.Tk()
root.title("威胁情报IOCv3-By小台灯")
root.geometry("800x450")  # 设置窗口大小

# 居中窗口
center_window(root, 800, 450)

#给IP输入框创建复制、粘贴、剪贴右键菜单
def create_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="复制", command=lambda: widget.event_generate('<<Copy>>'))
    menu.add_command(label="粘贴", command=lambda: widget.event_generate('<<Paste>>'))
    menu.add_command(label="剪切", command=lambda: widget.event_generate('<<Cut>>'))
    widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))



# 创建提示标签
label = tk.Label(root, text="请输入IP进行查询（每行一个IP）:")
label.pack(pady=5)


# 创建IP内容输入框（多行）
# entry = tk.Text(root, width=80, height=12)  # 增大输入框大小
# entry.pack(pady=20)
# create_context_menu(entry)
'''
代码优化说明
添加滚动条:
创建一个 text_frame 框架，将 entry 和 scrollbar 放置其中。
使用 entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 和 scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 来排列输入框和滚动条。
绑定滚动条和文本输入框。

布局调整:
使用 place 方法来精确定位按钮的位置。
取消不必要的 pack 方法，避免冲突。
'''
# 创建IP内容输入框（多行）并增加滚动条
text_frame = tk.Frame(root)
text_frame.pack(pady=20)

entry = tk.Text(text_frame, width=80, height=10)
entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(text_frame, command=entry.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

entry.config(yscrollcommand=scrollbar.set)
create_context_menu(entry)

# 创建搜索引擎选项
options = ["微步", "鹰图", "奇安信", "钟馗", "Shodan"]
option_vars = []

#创建一个Frame用户居中显示选项
frame = tk.Frame(root)
frame.pack()

for opt in options:
    var = tk.IntVar()
    var.set(0)
    option_vars.append(var)
    check_button = tk.Checkbutton(frame, text=opt, variable=var, width=5, height=2, font=("Helvetica", 12))
    check_button.pack(side=tk.LEFT) # 居中显示
frame.place(relx=0.45, rely=0.55, anchor=tk.CENTER,)

# 创建全选按钮
select_all_var = tk.IntVar()
select_all_var.set(0)

def select_all():
    global option_vars
    select_value = select_all_var.get()
    for var in option_vars:
        var.set(select_value)

select_all_button = tk.Checkbutton(root, text="全选", variable=select_all_var, command=select_all, width=5, height=2, font=("Helvetica", 12))
select_all_button.place(relx=0.77, rely=0.55, anchor=tk.CENTER)  # 调整全选按钮位置

#创建一个清空输入框的按钮
def clear_entry():
    entry.delete("1.0", tk.END)

# 创建清空输入框的按钮
clear_button = tk.Button(root, text="清空", command=clear_entry, width=10, height=2, font=("Helvetica", 12))
clear_button.pack(pady=20)
clear_button.pack(side=tk.LEFT)
clear_button.place(relx=0.65, rely=0.7, anchor=tk.CENTER)

# 从config.txt文件中读取账号和密码信息
accounts = {}
try:
    with open('config.txt', 'r') as file:
        for line in file:
            data = line.strip().split()
            if len(data) == 3:  # 确保每行有三个元素
                key = data[0]  # 第一个元素作为键
                value = data[1:]  # 剩下的元素作为值的列表
                accounts[key] = ' '.join(value)  # 将值的列表合并为一个字符串
except FileNotFoundError:
    # messagebox.showinfo("提示", "在当前文件夹下已生成config.txt配置文件，请按照规范配置后再重启程序登录！")
    print("未找到config.txt文件")
    # 创建新的config.txt文件并写入内容
    with open('config.txt', 'w') as file:
        file.write("#微步 user123 pass123\n")
        file.write("#鹰图 user123 pass123\n")
        file.write("#奇安信 user123 pass123\n")
        file.write("#钟馗 user123 pass123\n")
        file.write("#Shodan user123 pass123\n")
        file.write("\n")
        # file.write("#这个配置文件主要是给自动登录配置的！\n")
        file.write("#使用方法：把#去掉，替换对应的账号和密码。\n")
        file.write("#特别注意：账号前面的名称不能修改！账号和前面的名称有空格，账号和密码中间也有空格。\n")
        file.write("#特别注意：账号前面的名称不能修改！账号和前面的名称有空格，账号和密码中间也有空格。\n")
        file.write("#特别注意：账号前面的名称不能修改！账号和前面的名称有空格，账号和密码中间也有空格。\n")
print(accounts)


#创建批量登录函数
def login():
    selected_engines = [i for i, var in enumerate(option_vars) if var.get() == 1]
    if not selected_engines:
        messagebox.showerror("错误", "请选择至少一个威胁情报登录")
        return
    global driver
    try:
        # Check if the driver is already closed and restart if necessary
        driver.title
    except:
        start_browser()
    for i in range(len(options)):
        if option_vars[i].get() == 1:
            if i == 0:  # 微步
                # print("当前选项:", options[i])
                selected_option = options[i]
                if selected_option in accounts:
                    data = accounts[selected_option].split()
                    if len(data) == 2:
                        name = data[0]
                        password = data[1]
                    else:
                        print(f"账号信息格式错误: {selected_option}")
                else:
                    messagebox.showinfo("自动化登录提示", f"请配置好config.txt文件中{selected_option}的账号和密码，然后重新运行程序。确保账号密码填写规范。")
                    return  # 停止执行后续代码
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get('https://passport.threatbook.cn/login?service=x&callbackURL=https://x.threatbook.com/v5/node/db3fae7d2dd14bf0/8963c70f2b71019b?redirectURL=https%253A%252F%252Fx.threatbook.com%252F')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[3]/div[2]'))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/div/label/span'))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="phoneOrEmail"]'))).send_keys(name)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(password)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[2]/div[1]/div/div[4]/form/div[3]/div/input'))).click()
            elif i == 1:    # 鹰图
                # print("当前选项:", options[i])
                selected_option = options[i]
                if selected_option in accounts:
                    data = accounts[selected_option].split()
                    if len(data) == 2:
                        name = data[0]
                        password = data[1]
                    else:
                        print(f"账号信息格式错误: {selected_option}")
                else:
                    messagebox.showinfo("自动化登录提示", f"请配置好config.txt文件中{selected_option}的账号和密码，然后重新运行程序。确保账号密码填写规范。")
                    return  # 停止执行后续代码
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get('https://user.skyeye.qianxin.com/user/sign-in?wx=https://hunter.qianxin.com/qrCode&next=https://hunter.qianxin.com/api/uLogin')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pane-first"]/div/form/div[1]/div/div[2]/input'))).send_keys(name)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pane-first"]/div/form/div[2]/div/div[2]/input'))).send_keys(password)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pane-first"]/div/form/div[3]/div/button/span'))).click()
            elif i == 2:    # 奇安信
                # print("当前选项:", options[i])
                selected_option = options[i]
                if selected_option in accounts:
                    data = accounts[selected_option].split()
                    if len(data) == 2:
                        name = data[0]
                        password = data[1]
                    else:
                        print(f"账号信息格式错误: {selected_option}")
                else:
                    messagebox.showinfo("自动化登录提示", f"请配置好config.txt文件中{selected_option}的账号和密码，然后重新运行程序。确保账号密码填写规范。")
                    return  # 停止执行后续代码
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get('https://user.ti.qianxin.com/login')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__qiankun_microapp_wrapper_for_login_alpha__"]/div/div[2]/div/div/div[2]/div[3]/div[1]/label/span[1]/span'))).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__qiankun_microapp_wrapper_for_login_alpha__"]/div/div[2]/div/div/div[2]/form/div[1]/div/div/input'))).send_keys(name)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__qiankun_microapp_wrapper_for_login_alpha__"]/div/div[2]/div/div/div[2]/form/div[2]/div/div/div/input'))).send_keys(password)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="__qiankun_microapp_wrapper_for_login_alpha__"]/div/div[2]/div/div/div[2]/div[2]/button[1]/span'))).click()
            elif i == 3:    # 钟馗
                # print("当前选项:", options[i])
                selected_option = options[i]
                if selected_option in accounts:
                    data = accounts[selected_option].split()
                    if len(data) == 2:
                        name = data[0]
                        password = data[1]
                    else:
                        print(f"账号信息格式错误: {selected_option}")
                else:
                    messagebox.showinfo("自动化登录提示", f"请配置好config.txt文件中{selected_option}的账号和密码，然后重新运行程序。确保账号密码填写规范。")
                    return  # 停止执行后续代码
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get('https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.zoomeye.org%2Flogin')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="login_form"]/div[2]/input'))).send_keys(name)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="inputPassword"]'))).send_keys(password)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-login"]'))).click()
            elif i == 4:    # shodan
                # print("当前选项:", options[i])
                selected_option = options[i]
                if selected_option in accounts:
                    data = accounts[selected_option].split()
                    if len(data) == 2:
                        name = data[0]
                        password = data[1]
                    else:
                        print(f"账号信息格式错误: {selected_option}")
                else:
                    messagebox.showinfo("自动化登录提示", f"请配置好config.txt文件中{selected_option}的账号和密码，然后重新运行程序。确保账号密码填写规范。")
                    return  # 停止执行后续代码
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get('https://account.shodan.io/login?continue=https%3A%2F%2Fwww.shodan.io%2Fdashboard')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys(name)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(password)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/main/div/div/div/div[1]/form/div[3]/input'))).click()



#在TK界面创建一个登录按钮
login_button = tk.Button(root, text="登录", command=login, width=10, height=2, font=("Helvetica", 12))
login_button.pack(pady=20)
login_button.pack(side=tk.LEFT)
login_button.place(relx=0.35, rely=0.7, anchor=tk.CENTER)

# 创建查询按钮
# search_button = tk.Button(root, text="查询", command=search, width=10, height=2, font=("Helvetica", 12))
# search_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
search_button = tk.Button(root, text="查询", command=search, width=10, height=2, font=("Helvetica", 12))
search_button.pack(pady=20)
search_button.pack(side=tk.LEFT)
search_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# 绑定窗口关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 运行tkinter窗口
root.mainloop()