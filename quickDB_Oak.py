from genericpath import isdir
import os,sys
import webbrowser
from time import sleep


ls = '[QuickDB]-'
ls_error = '[QuickDB - Error]-'
folder_name = 'QuickDB'
'''in QuickDB there are space and database(tables of data)
spaces are locus of existence of databases, they store different
databases accessible through shell (There is no interface yet)
QuickDB is developed by using Python and HTML/CSS
'''
def check_path():
    current_path = os.getcwd()
    current_path = current_path.split('/')
    if current_path[-1] == folder_name:
        return True
    else:
        return False


def create_space():
    test = check_path()
    if test == True:
        display = ls + ' Enter the name of the space you wish to create:'
        space = input(display)

        flag = True
        spaces = os.listdir(os.getcwd())
        if space in spaces:
            print(ls_error,'This space already exist! Choose a different one.')
            del spaces
            create_space()
        elif not space:
            print(ls_error,'The name cannot be an empty string.')
            create_space()
        elif flag:
            for letter in space:
                if letter != ' ':
                    flag = False
                    break
            if flag == True:
                print(ls_error,'the name cannot have just empty chars!')
                create_space()
        os.mkdir(space)
        os.chdir(space)
        os.mkdir('Databases')
        new_path = os.path.join(os.getcwd(),'Databases')
        os.chdir(new_path)
        select_space()
        #reasons for the program to raise error:
        #space already exist fixed
        #space cannot be an empty name fixed
        #space cannot be made of just spaces ' ' fixed
    else:
        print(ls_error,'Error while locating the correct folder, make sure the app is in ../', folder_name)
      
create_space()
def select_space(): 
    if check_path() == True:
        folderstmp = os.listdir(os.getcwd())
        folders = []
        for folder in folderstmp:
            if isdir(folder) == 1:
                folders.append(folder)
        print(ls,'Enter one of the following spaces you wish to use:')
        for folder in folders:
            print('-',folder)
        select_space = input('>')
        while select_space not in folders and select_space.lower() != '/bye':
            print(ls_error,'this space does not exist, please enter an existing space.')
            for folder in folders:
                print('-', folder)
            select_space = input('>')
        if select_space.lower() == '/bye':
            print(ls,'cheers.')
            print('----------> Raffaele Palumbo.')
            sys.exit()
        else:
            use_space(select_space)
    else:
        print(ls_error,'It seems that the folder is not correct, do not move the app outside its native folder.')

def use_space(space):
    print(ls,'You are in [', space, '] space.')
    command = input('>')
    main_command, second_part = check_command(command)
    while main_command.lower() != '/bye' and main_command.lower() != '/return':
        if main_command.lower() == '/create_db':
            if second_part == '':
                print(ls_error,'the database should have a name! I will call it "Dummy".')
                second_part = 'Dummy'
                second_part = second_part + '.txt'
                main_command = create_database(second_part,space)
            elif second_part.lower() == '/create_db' or '/create_db' in second_part:
                print(ls_error,'You cannot use this name.')
            elif second_part.lower() == space:
                print(ls_error,space,'already exists, you cannot have a database that has the name of your space.')
            else:
                try: os.chdir(os.path.join(os.getcwd(),space,'Databases'))
                except: pass
                main_command = create_database(second_part +'.txt',space)
                #create_HTML(second_part)
        command = input('>')
        main_command, second_part = check_command(command)

    if main_command.lower() == '/bye':
        print(ls,'cheers.')
        print('----------> Raffaele Palumbo.')
        sys.exit()
    if main_command.lower() == '/return':
        select_space()

def create_database(fileName,which_space):
    #os.chdir(os.path.join(os.getcwd(),which_space,'Databases'))
    try: open(fileName,'x')
    except: print(ls_error,'it seems this database already exists!'); select_space()
    actual_command = main(fileName)
    if actual_command:
        return actual_command

def get_space():
    current_path = os.getcwd()
    current_path = current_path.split('/')
    return current_path[-2]

def create_row(field1,field2,filename):
    table = open(filename,'a')
    l = db_graphic('straight_line',10,'return_on')
    format = field1 + '||' + field2 +'\n'
    table.write(format)
    print(ls + 'Row successfully added!')
    table.close()
    main(filename)

def show_table(filename):
    filename = open(filename)
    row = filename.readline()
    while row:
        print(row)
        db_graphic('straight_line')
        row = filename.readline()

def db_graphic(which, value = 15, mode = 'return_off'):
    if which == 'straight_line' and mode =='return_off':
        for i in range(value):
            print('-', end = '')
        print('')
    if which == 'straight_line' and mode == 'return_on':
        line = ''
        for i in range(value):
            line += '-'
        line = line + '\n'
        return line

def check_command(command):
    command_structure = command.split()
    main_command = command_structure[0]
    other = ''
    for s in range(1,len(command_structure)):
        other += command_structure[s]    
    return main_command,other

def main(fileName):
    print(ls,'you are manipulating the current database:', fileName, 'in', get_space())
    tmp = fileName
    fileName = fileName.split('.')
    #display = fileName.rstrip('.txt') + '>'
    display = fileName[0] + '>'
    fileName = tmp
    command = input(display)
    actual_command, second_part = check_command(command)
    while actual_command.lower() != '/return' and actual_command.lower() != '/bye':
        if actual_command.lower() == '/return':
            use_space(get_space())
        if actual_command.lower() == '/visualize':
            pass
        if actual_command.lower() == '/add_row':
            try: 
                database = open(fileName,'a')
                rows = second_part.split(',')
                format_0 = rows[0] + '|' + rows[1] + '\n'
                format_1 = ''
                final_lenght = len(rows[0]) + len(rows[1])
                for i in range(final_lenght):
                    format_1 += '-'
                format_1 = format_1 + '\n'
                database.write(format_0)
                database.write(format_1)
                print(ls,'Success!')
                database.close()
            except: print(ls_error,'Could not add any row, are you sure the format is correct?')

        if actual_command.lower() == '/delete_row':
            pass
        if actual_command.lower() == '/search_data':
            pass
        if actual_command.lower() == '/show_database':
            database = open(fileName)
            database.close()

        if actual_command.lower() == '/destroy_database':
            database = open(fileName)
            count_lines = 0
            while database.readline():
                count_lines += 1
            print(ls,'Are you sure? Do you really want to delete',database.name, 'in', get_space(),'?')
            print(ls,'The database contains', round(count_lines/2), 'elements.')
            print(ls,'Shall I proceed?(Y/n)')
            userInput = input('>')
            if userInput.lower() == 'y':
                database = open(fileName,'w')
                database.close()
                print(ls,'the database has firstly been cleaned.')
                sleep(2)
                try: 
                    os.remove(fileName)
                    print(ls,'Database has been destroyed.')
                except:
                    print(ls_error,'Could not destroy the database.')
                os.chdir('.')
                use_space(get_space())
            else:
                print(ls,'You decided to keep the database',fileName)
            database.close()
        command = input(display)
        actual_command, second_part = check_command(command)
        if actual_command.lower() == '/bye':
            print(ls,'cheers.')
            print('----------> Raffaele Palumbo.')
            sys.exit()
########HTML/CSS visualization
def create_HTML(space):
    top_message = '<!--Fully created in QuickDB app \nAuthor:Raffaele Palumbo. -->\n'
    html_page = space + '_Visualization.html'
    try:
        try:    file = open(html_page,'x'); file.close()
        except: print(ls_error,space,'visualization already exists.')
        file = open(html_page,'w')
        html_code = ['<html>','      <head>','      </head>','      <body>','      </body>','</html>']
        file.write(top_message)
        for element in html_code:
            file.write(element + '\n')
        file.close()
        _color_ = 'navy' #Default color
        style_line = 'style = color:' + _color_ +';>'
        space = space.split('.')
        top_line = '<h1 ' + style_line + space[0] + ' Visualization.' + '</h1>'
        top_message = [top_line]
        bottom_message = ['<hr>','<p><em>HTML generated in Python.</em></p>']
        try:
            #4 should be for <head></head>
            #7 should be for <body></body>
            write_HTML(html_page,4,top_message)
            write_HTML(html_page,7,bottom_message)
        except:
            print(ls_error,'An error occurred while writing HTML.')
    except:
        print(ls_error,'An error occurred while creating the visualization.')
        
def write_HTML(htmlFile,which_line,html_code):
    try: file= open(htmlFile,'r')
    except: print(ls_error,'There was an error while opening:',htmlFile)
    file.close()
    file = open(htmlFile,'r')
    lines = file.readlines()
    for html in html_code:
        html = html + '\n'
        lines.insert(which_line,html)
        which_line += 1
    file.close()
    file = open(htmlFile,'w')
    for html in lines:
        file.write(html)
    file.close()

def update_HTML():
    pass

create_database('universe')