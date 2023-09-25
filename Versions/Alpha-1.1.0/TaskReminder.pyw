import tkinter.messagebox
import customtkinter
from tkinter import font
from tkinter import *
from datetime import datetime, date
import os
import shutil
import idk
from errors import *
from changes import *
from decouple import config
from createashortcut import *
from pathlib import Path

# To be run first

path = Path(__file__).parents[2]
backup()

if 'TaskReminder - Shortcut.lnk' not in os.listdir():
    create()

# FROM Config File

title = config('TITLE')
icon = config('ICON_OPTION')
icon_path = config('ICON_PATH')
appearance_mode = config('APPEARANCE_MODE')
theme = config('THEME')
version = config('VERSION')

customtkinter.set_appearance_mode(appearance_mode)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme(theme)  # Themes: blue (default), dark-blue, green

# Default File Locations

backup_path = fr"{path}\Backup"
tasks_path = fr"{path}\Tasks.txt"

file = open(tasks_path, "r") # Opens the text file in read
newFC = [i.rstrip() for i in file.readlines()] # Stores every line of the file in a list with the removal if \n or newline
file.close()
while('' in newFC): # If the list still has an empty string this line will run
    newFC.remove('') # This removes the empty string in the list

dictionary = dict() # Creates a dictionary for a better programmability

def getTime():
    time_now = datetime.now()
    date_now = date.today()
    current_time = time_now.strftime("%H:%M:%S")
    time = f"{date_now} {current_time}"
    time = time.replace(":", "-")
    return time


def TaskAssigning():
    global keysList # Declares keysList as a global variable
    TaskTitle = -1
    keysList = list(dictionary.keys())  # Makes a list out of the keys (from the TaskTitling() function) in the dictionary
    x = 0
    for i in newFC:
        if i in dictionary:
            TaskTitle += 1
        elif i.startswith(">"):
            values = i[2:]
            print(keysList)
            dictionary[f"{keysList[TaskTitle]}"][values] = {"Description": "", "Due Date": "", "Priority": ""} # will have description/instruction, due date, priority
            try:
                xx = x # Gets the current value of x and assigns it to xx
                for idk in range(0,3): # A loop for 3 times
                    y = newFC[xx + 1]
                    if y.startswith("*>Desc") or y.startswith("*>Description"):
                        dash_1 = y.find("-")
                        dictionary[f"{keysList[TaskTitle]}"][values]["Description"] = (y[dash_1 + 2:] if y[dash_1 + 1] == " " else y[dash_1 + 1:])
                    elif y.startswith("*>Due"):
                        dash_1 = y.find("-")
                        dictionary[f"{keysList[TaskTitle]}"][values]["Due Date"] = (y[dash_1 + 2:] if y[dash_1 + 1] == " " else y[dash_1 + 1:])
                    elif y.startswith("*>Priority"):
                        dash_1 = y.find("-")
                        dictionary[f"{keysList[TaskTitle]}"][values]["Priority"] = (y[dash_1 + 2:] if y[dash_1 + 1] == " " else y[dash_1 + 1:])
                    xx += 1
            except:
                continue
        x += 1


def TaskTitling():
    for i in newFC:
        if i.startswith(">") == False and i.startswith("*>") == False:
            dictionary[i] = {}


def save_dictionary():
    str = ""
    for i in dictionary:
        str += f"{i}\n"
        for k, v in dictionary[i].items():
            str += f"> {k}\n"
            for a, b in dictionary[i][k].items():
                y = "Due Date" if a == "Due Date" else "Description" if a == "Description" else "Priority"
                str += f"*>{y} - {b}\n"
    return str

TaskTitling()
TaskAssigning()

appHeight = 250
appWidth = 250
ctk = customtkinter

app = ctk.CTk()
app.geometry(f"{appWidth}x{appHeight}+810+430")
app.title(title)
if icon == 1:
    app.iconphoto(False, PhotoImage(file=icon_path)) # ONLY PNG
# app.attributes("-topmost", True)

# Function for SubTasks

def Specfic_SubTask(TaskTitle):
    SubTaskKeys = list(dictionary[TaskTitle].keys())
    SubTask = ""
    SubtaskList = list()

    for i in SubTaskKeys:
        SubTask += f"> {i} \n"
        SubTask += f"Description: {dictionary[TaskTitle][i]['Description']}\n"
        SubTask += f"Due Date: {dictionary[TaskTitle][i]['Due Date']}\n"
        SubTask += f"Priority: {dictionary[TaskTitle][i]['Priority']}\n"
        SubtaskList.append(f"> {i} \n")
        SubtaskList.append(f"Description: {dictionary[TaskTitle][i]['Description']}\n")
        SubtaskList.append(f"Due Date: {dictionary[TaskTitle][i]['Due Date']}\n")
        SubtaskList.append(f"Priority: {dictionary[TaskTitle][i]['Priority']}\n")

    return SubTask, SubtaskList

# Specfic Task Window

def Specfic_Task_Window(TaskTitle):
    Showing_Task = ctk.CTkToplevel(master=app)
    Showing_Task.title("Tasks")
    Showing_Task.geometry("450x400")
    Showing_Task.attributes("-topmost", True)
    LabelTaskTitle = ctk.CTkLabel(master=Showing_Task, text=TaskTitle, text_font=("Arial", 17), text_color="#53adcb")
    LabelTaskTitle.place(relx=0.5, rely=0.135, anchor=ctk.CENTER)

    SST = Specfic_SubTask(TaskTitle)
    SubTaskText, SubtaskList = SST[0], SST[1]

    textfont = font.Font(size=15, family="Arial")
    text = Text(Showing_Task, width=30, height=10, background="#212325", bd=0, font=textfont, fg="white")
    text.insert(INSERT, SubTaskText)
    text.insert(END, "")

    linenum = 1
    for line in SubtaskList:
        text.tag_config("Task", foreground="blue")
        text.tag_config("Subtask", foreground="yellow")
        if line.startswith(">"):
            text.tag_add("Task", f"{linenum}.0", f"{linenum}.1")
        elif line.startswith("Description:"):
            text.tag_add("Subtask", f"{linenum}.0", f"{linenum}.11")
        elif line.startswith("Due Date:"):
            text.tag_add("Subtask", f"{linenum}.0", f"{linenum}.9")
        elif line.startswith("Priority:"):
            text.tag_add("Subtask", f"{linenum}.0", f"{linenum}.9")
        linenum += 1

    text.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    buttonExit = ctk.CTkButton(master=Showing_Task, text="Exit", command=Showing_Task.withdraw, width=30)
    buttonExit.place(relx=0.9, rely=0.9, anchor=ctk.CENTER)

# Specfic Task Menu Window

def Specific_Task():
    Showing_Task = ctk.CTkToplevel(master=app)
    Showing_Task.title("Tasks")
    Showing_Task.geometry("300x300")

    def TaskTitleOption():
        TaskTitle = OptionMenuTaskTitle.get()
        Specfic_Task_Window(TaskTitle)

    button_task_title = ctk.CTkButton(master=Showing_Task, text="Choose", command=TaskTitleOption, width=50)
    button_task_title.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
    OptionMenuTaskTitle_var = ctk.StringVar(value="Choose")
    OptionMenuTaskTitle = ctk.CTkOptionMenu(master=Showing_Task, values=[i for i in keysList], variable=OptionMenuTaskTitle_var)
    OptionMenuTaskTitle.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
    buttonExit = ctk.CTkButton(master=Showing_Task, text="Exit", command=Showing_Task.withdraw, width=30)
    buttonExit.place(relx=0.9, rely=0.9, anchor=ctk.CENTER)

# All Task Window

def All_Task():
    All_Task = ctk.CTkToplevel(master=app)
    All_Task.title("All Tasks")
    All_Task.geometry("400x570")
    All_Task.attributes("-topmost", True)

    AllTask = ''

    textfont = font.Font(size=15, family="Arial")
    text = Text(All_Task, width=30, height=15, background="#212325", bd=0, font=textfont, fg="white")

    ctkBar = ctk.CTkScrollbar(master=All_Task, command=text.yview, height=300, width=16, border_spacing=2, fg_color="#212325")
    ctkBar.place(relx=0.97, rely=0.5, anchor=ctk.CENTER)

    for i in keysList:
        SST = Specfic_SubTask(i)
        AllTaskText= SST[0]
        AllTask += f"{i}\n{AllTaskText}\n"

    text.insert(INSERT, AllTask)
    text.insert(END, "")

    linenum, x, idk = 1, 0, 0
    AllTaskListNames = []
    for i in keysList:
        SST = Specfic_SubTask(i)
        AllTaskList = SST[1]
        AllTaskListNames.append(i)

        if AllTaskListNames[idk] == i:
            x += 1
        for line in AllTaskList:
            text.tag_config("Task", foreground="blue")
            text.tag_config("Subtask", foreground="yellow")
            if line.startswith(">"):
                text.tag_add("Task", f"{x + linenum}.0", f"{x + linenum}.1")
            elif line.startswith("Description:"):
                text.tag_add("Subtask", f"{x + linenum}.0", f"{x + linenum}.11")
            elif line.startswith("Due Date:"):
                text.tag_add("Subtask", f"{x + linenum}.0", f"{x + linenum}.9")
            elif line.startswith("Priority:"):
                text.tag_add("Subtask", f"{x + linenum}.0", f"{x + linenum}.9")
            linenum += 1
        x += 1
        idk += 1

    text.configure(yscrollcommand=ctkBar.set, state="disabled")
    text.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    buttonExit = ctk.CTkButton(master=All_Task, text="Exit", command=All_Task.withdraw, width=30, text_font=("Arial", 11))
    buttonExit.place(relx=0.85, rely=0.93, anchor=ctk.CENTER)

# Show Task Menu Window

def Show_Task_Menu():
    Show_Task_Menu = ctk.CTkToplevel(master=app)
    Show_Task_Menu.title("Show Task Menu")
    Show_Task_Menu.geometry("300x300")

    windowLabel_ShowTaskMenu = ctk.CTkLabel(master=Show_Task_Menu, text="Show Task Menu", text_font=("Arial", 17), text_color="#53adcb")
    windowLabel_ShowTaskMenu.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
    buttonSpecific = ctk.CTkButton(master=Show_Task_Menu, text="Specific Task", command=Specific_Task, width=70, text_font=("Arial", 12))
    buttonSpecific.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
    buttonAllTask = ctk.CTkButton(master=Show_Task_Menu, text="All Tasks", command=All_Task, width=70, text_font=("Arial", 12))
    buttonAllTask.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    buttonExit = ctk.CTkButton(master=Show_Task_Menu, text="Exit", command=Show_Task_Menu.withdraw, width=30, text_font=("Arial", 11))
    buttonExit.place(relx=0.85, rely=0.9, anchor=ctk.CENTER)

# Modify Task Menu Window

def Modify_Task_Menu():
    global keysList
    global dictionary
    Modify_Task_Menu = ctk.CTkToplevel(master=app)
    Modify_Task_Menu.title("Show Task Menu")
    Modify_Task_Menu.geometry("300x300")
    Modify_Task_Menu.attributes("-topmost", True)

    ModifyOptionMenu = ctk.CTkOptionMenu(master=Modify_Task_Menu, values=["Add", "Remove", "Edit"], variable=ctk.StringVar(value="Choose"))
    ModifyOptionMenu.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    OptionLabel = ctk.CTkLabel(master=Modify_Task_Menu, text='', text_font=("Arial", 15), text_color="white")
    OptionLabel.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

    entry = customtkinter.CTkEntry(master=Modify_Task_Menu, width=100, placeholder_text="CTkEntry")
    RemoveOptionMenu = ctk.CTkOptionMenu(master=Modify_Task_Menu, values=[i for i in keysList], variable=ctk.StringVar(value="Choose"))
    task_title_optionmenu = ctk.CTkOptionMenu(master=Modify_Task_Menu, values=[i for i in keysList], variable=ctk.StringVar(value="Choose"))

    def OptionReset():
        try:
            ModifyOptionMenu.configure(values=["Add", "Remove", "Edit"], variable=ctk.StringVar(value="Choose"))
            buttonChoose.configure(command=OptionChose)
            entry.place_forget()
            RemoveOptionMenu.place_forget()
            task_title_optionmenu.place_forget()
            OptionLabel.configure(text='')
            ModifyOptionMenu.configure(state="enabled")
            ModifyOptionMenu.place_configure(relx=0.5, rely=0.5, anchor=ctk.CENTER)
            OptionLabel.place_configure(relx=0.5, rely=0.4, anchor=ctk.CENTER)
            subtask_title_optionmenu.place_forget()
        except:
            pass

    # changes_for_log = ""

    OptionChosen = ''
    def OptionFunc(ToChange):
        global OptionChosen
        global keysList
        global dictionary

        modify_status = False

        if OptionChosen == "Add":
            name = entry.get()
            if ToChange == "Task":
                try:
                    if name not in keysList and name != "":
                        dictionary[name] = {}

                        modify_status = True
                        done = f"'{name}' in Main Task"

                    else:
                        message = "Input already exists!" if name in keysList else "Entry is empty!"
                        tkinter.messagebox.showerror(title="Error", message=message)
                        raise (AlreadyExists(name) if name in keysList else EmptyEntry())
                except (AlreadyExists, EmptyEntry) as err:
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])

            elif ToChange == "Subtask":
                task_title = task_title_optionmenu.get()
                try:
                    if task_title != "Choose" and name not in list(dictionary[task_title].keys()) and name != "":
                        dictionary[task_title][name] = {"Description": "", "Due Date": "", "Priority": ""}

                        modify_status = True
                        done = f"Sub task '{name}' in '{task_title}' Task"

                    else:
                        error = "Choose first!" if (task_title == "Choose") else "Entry is empty!" if name == '' else f"Subtask: {name} already exists!"
                        tkinter.messagebox.showerror(title="Error", message=error)
                        raise (InvalidValue(task_title) if task_title == "Choose" else EmptyEntry() if name == '' else AlreadyExists(name))
                except (AlreadyExists, EmptyEntry, InvalidValue) as err:
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])

            elif ToChange == "Description" or "Due Date" or "Priority":  # To be improved
                OptionLabel.configure(text=f"{OptionChosen} ({ToChange})")
                task_title = task_title_optionmenu.get()
                subtask_title = subtask_title_optionmenu.get()
                tb_changed = dictionary[task_title][subtask_title][ToChange]
                try:
                    if task_title != "Choose" and name != "" and tb_changed == '':
                        dictionary[task_title][subtask_title][ToChange] = name

                        modify_status = True
                        done = f"'{name}' for the {ToChange} of Sub task '{subtask_title}' in '{task_title}' Task"

                    else:
                        error = "Choose first!" if task_title != "Choose" else "Entry is empty!" if name != "" else f"{ToChange} is not empty!"
                        tkinter.messagebox.showerror(title="Error", message=error)
                        raise (InvalidValue(task_title) if task_title == "Choose" else EmptyEntry() if name == '' else NotEmpty(ToChange))
                except (NotEmpty, EmptyEntry, InvalidValue) as err:
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])


        elif OptionChosen == "Remove":
            if ToChange == "Task":
                task_title = task_title_optionmenu.get()
                dictionary.pop(task_title)

                modify_status = True
                done = f"'{task_title}'"

            elif ToChange == "Subtask":
                task_title = task_title_optionmenu.get()
                subtask_title = subtask_title_optionmenu.get()
                try:
                    dictionary[task_title].pop(subtask_title)

                    modify_status = True
                    done = f"'{subtask_title}' in '{task_title}'"

                except KeyError as err:
                    tkinter.messagebox.showerror(title="Error", message=f"{subtask_title} does not exist or already removed!")  # To be improved
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])


            elif ToChange == "Description" or "Due Date" or "Priority":
                OptionLabel.configure(text=f"{OptionChosen} ({ToChange})")
                task_title = task_title_optionmenu.get()
                subtask_title = subtask_title_optionmenu.get()
                tb_changed = dictionary[task_title][subtask_title][ToChange]
                if task_title != "Choose":
                    dictionary[task_title][subtask_title][ToChange] = ""

                    modify_status = True
                    done = f"Data of '{ToChange}' for '{subtask_title}' in '{task_title}'"

                elif tb_changed == "":
                    tkinter.messagebox.showerror(title="Error", message=f"Data already empty!")  # To be improved


        elif OptionChosen == "Edit":
            name = entry.get()
            if ToChange == "Task":
                if name not in keysList:
                    task_title = task_title_optionmenu.get()
                    try:
                        if task_title != "Choose" and name != "":
                            keyPos = idk.keyPosition(dictionary, task_title)
                            dictionary = idk.replaceKey(dictionary, keyPos, name)

                            modify_status = True
                            done = f"name of '{task_title}' to '{name}'"

                        else:
                            error = "Choose first!" if (task_title == "Choose") else "Entry is empty!"
                            tkinter.messagebox.showerror(title="Error", message=error)
                            raise (InvalidValue(task_title) if task_title == "Choose" else EmptyEntry())
                    except (InvalidValue, EmptyEntry) as err:
                        error_name = err.__class__.__name__
                        error_logging(error_name, getTime()[:10], getTime()[11:])
            elif ToChange == "Subtask":
                task_title = task_title_optionmenu.get()
                subtask_title = subtask_title_optionmenu.get()
                try:
                    if task_title != "Choose" and name != "":
                        keyPos = idk.keyPosition(dictionary[task_title], subtask_title)
                        dictionary[task_title] = idk.replaceKey(dictionary[task_title], keyPos, name)

                        modify_status = True
                        done = f"name of '{subtask_title}' in '{task_title}' to '{name}'"

                    else:
                        error = "Choose first!" if (task_title == "Choose") else "Entry is empty!"
                        tkinter.messagebox.showerror(title="Error", message=error)
                        raise (InvalidValue(task_title) if task_title == "Choose" else EmptyEntry())
                except (InvalidValue, EmptyEntry) as err:
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])

            elif ToChange == "Description" or "Due Date" or "Priority":
                OptionLabel.configure(text=f"{OptionChosen} ({ToChange})")
                task_title = task_title_optionmenu.get()
                subtask_title = subtask_title_optionmenu.get()
                tb_changed = dictionary[task_title][subtask_title][ToChange]
                try:
                    if task_title != "Choose" and name != "":
                        dictionary[task_title][subtask_title][ToChange] = name

                        modify_status = True
                        done = f"Data '{ToChange}' for '{subtask_title}' in '{task_title}' from '{tb_changed}' to '{name}'"

                    else:
                        error = "Choose first!" if (task_title == "Choose") else "Entry is empty!"
                        tkinter.messagebox.showerror(title="Error", message=error)
                        raise (InvalidValue(task_title) if task_title == "Choose" else EmptyEntry())
                except (InvalidValue, EmptyEntry) as err:
                    error_name = err.__class__.__name__
                    error_logging(error_name, getTime()[:10], getTime()[11:])

        keysList = list(dictionary.keys())  # Updates the global keysList
        task_title_optionmenu.configure(values=[i for i in keysList])

        # LOGGING

        if modify_status:
            path = changes().name
            changes_file = open(path, "a")
            changes_file.write(f"Modification Type: '{OptionChosen}', Modified: '{ToChange}', {'Added' if OptionChosen == 'Add' else 'Removed' if OptionChosen == 'Remove' else 'Modified'}: {done}\n")


    def OptionFunc_Subtask(Option):
        global subtask_title_optionmenu
        task_title = task_title_optionmenu.get()
        try:
            if task_title != "Choose":
                subtask_title_optionmenu = ctk.CTkOptionMenu(master=Modify_Task_Menu,
                                                             values=[i for i in list(dictionary[task_title].keys())])
                subtask_title_optionmenu.place(relx=0.5, rely=0.52, anchor=ctk.CENTER)
                buttonChoose.configure(command=lambda: OptionFunc(Option))
            else:
                tkinter.messagebox.showerror(title="Error", message="Please choose!")
                raise InvalidValue(task_title)
        except InvalidValue as err:
            error_name = err.__class__.__name__
            error_logging(error_name, getTime()[:10], getTime()[11:])


    def GUI():
        global OptionChosen
        OptionLabel.configure(text=OptionChosen)
        if OptionChosen == "Add" or OptionChosen == "Edit":
            entry.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

    def OptionChose():
        global OptionChosen
        Option = ModifyOptionMenu.get()
        if Option in ["Add", "Remove", "Edit"]:
            ModifyOptionMenu.configure(values=["Task", "Subtask", "Description", "Due Date", "Priority"], variable=ctk.StringVar(value="Choose"))
            OptionChosen = Option
        if Option in ["Task", "Subtask", "Description", "Due Date", "Priority"]:
            ModifyOptionMenu.configure(state="disabled")
            if Option == "Task":
                GUI()
                if OptionChosen == "Add":
                    buttonChoose.configure(command=lambda: OptionFunc("Task"))
                else:
                    ModifyOptionMenu.place_forget()
                    task_title_optionmenu.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
                    buttonChoose.configure(command=lambda: OptionFunc(Option))
            elif Option == "Subtask":
                GUI()
                if OptionChosen == "Remove":
                    ModifyOptionMenu.place_forget()
                    task_title_optionmenu.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
                    buttonChoose.configure(command=lambda: OptionFunc_Subtask(Option))
                elif OptionChosen == 'Add':
                    buttonChoose.configure(command=lambda: OptionFunc("Subtask"))
                    task_title_optionmenu.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
                else:
                    GUI()
                    ModifyOptionMenu.place_forget()
                    task_title_optionmenu.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
                    OptionLabel.place_configure(relx=0.5, rely=0.3, anchor=ctk.CENTER)
                    buttonChoose.configure(command=lambda: OptionFunc_Subtask(Option))
            else:
                GUI()
                ModifyOptionMenu.place_forget()
                task_title_optionmenu.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
                OptionLabel.place_configure(relx=0.5, rely=0.3, anchor=ctk.CENTER)
                buttonChoose.configure(command=lambda: OptionFunc_Subtask(Option))


    buttonChoose = ctk.CTkButton(master=Modify_Task_Menu, text="Confirm", command=OptionChose, width=30, text_font=("Arial", 11))
    buttonChoose.place(relx=0.35, rely=0.8, anchor=ctk.CENTER)

    buttonReset = ctk.CTkButton(master=Modify_Task_Menu, text="Reset", command=OptionReset, width=30, text_font=("Arial", 11))
    buttonReset.place(relx=0.65, rely=0.8, anchor=ctk.CENTER)

    windowLabel_ShowTaskMenu = ctk.CTkLabel(master=Modify_Task_Menu, text="Modify Task Menu", text_font=("Arial", 17), text_color="#53adcb")
    windowLabel_ShowTaskMenu.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
    buttonExit = ctk.CTkButton(master=Modify_Task_Menu, text="Exit", command=Modify_Task_Menu.withdraw, width=30, text_font=("Arial", 11))
    buttonExit.place(relx=0.85, rely=0.9, anchor=ctk.CENTER)


# MAIN WINDOW

windowVersionLabel_Main = ctk.CTkLabel(master=app, text=f"Version: {version}", text_font=("Arial", 9))
windowVersionLabel_Main.place(relx=0.175, rely=0.95, anchor=ctk.CENTER)
windowLabel_Main = ctk.CTkLabel(master=app, text="Main Window", text_font=("Arial", 17), text_color="#53adcb")
windowLabel_Main.place(relx=0.5, rely=0.175, anchor=ctk.CENTER)
buttonShowTask_Main = ctk.CTkButton(master=app, text="Show", width=50, command=Show_Task_Menu, text_font=("Arial", 12))
buttonShowTask_Main.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
buttonShowModify_Main = ctk.CTkButton(master=app, text="Modify", width=50, text_font=("Arial", 12), command=Modify_Task_Menu)
buttonShowModify_Main.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
buttonExit_Main = ctk.CTkButton(master=app, text="Exit", command=app.quit, width=20, text_font=("Arial", 11))
buttonExit_Main.place(relx=0.85, rely=0.9, anchor=ctk.CENTER)

app.mainloop()

backup()
file_save = open(fr'{path}\Tasks.txt', 'a')
file_save.truncate(0)

file_save.write(save_dictionary())

file_save.close()

'''
Changes in dictionary will be saved here or somewhere else within the loop
> Get the changed (idk) then modify the file with it prolly more efficient than rewriting the whole file but harder!
'''

# Save the file after closed