from tkinter import *
import re

def main():
    PASSWORD = input("Enter your password")
    config = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    
    pat = re.compile(config)
    
    mat = re.search(pat, PASSWORD)
    
    if mat:
        print("valid.")
    else:
        print("invalid")






































































