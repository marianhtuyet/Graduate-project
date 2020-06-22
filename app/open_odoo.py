# pip install pyinstaller
# pyinstaller --onefile open_odoo.py
import os
# Note: In linux, command have to put in quote Ex: os.system("gnome-terminal -e '{command}'")
TERMINAL_COMMAND = "C:\\Users\\Anhtuyet\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe C:\\odoo_project\\odoo\\odoo-bin -c C:/odoo_project/odoo.conf"
BROWSER_COMMAND = ""
if os.name == 'nt':
    open_cmd = "start cmd /c "
else:
    open_cmd = "gnome-terminal -e "

os.system(open_cmd + TERMINAL_COMMAND)