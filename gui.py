import shutil
from tkinter import *
import minecraft_launcher_lib
import os
import glob
import math
import sys

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




class ModData:
    os.chdir("./mods")
    modfiles_in_system = glob.glob("*.jar")
    mods_in_system = list()

    for mod in modfiles_in_system:
        new_mod = mod[:-4]
        mods_in_system.append(new_mod)



def delete_files_in_mc_mods_folder():
    try:
        files = glob.glob(os.path.join(os.path.join(minecraft_launcher_lib.utils.get_minecraft_directory(), "mods"), "*.jar"))
        for file in files:
            os.remove(file)

    except OSError as e:
        change_status("An error occured when clearing mod folder.")



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
        mods.append(IntVar(value=0))  # Add a new IntVar for each mod
        mod = mod.replace("-", " ")
        mod = mod.replace("_", " ")
        mod_check = Checkbutton(select_gui, text=mod, variable=mods[mod_id - 1])

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