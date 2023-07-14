#@title **Linux遠端桌面**
#@markdown 過程需要4~5分鐘
 
import os
import subprocess
import random, string, urllib.request, json, getpass
 
#@markdown  登入遠端桌面:https://remotedesktop.google.com/headless

import os

username = "user"
password = "root"

# Creation of user
os.system(f"useradd -m {username}")
 
# Add user to sudo group
os.system(f"adduser {username} sudo")
    
# Set password of user to 'root'
os.system(f"echo '{username}:{password}' | sudo chpasswd")
 
# Change default shell from sh to bash
os.system("sed -i 's/\/bin\/sh/\/bin\/bash/g' /etc/passwd")
 
print("用戶創建成功!")
print("您的username: user")
print("您的password: root")
 
#CRP = "DISPLAY= /opt/google/chrome-remote-desktop/start-host --code=\"4/0AX4XfWgDWCk-7bUvdT1ZtFvBSnHnZQXwXobmzNL2nBZDDWIowheHLetSF2wvarJ5VWVEHA\" --redirect-url=\"https://remotedesktop.google.com/_/oauthredirect\" --name=$(hostname)" #@param {type:"string"}
print("請輸入Debian Linux鏈接")
CRP = getpass.getpass()

#@markdown Pin碼已預設為: 123456
Pin = 123456

class CRD:
    def __init__(self):
        os.system("apt update")
        self.installCRD()
        self.installDesktopEnvironment()
        self.installGoogleChorme()
        self.finish()
 
    @staticmethod
    def installCRD():
        print("安裝Google遠端桌面...")
        subprocess.run(['wget', 'https://dl.google.com/linux/direct/chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['dpkg', '--install', 'chrome-remote-desktop_current_amd64.deb'], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
 
    @staticmethod
    def installDesktopEnvironment():
        print("安裝桌面環境...")
        os.system("export DEBIAN_FRONTEND=noninteractive")
        os.system("apt install --assume-yes xfce4 desktop-base xfce4-terminal")
        os.system("bash -c 'echo \"exec /etc/X11/Xsession /usr/bin/xfce4-session\" > /etc/chrome-remote-desktop-session'")
        os.system("apt remove --assume-yes gnome-terminal")
        os.system("apt install --assume-yes xscreensaver")
        os.system("systemctl disable lightdm.service")
 
    @staticmethod
    def installGoogleChorme():
        print("正在安裝Google Chrome...")
        subprocess.run(["wget", "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(["dpkg", "--install", "google-chrome-stable_current_amd64.deb"], stdout=subprocess.PIPE)
        subprocess.run(['apt', 'install', '--assume-yes', '--fix-broken'], stdout=subprocess.PIPE)
 
    @staticmethod
    def finish():
        print("完成")
        os.system(f"adduser {username} chrome-remote-desktop")
        command = f"{CRP} --pin={Pin}"
        os.system(f"su - {username} -c '{command}'")
        os.system("service chrome-remote-desktop start")
        print("success!")
 
 
try:
    if username:
        if CRP == "":
            print("請輸入鏈接")
        elif len(str(Pin)) < 6:
            print("Pin碼必須大於6位數")
        else:
            CRD()
except NameError as e:
    print("未找到用戶 請先創建用戶")
