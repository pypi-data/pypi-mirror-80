#will show all my python files in one screen

import os, glob
import sys
import random
from pyfiglet import Figlet
import importlib
import pylint
import time



modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]




count=-1
y = []
for i in __all__:
	count=count+1
	lst2 = str(count)+" "+i
	y += [lst2]

x = y



def func_initialize():
	chno1 = int(input("\n enter file number to open "))
	aa = __all__[chno1]+".py"

# code used in multiple function

def clearscreen():
	os.system("cls")

def colorchanger():
	rc = random.randint(0,10)
	os.system("color "+str(rc))


def file_info():
	chno1 = int(input("\n enter file number to open "))
	aa = __all__[chno1]+".py"
	print('File         :', aa)
	print('Access time  :', time.ctime(os.path.getatime(aa)))
	print('Modified time:', time.ctime(os.path.getmtime(aa)))
	print('Change time  :', time.ctime(os.path.getctime(aa)))
	print('Size         :', os.path.getsize(aa))
    
	file = open(aa,"r")
	Counter = 0
	Content = file.read() 
	CoList = Content.split("\n") 
	for i in CoList: 
		if i: 
			Counter += 1
	print("This is the number of lines in the file ",Counter) 
	


def banner():
	custom_fig = Figlet(font='nvscript')
	print(custom_fig.renderText('p-index'))



def main_menu():
    for a,b,c in zip(x[::3],x[1::3],x[2::3]):
        print('{:<30}{:<30}{:<}'.format(a,b,c))

#avoid using default keyword like open as function

                                                    

def enter_file_to_open():
	chno = int(input("\n enter file number to open "))
	os.system('python '+__all__[chno]+".py")




def readit():
	chno1 = int(input("\n enter file number to open "))
	aa = __all__[chno1]+".py"
	file = open(aa, 'r')
	contents = file.read()
	file.close()
	print(contents)

def open_in_notepad():
	try:
		chno1 = int(input("\n enter file number to open "))
		aa = __all__[chno1]+".py"
		osCommandString = "notepad.exe "+'"'+aa+'"'
		os.system(osCommandString)
	except:
		print("file is not there | type correct option")

def open_in_vscode():
	try:
		chno1 = int(input("\n enter file number to open in vs code "))
		aa = __all__[chno1]+".py"
		osCommandString = "code "+'"'+aa+'"'
		os.system(osCommandString)
	except:
		print("file is not there | type correct option")


def install_py__module():
	minstall = input("enter python module to install ")
	os.system("python -m pip install "+minstall)


def check_quality():
	try:
		chno1 = int(input("\n enter file number to check its quality "))
		aa = __all__[chno1]+".py"
		os.system("pylint "+aa)
	except:
		print("file is not there | type correct option")
	

def reading_read_me():
	try:
		chno1 = int(input("\n enter file number to view its readme "))
		la = __all__[chno1]
		module = importlib.import_module(la, package=None)
		module.read_me()
	except:
		print("python file doesnt have read_me() method")

class Error(Exception):
    """Base class for other exceptions"""
    pass


class qutt(Error):
    """Raised when user want to quit the program"""
    pass

def quitscreen():
	raise qutt("quit")

"""
add below line to your code so it dont execute on import and you can use readme 
function to view information about it


----------------------------------start------------------------------------------

def read_me():
    print("useless file used to test random things")

def main():
    pass

if __name__ == "__main__":
    main()


------------------------------------end------------------------------------------

"""


"""
def chooseoption():
    print("do you want to run single time or multiple times")
    inp = input()
    if(inp[0] == "m"):
        multichooseit()
    else:
        chooseit()

"""


def print_options():
 #i do not gurantee that this tool will work
 print("\n choose options: ")
 print("1. change color")
 print("2. open file in prompt")
 print("3. read file content into prompt")
 print("4. open file in notepad")
 print("5. open file in vscode")
 print("6. open readme of python file")
 print("7. install python module")
 print("8. check python file quality")
 print("9. get file information")
 print("10. clear screen")
 print("11. exit")




def choose_options():
	try:
		print("\n choose any option ")
		cho = int(input())
		if(cho == 1): 
			colorchanger()

		if(cho == 2):
			enter_file_to_open()

		if(cho == 3):
			readit()

		if(cho == 4):
			open_in_notepad()

		if(cho == 5):
			open_in_vscode()

		if(cho == 6):
			reading_read_me()

		if(cho == 7):
			install_py__module()

		if(cho == 8):
			check_quality()

		if(cho == 9):
			file_info()

		if(cho == 10):
			clearscreen()

		if(cho == 11):
			quitscreen()
	
	except qutt:
		sys.exit(2)

	except:
			print("enter correct input")
		



#press ctrl-c to quit

def running():
	try:
		while True:
			banner()
			main_menu()
			colorchanger()
			print_options()
			choose_options()
	except KeyboardInterrupt:
		print('\n')

def main():
    pass

if __name__ == "__main__":
    main()

