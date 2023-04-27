import tkinter as tk
from tkinter import font
import os, random, string
from assets import CryptApp, Vault

app = tk.Tk()
Ubuntu = font.Font(font="Ubuntu")

class data():
    reading = open("assets/Private/code.txt", "r")
    code = reading.readline()
    reading.close()
    trys = 3
    reading1 = open("assets/Private/key.txt", "r")
    key = reading1.readline()
    reading1.close()
    reading2 = open("assets/Private/random_string.txt", "r")
    random_string = reading2.readline()
    reading2.close()

def update_data():
    code1 = open("assets/Private/code.txt", "r")
    data.code = code1.readlines()
    code1.close()
    data.trys = 3
    code2 = open("assets/Private/key.txt", "r")
    data.key = code2.readlines()
    code2.close()
    code3 = open("assets/Private/random_string.txt", "r")
    data.random_string = code3.readlines()
    code3.close()
    print("We have finish to update the data")

def random_string_recup():
    file = open("assets/Private/random_string.txt", "r")
    data.random_string = file.readlines()
    file.close()

def Exit_App():
    app.destroy()

def key_create1():
    usb_directory = f"/media/antho/{key_input0.get()}/Key_Protect/"
    if os.path.exists(usb_directory) == True:
        data.random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(10, 100)))
        tofile = open("assets/Private/random_string.txt", "w")
        tofile.write(data.random_string)
        tofile.close()
        creator = open(f"{usb_directory}Underlocker_generate.txt", "w+")
        creator.write(data.random_string)
        creator.close()
        CryptApp.crypt_decrypt(entry_file=f"{usb_directory}Underlocker_generate.txt", exit_file=f"{usb_directory}Underlocker.txt", key=data.key)
        os.remove(f"{usb_directory}Underlocker_generate.txt")

        label2.config(text=f"We have install on {key_input0.get()} your reset key")
    else:
        print("Error !! Try debug...")
        os.mkdir(usb_directory)
        key_create1()
    key_input0.destroy()
    key_button1.config(text="Exit", command=Exit_App)

def key_create():
    app.title("The_Vault/Key_creator")
    button1.destroy()
    button2.destroy()

    global label2
    label2 = tk.Label(app, text="Entry the usb key's name:", font=Ubuntu, bg="black", fg="white")
    label2.pack(pady=10)
    global key_input0
    key_input0 = tk.Entry(app, bg="black", fg="white", font=Ubuntu)
    key_input0.pack(pady=10)
    global key_button1
    key_button1 = tk.Button(app, text="Send", command=key_create1)
    key_button1.pack(pady=10)

def usb_detector():
    input("We wait the USB key press any key to start")
    usb_directory = "/media/antho/"
    # Récupérer la liste des fichiers dans le répertoire /media
    files = os.listdir(usb_directory)

    # Chercher le nom de la clé USB
    usb_name = ""
    for file in files:
        if "usb" in file.lower():
            usb_name = file
            break

    # Si la clé USB est trouvée, extraire le fichier .txt
    if usb_name:
        txt_file_path = os.path.join(usb_directory, usb_name, "Key_Protect/Underlocker.txt")
        the_Underlock = CryptApp.crypt_decrypt(entry_file=txt_file_path, exit_file=f"{txt_file_path}.txt", key=data.key)
        text_file = open(f"{txt_file_path}.txt", "r")
        text_files = text_file.readlines()
        text_file.close()
        os.remove(f"{txt_file_path}.txt")
        random_string_recup()
        if text_files == data.random_string:
            print("True Start process....")
            inputer0.destroy()
            emu_button1.destroy()
            code = input("new code: ")
            cofile = open("assets/Private/code.txt", "w")
            cofile.write(code)
            cofile.close()
            update_data()
            app.destroy()

        else:
            print("Invalid Key")
    else:
        print("La clé USB n'a pas été détectée.")

def emulator_verif():
    if data.trys != 0:
        if data.code == inputer0.get():
            print("Code == True")
            data.trys = 3
            app.destroy()
            print("Open vault ....")
            Vault.run()
        else:
            data.trys = data.trys - 1
            print(f"Code == False you have {data.trys} try left")
            if data.trys == 0:
                emulator_verif()
    else:
        print("You don't have try left. Start the underlock key process...")
        usb_detector()

def emulator():
    app.title("The_Vault/Emulator")
    button1.destroy()
    button2.destroy()

    global inputer0
    inputer0 = tk.Entry(app, bg="black", fg="white", font=Ubuntu)
    inputer0.pack(pady=10)
    global emu_button1
    emu_button1 = tk.Button(app, text="Send", command=emulator_verif, font=Ubuntu)
    emu_button1.pack(pady=10)

def appli():
    #1 des 2 apps (1= keyapp 2= emulator)
    app.title("The_Vault")
    app.geometry("500x500")
    app.config(bg="black")

    label0 = tk.Label(app, font=Ubuntu, text="Key_Protect", bg="black", fg="white")
    label0.pack(pady=10)

    global button1
    button1 = tk.Button(app, text="Run: Emulator", command=emulator, font=Ubuntu)
    button1.pack(pady=10)
    global button2
    button2 = tk.Button(app, text="Run: KeyApp", font=Ubuntu, command=key_create)
    button2.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    appli()