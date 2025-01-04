import shutil
from tkinter import *
import minecraft_launcher_lib
import os
import glob
import math
import sys
import zipfile
import json
import requests
from packaging.version import Version



def get_version_data():
    versions_data_url = 'https://launchermeta.mojang.com/mc/game/version_manifest_v2.json'

    response = requests.get(versions_data_url)

    version_data = response.json()

    version_names = []

    for version in version_data["versions"]:
        if version["type"] == "release":
            version_names.append(version["id"])

    return version_names



mods = []

if not os.path.exists("./mods"):
    os.mkdir("./mods")



if not os.path.exists(os.path.join(os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods"))):
    os.mkdir(os.path.join(os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods")))



def set_window_icon(icon_name, root):
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(__file__)

    icon_path = os.path.join(application_path, icon_name)

    if os.path.exists(icon_path):
        root.iconbitmap(default=icon_path)
    else:
        print(f"Error: Icon file not found at {icon_path}")


from packaging.version import Version


from packaging import version

from packaging import version

def normalize_version(constraint):
    """
    Normalize version constraints (e.g., '>=1.21, <2' -> separate checks)
    """
    parts = [part.strip() for part in constraint.split(',')]
    conditions = []

    for part in parts:
        if '>' in part:
            conditions.append(lambda v: v > version.parse(part[2:].strip()))
        elif '<' in part:
            conditions.append(lambda v: v < version.parse(part[2:].strip()))
        elif '=' in part:
            conditions.append(lambda v: v == version.parse(part[2:].strip()))
        else:
            conditions.append(lambda v: v == version.parse(part))

    return conditions

def get_valid_versions(mod_version, constraint):
    """
    Check if mod_version satisfies the version constraint.
    """
    try:
        mod_version = version.parse(mod_version)
        conditions = normalize_version(constraint)

        # Check if the mod version satisfies all conditions
        return all(condition(mod_version) for condition in conditions)
    except Exception as e:
        print(f"Error comparing versions: {mod_version} with {constraint}: {e}")
        return False



class ModData:
    os.chdir("./mods")
    modfiles_in_system = glob.glob("*.jar")
    mods_in_system = list()

    for mod in modfiles_in_system:
        new_mod = mod[:-4]

        with zipfile.ZipFile(mod, 'r') as f:

            try:
                list_of_mod_content = f.infolist()

                for i in list_of_mod_content:

                    file_name = i.filename
                    if file_name == "fabric.mod.json":

                        with f.open(file_name, "r") as json_file:
                            data = json.load(json_file)

                        depends = data.get("depends", {})
                        minecraft_version = depends.get("minecraft")

                        if minecraft_version:
                            print(f"{mod}: Minecraft version dependency: {minecraft_version}")
                            compatible_versions = get_valid_versions(minecraft_version, get_version_data())
                            print(f"Compatible versions: {compatible_versions}")
                        else:
                            print(f"{mod}: No 'minecraft' dependency found.")

            except Exception as e:
                print(f"An error occured while loading mods: {e}")

        mod_name = mod.split(os.path.sep)[-1]
        mods_in_system.append(mod_name)

    print("Mods in system:", mods_in_system)



def delete_files_in_mc_mods_folder():
    try:
        files = glob.glob(os.path.join(os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods"), "*.jar"))
        print(files)
        for file in files:
            os.remove(file)
            print(file)

    except Exception as e:
        change_status(f"An error occured when clearing mod folder: {e}")



def mod_select():
    global select_gui
    global gui
    global mods

    gui.destroy()

    select_gui = Tk()
    select_gui.title("Mod Select | By BravestCheetah")
    set_window_icon("mc-modmanager-icon.ico", select_gui)
    select_gui.geometry("500x600")

    select_gui.columnconfigure(0, weight=1)
    select_gui.columnconfigure(1, weight=1)

    done_button = Button(select_gui, text="Save", command=save)
    cancel_button = Button(select_gui, text="Cancel", command=main)

    done_button.grid(row=0, column=0, sticky="we")
    cancel_button.grid(row=0, column=1, sticky="we")

    mods.clear()
    mod_id = 0

    for mod in ModData.mods_in_system:
        mod_id += 1
        mod_name = mod[0]
        mods.append(IntVar(value=0))  # Add a new IntVar for each mod
        mod_name = mod_name.replace("-", " ")
        mod_name = mod_name.replace("_", " ")
        mod_check = Checkbutton(select_gui, text=mod_name, variable=mods[mod_id - 1])

        mod_check.grid(row=math.floor(mod_id / 2 - 0.5) + 1, column=1 - mod_id % 2, sticky="w")

    select_gui.mainloop()



def save():
    global select_gui
    global mod_save
    global mods

    mod_save = [mod.get() for mod in mods]

    select_gui.destroy()
    main()



def inject_saved_mods():
    global mod_save
    global mods

    change_status("Clearing minecraft mods folder...")
    delete_files_in_mc_mods_folder()

    for index, mod_state in enumerate(mod_save):
        change_status("Checking mod: " + ModData.modfiles_in_system[index])
        if mod_state == 1:
            mod_file = ModData.modfiles_in_system[index]
            mod_file_dir = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mods", mod_file))

            change_status("Injecting mod: " + ModData.modfiles_in_system[index])

            shutil.copy(mod_file_dir, os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods"))

    change_status("Done!")




def main():
    print(ModData.mods_in_system)
    global gui
    global dir_text_info
    global dir_text
    global mod_button
    global inject_button
    global status_text

    gui = Tk()
    gui.title("MC-ModManager | By BravestCheetah")
    gui.geometry("600x120")
    set_window_icon("mc-modmanager-icon.ico", gui)
    gui.resizable(0, 0)

    gui.columnconfigure(0, weight=1)
    gui.columnconfigure(1, weight=1)

    #directory textbox
    dir_text_info = Label(gui, text="Fabric Installation Directory:", anchor="w")

    dir_text = Label(gui, text=os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods"), borderwidth=5, bg="LIGHTGREY", anchor="w")

    #buttons :D
    mod_button = Button(gui, text="Mod Select", command=mod_select)
    inject_button = Button(gui, text="Inject", command=inject_saved_mods)

    #Status
    status_text = Label(gui, text="Status")

    #specify grid pos
    dir_text_info.grid(row=0, column=0, columnspan=2, pady=2, sticky="ew")
    dir_text.grid(row=1, column=0, columnspan=2, pady=2, padx=10, sticky="ew")


    mod_button.grid(row=2, column=0, pady=2, padx=2, sticky="ew")
    inject_button.grid(row=2, column=1, pady=2, padx=2, sticky="ew")

    status_text.grid(row=3, column=0, columnspan=2, pady=2, sticky="ew")

    #mainloop
    gui.mainloop()



def change_status(text):
    global status_text

    status_text.config(text=text)



if __name__ == "__main__":
    main()