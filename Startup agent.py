__author__ = 'Yotam'

from time import localtime
import ctypes
from tkinter import filedialog, Tk
import os

def database_starter():
    try:
        database = open('database.dat', 'r+')
    except FileNotFoundError:
        database = open('database.dat', 'w+')
    if database.read() == '':
        print(database.read() + ' == \'\'')
        return database, True
    elif database.read() != '':
        print(database.read() + ' != \'\'')
        return database, False
    else:
        print('WTF?')

def program_loader(database, program):
    paths = list(database)
    status = os.spawnl('P_WAIT', paths[program-1].split()[1])
    return status

def answeryn(text):
    while True:
        yn = input(text)
        if yn == 'y':
            return True
        elif yn == 'n':
            return False
        else:
            print('I didn\'t understand')

def add_program(database):
    Tk().withdraw()
    filepath = filedialog.askopenfilename() # show an "Open" dialog box and return the path to the selected file
    assert filepath.split('/')[-1].split('.')[-1] == 'exe'
    num = database.write(filepath.split('/')[-1].split('.')[0] + '? ?' + filepath + '\n')
    print(num)
    database.flush()

def display_programs(database):
    paths = list(database)
    print(database.readlines())
    for i in range(len(paths)):
        print(str(i+1) + '. ' + paths[i].split('? ?')[0])

def main():

    new = False
    database, new = database_starter()

    if new:
        more = True
        print('It seems that this is your first time using my services. please add your first program:')
        while more:
            add_program(database)
            more = answeryn('Would you like to add another program? y/n')


    else:
        curtime = localtime()
        if curtime.tm_hour >= 2 and curtime.tm_hour <= 6:
            print('Good... What are you doing up sir?')
        elif curtime.tm_hour >= 7 and curtime.tm_hour <= 11:
            print('Good morning sir. How would you like to start you day')
        elif curtime.tm_hour >= 12 and curtime.tm_hour <= 18:
            print('Good afternoon sir. What would you like to do?')
        elif curtime.tm_hour >= 19 and curtime.tm_hour <= 1:
            print('Good evening sir. What would you like to do?')

    display_programs(database)
    newprog = answeryn("Would you like to add another program? y/n")
    while newprog:
        add_program(database)
        print('New options:')
        display_programs(database)
        newprog = answeryn('Would you like to add another? y/n')

    while True:
        program = input("Enter program number:")
        if isinstance(program, int) and program > 0 and program < len(list(database)):
            break
        print('Invalid program number.')
    status = program_loader(database, program)

    if status != 0:
        restart = answeryn('Is everything alright sir? would you like to restart that program? y/n')
        if restart:
            status = program_loader(database, program)

    print('Well sir, have a good day! Hope to see you soon.')

main()
