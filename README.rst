**********************
Task Reminder by hornley
**********************
Version: Alpha-2.0.0
^^^^^^^^^^^^^^^^^^^^^^

Task Reminder is written in **Python**.


How to use::

    Navigate to dist > TaskReminder
    Find and run TaskReminder

    Once the app is ran, it will create a shortcut in your Folder so no need to do navigation anymore.

- Features:
    - Modification of tasks
        - Adding
        - Removing
        - Editing
    - Showing of tasks
        - Specific Task
        - All Task
    - Logging
        - Changes
        - Errors
    - Settings
        - Main Settings (accessible through the main window)
            - Minimizable option
            - Backup option
            - Topmost option
            - Reset after modification option
            - Icon option
            - Theme option
            - Check for updates button
        - Window settings (for other windows other than the main)
            - Topmost option
    - Backup

- To be added:
    - Hotkey to open and close
    - One window only (Improvement)
    - Custom Background (Colors or Images)
    - Delete previous versions of TaskReminder after an install
    - Update Features of RST

socials
--------
`Task Reminder Github <https://github.com/hornley/taskreminder>`_

`Discord Profile <https://discord.com/users/341604307113738243>`_

`Discord Server <https://discord.gg/6QmeEDjWUm>`_

versions
--------
- Alpha-1.0.0 (09-23-2023)
    - Released
- Alpha-1.1.0 (09-24-2023)
    - Saving fix
    - Path.txt no longer needed
    - Auto shortcut creation after one run
    - Version label added in main window
- Alpha-1.2.0 (09-24-2023)
    - 1 to 2 window
- Alpha-1.3.0 (09-25-2023)
    - Added Custom Icon Configuration
    - Added dark and light modes
    - Added themes
    - Added installer (thru 7-Zip)
    - Added a README.txt with the same contents as README.rst
    - Fixed Tast.txt overwritten after a new update
    - Fixed the X button of each window not closing properly
    - Fixed Backup/Logging path does not exist error
- Alpha-1.4.0 (09-30-2023)
    - Added a date chooser or calendar gui for the due date
    - Added an option menu for priority
    - Added Reset after a modification in config
    - Added done button in specific task window, choose a subtask within the chosen task to remove as done
    - Added settings for each window (Only Topmost option available)
    - Added Check for almost due tasks
    - Subtask near due date pop up
    - Backup disable and enable config
    - Minimizable to taskbar config
    - Change some text buttons
    - Fixed Specific Showed Task not closing the other windows
    - Fixed error messages
- Alpha-2.0.0 (10-10-2023)
    - Removed Show Task Menu in minimized items
    - Fixed the placement of settings window
    - Fixed value of topmost not getting kept
    - Use the main settings instead of config.txt
    - Due Date Fixed
    - Updated ctk library for better features
    - Less storage used! (around 20mb)