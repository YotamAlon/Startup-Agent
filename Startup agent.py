__author__ = 'Yotam'

from time import localtime
import ctypes
from tkinter import filedialog, Tk
import subprocess


def database_starter():
    try:
        database = open('database.dat', 'r+')
    except FileNotFoundError:
        database = open('database.dat', 'w+')
    if database.read() == '':
        database.seek(0)
        return True, 0
    else:
        database.seek(0)
        return False, len(list(database))


def program_loader(program):
    database = open('database.dat', 'r+')
    to_load = list(database)[program].split('$$')
    status = subprocess.Popen(['\"' + to_load[1] + '\"', to_load[2]])
    return status


def askyn(text):
    while True:
        yn = input(text)
        if yn == 'y':
            return True
        elif yn == 'n':
            return False
        else:
            print('I didn\'t understand')


def add_program():
    database = open('database.dat', 'r+')
    database.read()
    Tk().withdraw()
    filepath = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    filelst = filepath.split('/')
    assert filepath.split('/')[-1].split('.')[-1] == 'exe'
    num = database.write(filelst[-1].split('.')[0] + '$$' + '/'.join(filelst[:-1]) +'$$' +filelst[-1])
    database.flush()
    database.seek(0)
    n = len(list(database))
    database.close()
    return n


def display_programs():
    database = open('database.dat', 'r+')
    paths = list(database)
    for i in range(len(paths)):
        print(str(i + 1) + '. ' + paths[i].split('$$')[0])
    database.close()


def main():
    new = False
    new, size = database_starter()

    if new:
        more = True
        print('It seems that this is your first time using my services. please add your first program:')
        while more:
            size = add_program()
            more = askyn('Would you like to add another program? y/n')


    else:
        curtime = localtime()
        if curtime.tm_hour >= 2 and curtime.tm_hour <= 6:
            print('Good... What are you doing up sir?')
        elif curtime.tm_hour >= 7 and curtime.tm_hour <= 11:
            print('Good morning sir. How would you like to start you day?')
        elif curtime.tm_hour >= 12 and curtime.tm_hour <= 18:
            print('Good afternoon sir. What would you like to do?')
        elif curtime.tm_hour >= 19 and curtime.tm_hour <= 1:
            print('Good evening sir. What would you like to do?')

    display_programs()
    newprog = askyn("Would you like to add another program? y/n")
    while newprog:
        size = add_program()
        print('New options:')
        display_programs()
        newprog = askyn('Would you like to add another? y/n')

    while True:
        prognum = input("Enter program number:")
        try:
            program = int(prognum)-1
        except TypeError:
            print('Invalid program number.')
            continue
        if -1 < program < size:
            break
        print('Invalid program number.')
    status = program_loader(program)

    if status != 0:
        restart = askyn('Is everything alright sir? would you like to restart that program? y/n')
        if restart:
            status = program_loader(program)

    print('Well sir, have a good day! Hope to see you soon.')


main()
