import os, win32com.client

def create(path1):

    path = os.path.join(path1, 'TaskReminder - Shortcut.lnk')
    target = fr"{path1}\dist\TaskReminder\TaskReminder.exe"
    icon = fr"{path1}\dist\TaskReminder\TaskReminder.exe"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()
def d_create(path):
    if 'TaskReminder - Shortcut.lnk' not in os.listdir():
        create(path)
    if "Log" not in os.listdir(path):
        os.mkdir(f"{path}\Log")
    if "Changes" not in os.listdir(f"{path}\Log"):
        os.mkdir(f"{path}\Log\Changes")
    if "Error" not in os.listdir(f"{path}\Log"):
        os.mkdir(f"{path}\Log\Error")
    if "Backup" not in os.listdir(path):
        os.mkdir(f"{path}\Backup")
    if "Tasks.txt" not in os.listdir(path):
        _x = open(f"{path}\Tasks.txt", "a+")
        _x.close()