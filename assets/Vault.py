import tkinter as tk
from tkinter import font
import os, zipfile, Run_App, json
from assets import CryptApp

def exit_app():
    app.destroy()

def underlock():
    print("Underlocking...")
    os.mkdir("The_Vault")
    os.mkdir("reserv_construct")
    # Ouvrir le fichier zip
    with zipfile.ZipFile("The_Vault.zip", "r") as zip_ref:
        # Extraire tous les fichiers dans le dossier "mon_dossier"
        zip_ref.extractall("reserv_construct")
    # définir le chemin du dossier à lister
    directory = "reserv_construct"
    # obtenir la liste de tous les fichiers dans le dossier
    files = os.listdir(directory)
    # json requirments
    global final_file
    CryptApp.crypt_decrypt(entry_file="reserv_construct/list.json", exit_file="list.json", key=Run_App.data.key)
    os.remove("reserv_construct/list.json")
    # afficher chaque nom de fichier dans la liste
    for file in files:
        print(f"Decrypting: {file}")
        final_file = file
        if file != "list.json":
            if ".crypt" in final_file:
                final_file = final_file.split(".")[0]
                with open('list.json') as f:
                    data = json.load(f)
                for mot in data:
                    if final_file in mot:
                        valeur = data[mot]
                        break
                final_file = final_file + valeur
                print(final_file)
            CryptApp.crypt_decrypt(entry_file=f"reserv_construct/{file}", exit_file=f"The_Vault/{final_file}", key=Run_App.data.key)
            os.remove(f"reserv_construct/{file}")
    os.rmdir("reserv_construct")
    os.remove("The_Vault.zip")
    os.remove("list.json")
    print("Finish")

def lock():
    print("Locking...")
    myzip = zipfile.ZipFile('The_Vault.zip', 'w')
    # définir le chemin du dossier à lister
    directory = "The_Vault"
    # obtenir la liste de tous les fichiers dans le dossier
    files = os.listdir(directory)
    # Creation de la liste list.json
    json_list = {}
    json_helper = ""
    global final_file
    # afficher chaque nom de fichier dans la liste
    for file in files:
        final_file = file
        print(f"Crypting: {file}")
        if "." in file:
            remove_char = True
            for char in reversed(file):
                if char == ".":
                    remove_char = False
                    break
                else:
                    json_helper = char + json_helper
                    final_file = final_file[:-1]
            json_list[f"{file}"] = f".{json_helper}"
            CryptApp.crypt_decrypt(entry_file=f"The_Vault/{file}", exit_file=f"{final_file}crypt", key=Run_App.data.key)
            # ajouter un fichier à l'archive
            myzip.write(f"{final_file}crypt")
            os.remove(f"{final_file}crypt")
            os.remove(f"The_Vault/{file}")
        else:
            CryptApp.crypt_decrypt(entry_file=f"The_Vault/{file}", exit_file=file, key=Run_App.data.key)
            # ajouter un fichier à l'archive
            myzip.write(file)
            os.remove(file)
            os.remove(f"The_Vault/{file}")
    print("Start closing process....")
    json_create = open("list1.json", "w+")
    json.dump(json_list, json_create)
    json_create.close()
    CryptApp.crypt_decrypt(entry_file="list1.json", exit_file="list.json", key=Run_App.data.key)
    myzip.write("list.json")
    os.remove("list.json")
    os.remove("list1.json")
    os.rmdir("The_Vault")
    print("Finish")


def create_vault():
    if os.path.exists("The_Vault/check.txt") != True:
        os.mkdir("The_Vault")
        check = open("The_Vault/check.txt", "w+")
        check.write("Please don't delete this file")
        check.close()
        print("We have create The_Vault")
    else:
        print("The_Vault already exist")

def run():
    print("Start....")
    global app
    global Ubuntu
    app = tk.Tk()
    Ubuntu = font.Font(font="Ubuntu")
    app.title("Your_Vault")
    app.geometry("500x500")
    app.config(bg="black")

    global la0
    la0 = tk.Label(app, text="Chose an option:", bg="black", fg="white", font=Ubuntu)
    la0.pack(pady=10)

    global bu0
    bu0 = tk.Button(app, text="Create your Vault", font=Ubuntu, command=create_vault)
    bu0.pack(pady=10)
    global bu1
    bu1 = tk.Button(app, text="Lock The_Vault", font=Ubuntu, command=lock)
    bu1.pack(pady=10)
    global bu2
    bu2 = tk.Button(app, text="Underlock The_Vault", font=Ubuntu, command=underlock)
    bu2.pack(pady=10)

    bu_exit = tk.Button(app, text="Exit App", font=Ubuntu, command=exit_app, bg=None, fg="purple")
    bu_exit.pack(pady=10)

    print("Please check if the file The_Vault/ exists for use it or The_Vault.zip")

    app.mainloop()