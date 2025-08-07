from code_tools import countup
from code_tools import folder_name_char_check
from os.path import exists
from os import makedirs
from sys import modules
import time
import log_tools, progressbar_control

"""Batch Folder Create
    By Michael Fulcher

    Send Donations to (recommended $1.50USD) -
    PayPal: mjfulcher58@gmail.com
    Bitcoin: 3DXiJxie6En3wcyxjmKZeY2zFLEmK8y42U
    Other options @ http://michaelfulcher.yolasite.com/
"""

# create series of folders

def folder_name_validity_check(a_name: str) -> bool:
    if len(a_name) > 0 and a_name[0] != ' ' and folder_name_char_check(a_name):
        return True
    else:
        return False

def name_spaces_check(a_name: str) -> bool:
    if len(a_name) > 1 and (a_name[0] == ' ' or a_name[-1] == ' '):
        return False
    else:
        return True

def makedir_n_iterate(a_folder_name: str) -> None:
    global w, success
    makedirs(a_folder_name)
    w += 1
    success += 1

def pick_destination() -> str:
    global w, success, folder_existed_count, ignore_FileExistsError
    while 1:
        destination_folder = input('Enter Folder (Full path) where you would like to create your new folders:')
        if destination_folder[-1] == '\\':
            destination_folder = destination_folder[:-1]
        if destination_folder[0] == ' ' or destination_folder[-1] == ' ':
            destination_folder = destination_folder.strip()
        if exists(destination_folder):
            print("Found: " + destination_folder)
            return destination_folder
        else:
            if exists(destination_folder[0:3]):  # check that drive exists
                print(f"\nFolder ({destination_folder}) does not exist.")
                n_seperator = input("Would you like to create this folder?\nNote: spaces at the beginning and end of folder names cannot be used, they will be removed.\n'Y' for Yes, any other key to start over:").upper()
                if n_seperator == 'Y':
                    path_list = destination_folder.split('\\')
                    length = len(path_list)
                    w = 1
                    start_num = length - 1
                    destination_folder = path_list[0]
                    ignore_FileExistsError = False
                    success = 0
                    folder_existed_count = 0
                    while w < length:
                        if not name_spaces_check(path_list[w]):
                            path_list[w] = path_list[w].strip()
                        if not folder_name_validity_check(path_list[w]):
                            return destination_folder
                        else:
                            destination_folder += f'\\{path_list[w]}'
                            if exists(destination_folder):
                                folder_existed_count += 1
                                w += 1
                            else:
                                if w == start_num:
                                    ignore_FileExistsError = True
                                if not ignore_FileExistsError:
                                    print("\nFolder {} does not exist.".format(destination_folder))
                                    n_seperator = input("Do you want to create?\n 'Y' for Yes, 'a' for create full path, any other command will restart the programe:").upper()
                                    if n_seperator == 'Y':
                                        makedir_n_iterate(destination_folder)
                                        log_tools.add_to_txt_log('Created ' + destination_folder, add_date = True)
                                    elif n_seperator == 'A':
                                        makedir_n_iterate(destination_folder)
                                        log_tools.add_to_txt_log('Created ' + destination_folder, add_date = True)
                                        ignore_FileExistsError = True
                                    else:
                                        return destination_folder
                                else:
                                    makedir_n_iterate(destination_folder)
                                    log_tools.add_to_txt_log('Created ' + destination_folder, add_date = True)
                    if w == length:
                        print(f"Created {success} folders, {folder_existed_count} Folders existed prior.")
                        print("Destination folder {} Created.".format(destination_folder))
                        return destination_folder
            else:
                print("Drive does not exist.")

def pick_seperator() -> str:
    while 1:
        n_seperator = input('\nEnter word seperator.\n"Space" may be used. But name cannot contain only "Spaces".\nPress "Enter" for default "_" (Underscore) or you want names to contain only numbers:')
        if n_seperator == '':
            return "_"
        else:
            if not folder_name_char_check(n_seperator):
                print("\nCharacter {} is not a valid character for files names.".format(n_seperator))
                continue
            else:
                return n_seperator

def blank_name_msg() -> str:
    return input("Name entered is blank, this will lead to your folder names being only numbers.\nPress 'Enter' if this is OK.\nEnter any other command to change the common name of Folders:")

def add_seperator(seperator: str, a_name: str) -> str:
    global spaces_list, job_pos
    list_length = len(spaces_list[job_pos])
    if list_length > 0:
        for i in countup(list_length):
            a_name = a_name[:spaces_list[job_pos][i]] + seperator + a_name[spaces_list[job_pos][i] + 1:]  # Replace spaces with seperator char.
    return a_name

# def remove_spaces(a_string: str) -> str:
#     if a_string[0] == ' ':
#         a_string = a_string[1:]
#     i = len(a_string) - 1
#     while a_string[i] == ' ':
#         i -= 1
#     return a_string[:i]

def pick_common_name(seperator: str) -> str:
    global spaces_list, job_pos
    while 1:
        common_name = input("\n'Spaces' will be replace with word seperator character, Can be left blank.\nBeginning and End characters cannot be 'Spaces'\nEnter common name of Folders:")
        length = len(common_name)
        if length > 0:
            if common_name[0] == " " or common_name[-1] == " ":
                common_name = common_name.strip()
            if common_name[0] != ' ':
                if not folder_name_char_check(common_name):
                    continue
                for i in countup(length):
                    if common_name[i] == ' ':
                        spaces_list[job_pos].append(i)
                if seperator != ' ':
                    common_name = add_seperator(seperator, common_name)
            else:
                if blank_name_msg() == '':
                    return common_name
            return common_name
        else:
            if blank_name_msg() == '':
                return common_name

def convert_string_to_int(a_num_str: str, a_string: str) -> int:
    try:
        new_int = int(a_num_str)
        if new_int < 0:
            print('Number must be positive.')
            return -1
    except ValueError:
        print(a_string + ' number must be a numerical value.')
        return -1
    return new_int

def pick_start_num() -> int:
    while 1:
        user_input = input('\nStart number:\n("Enter" for default "1"):')
        if user_input == '':
            return 1
        else:
            number = convert_string_to_int(user_input, 'Start')
            if number != -1:
                return number

'''Check validity of end number'''
def pick_end_num():
    global start_num
    while 1:
        end_num_string = input("\nEnter End number:")
        end_num_int = convert_string_to_int(end_num_string, "End")
        if end_num_int <= start_num[job_pos]:
            print('End number must be greater then start number.')
            continue
        else:
            return end_num_int, end_num_string

def generate_start_num_string() -> str:
    global end_num_string
    start_num_string = str(start_num[job_pos])
    working_num_length = len(start_num_string)
    length = len(end_num_string[job_pos])
    return '0' * (length - working_num_length) + start_num_string

def check_job_num() -> bool:
    global job_pos, job_list_length
    n_seperator = input("Select Job.\nEnter Job number:")
    job_pos = convert_string_to_int(n_seperator, 'Job')
    if n_seperator == -1:
        print('Job number does not exist')
        return False
    else:
        if job_pos > job_list_length:
            print('Job number does not exist')
            return False
        else:
            job_pos -= 1
            return True

def last_chars_of_name(pos: int) -> str:
    global seperator, add_seperator_at_end, start_num_string
    output = ''
    if add_seperator_at_end[pos]:
        output += seperator[pos]
    return output + start_num_string[pos]

def make_dir(destination: str) -> None:
    global ignore_FileExistsError, success, folder_existed_count
    try:
        makedirs(destination)
        success += 1
        return
    except FileExistsError:
        folder_existed_count += 1
        if not ignore_FileExistsError:
            while 1:
                n_seperator = input("\nFolder {} already exists.\n\t'A' - Ignore all these Errors and skip creation of prior existing folders.\n\t'S' - Skip Just this one.\n\t'X' - eXit the program:".format(destination)).upper()
                if n_seperator == 'A':
                    log_tools.add_to_txt_log('Folder {} exists and creation skipped (Ignore all activated).'.format(destination), add_date=True)
                    ignore_FileExistsError = True
                    return
                elif n_seperator == 'S':
                    log_tools.add_to_txt_log('Folder {} exists and creation skipped (one time).'.format(destination), add_date=True)
                    return
                elif n_seperator == 'X':
                    log_tools.add_to_txt_log('Folder {} exists and user quit.'.format(destination), add_date=True)
                    raise SystemExit
        else:
            log_tools.add_to_txt_log('Folder {} exists and creation automatically skipped.'.format(destination), add_date=True)

def make_numbered_dir(a_folder: str) -> None:
    global pos, start_num, start_num_string, use_progress_bar
    make_dir(a_folder)
    if use_progress_bar:
        global total
        pos += 1
        progressbar_control.update_progressbar(pos, total)
    start_num[job_pos] += 1
    start_num_string[job_pos] = str(start_num[job_pos])

if __name__ == '__main__':
    global use_progress_bar, ignore_FileExistsError, w, success, folder_existed_count, end_num, start_num, spaces_list, job_pos
    log_tools.script_id = 'Create_Numbered_Folder_Series'
    log_tools.run_date = time.strftime('%d-%m-%Y', time.localtime())
    log_tools.initialize(False)
    del time
    job_pos = 0

    '''Source: https://stackoverflow.com/questions/3431498/what-code-can-i-use-to-check-if-python-is-running-in-idle'''
    if 'idlelib.run' in modules:
        use_progress_bar = False
    else:
        progressbar_control.setup_progressbar()
        use_progress_bar = True

    print('Create Numbered Folder Series Script\n\tBy Michael Fulcher\nSend Donations to - PayPal: mjfulcher58@gmail.com or Bitcoin: 3DXiJxie6En3wcyxjmKZeY2zFLEmK8y42U\nOther donation options @ http://michaelfulcher.yolasite.com/\n\n')
    destination_folder = list()
    destination_folder.append(pick_destination())

    seperator = list()
    seperator.append(pick_seperator())
    common_name, spaces_list = [], []
    spaces_list.append(list())

    common_name.append(pick_common_name(seperator[job_pos]))
    print("Common name set: " + common_name[job_pos])
    add_seperator_at_end = list()
    add_seperator_at_end.append(True)

    global start_num_string

    start_num = list()
    start_num.append(pick_start_num())

    end_num = list()
    end_num_string = list()
    return_tuple = pick_end_num()
    end_num.append(return_tuple[0])
    end_num_string.append(return_tuple[1])

    leading_zero = list()
    leading_zero.append(True)

    global job_list_length
    batch_mode = False
    start_num_string = list()
    start_num_string.append(generate_start_num_string())
    destination_folder[job_pos] += '\\'
    length = len(end_num_string[job_pos])

    while 1:
        output = "\n---Confirmation Menu---\nYou want to create:"
        if batch_mode:
            job_list_length = len(end_num_string)
            output += '\nJob #\tCommon Name\tDestination:\tStart:\tEnd\te.g.:'
            for i in countup(job_list_length):
                output += '\n{}\t{}\t\t{}\t{}\t{}\t{}{}{}'.format(str(i + 1), common_name[i], destination_folder[i], start_num_string[i], end_num_string[i], destination_folder[i], common_name[i], last_chars_of_name(i))
        else:
            job_list_length = 1
            output += '\nFolders'
            if common_name[job_pos] != '':
                output += " named " + common_name[job_pos]
            output += " from {} to {} inside Folder {}.\n\t e.g. {}{}{}".format(start_num_string[job_pos], end_num_string[job_pos], destination_folder[job_pos], destination_folder[job_pos], common_name[job_pos], last_chars_of_name(job_pos))
        output += "\n\nCommands:\n\t'p' - Change the seperator character.\n\t'n' - Change the common name.\n\t's' - Change start number.\n\t'f' - Change end number."
        if batch_mode:
            output += "\n\t'b' - Add another job.\n\t'r' - Remove a job."
        else:
            output += "\n\t'b' - Enter batch creation mode."
        n_seperator = input("{}\n\t'e' - Enable/Dissable seperator at end.\n\t'z' - Enable/Dissable leading zero.\n\t'c' - Confirm current settings and Create Folders.\n\t'x' - eXit the program\nThen 'Enter' to confirm:".format(output)).upper()
        if n_seperator == 'C':
            break
        elif n_seperator == 'E':
            if batch_mode and check_job_num() is False:
                continue
            add_seperator_at_end[job_pos] = not add_seperator_at_end[job_pos]
        elif n_seperator == 'P':
            if batch_mode and check_job_num() is False:
                continue
            seperator[job_pos] = pick_seperator()
            common_name[job_pos] = add_seperator(seperator[job_pos], common_name[job_pos])
        elif n_seperator == 'N':
            if batch_mode and check_job_num() is False:
                continue
            common_name[job_pos] = pick_common_name(seperator[job_pos])
        elif n_seperator == 'S':
            if batch_mode and check_job_num() is False:
                continue
            start_num[job_pos] = pick_start_num()
            while start_num[job_pos] >= end_num[job_pos]:
                print('Start number must be smaller than end number.')
                start_num[job_pos] = pick_start_num()
            if leading_zero[job_pos] or length > len(start_num_string[job_pos]):
                start_num_string[job_pos] = generate_start_num_string()
        elif n_seperator == 'F':
            if batch_mode and check_job_num() is False:
                continue
            return_tuple = pick_end_num()
            end_num[job_pos] = return_tuple[0]
            end_num_string[job_pos] = return_tuple[1]
            length = len(end_num_string[job_pos])
            if leading_zero[job_pos] and length != len(start_num_string[job_pos]):
                start_num_string[job_pos] = generate_start_num_string()
        elif n_seperator == 'Z':
            if batch_mode and check_job_num() is False:
                continue
            leading_zero[job_pos] = not leading_zero[job_pos]
            if leading_zero[job_pos]:
                start_num_string[job_pos] = generate_start_num_string()
            else:
                start_num_string[job_pos] = str(start_num[job_pos])
        elif n_seperator == 'B':
            batch_mode = True
            job_pos = len(start_num_string)
            destination_folder.append(pick_destination())
            seperator.append(pick_seperator())
            spaces_list.append(list())
            common_name.append(pick_common_name(seperator[job_pos]))
            print("Common name set: " + common_name[job_pos])
            add_seperator_at_end.append(True)
            start_num.append(pick_start_num())
            return_tuple = pick_end_num()
            end_num.append(return_tuple[0])
            end_num_string.append(return_tuple[1])
            leading_zero.append(True)
            start_num_string.append(generate_start_num_string())
            destination_folder[job_pos] += '\\'  # check use of length var
        elif n_seperator == 'R':
            if batch_mode:
                if check_job_num():
                    destination_folder.pop(job_pos)
                    seperator.pop(job_pos)
                    spaces_list.pop(job_pos)
                    common_name.pop(job_pos)
                    add_seperator_at_end.pop(job_pos)
                    start_num.pop(job_pos)
                    end_num.pop(job_pos)
                    start_num_string.pop(job_pos)
                    end_num_string.pop(job_pos)
                    leading_zero.pop(job_pos)
                    print("Removed Job no " + n_seperator)
                    if len(seperator) == 1:
                        batch_mode = False
                        job_pos = 0
            else:
                print('You have not enabled batch mode')
        elif n_seperator == 'X':
            log_tools.add_to_txt_log('User quit from confirmation menu.', add_date=True)
            raise SystemExit

    for i in countup(job_list_length):
        destination_folder[i] += common_name[i]
        if add_seperator_at_end[i]:
            destination_folder[i] += seperator[i]

    ignore_FileExistsError = False
    success = 0
    folder_existed_count = 0

    print('\nCreating Folders!')
    for i in countup(len(start_num)):
        job_pos = i
        log_tools.tprint('Creating Folders ' + destination_folder[job_pos])
        if use_progress_bar:
            global total, pos
            progressbar_control.bar.start()
            total = end_num[job_pos] - start_num[job_pos] + 2
            pos = 0
        if leading_zero[i]:
            start_str = str(start_num[job_pos])
            while start_num[i] <= end_num[i]:
                make_numbered_dir(destination_folder[i] + start_num_string[i])
                working_num_length = len(start_num_string[i])
                if working_num_length < length:
                    start_num_string[i] = '0' * (length - working_num_length) + start_num_string[i]
            log_tools.add_to_txt_log(
                'Completed process for {} folders {} to {}'.format(destination_folder[job_pos], start_str, str(
                    end_num[job_pos])), add_date=True)
        else:
            start_str = str(start_num[job_pos])
            while start_num[i] <= end_num[i]:
                make_numbered_dir(destination_folder[i] + start_num_string[i])
            log_tools.add_to_txt_log(
                'Completed process for {} folders {} to {}'.format(destination_folder[job_pos], start_str,  str(
                    end_num[job_pos])), add_date=True)

    log_tools.tprint("Created {} folders, {} Folders existed prior.".format(str(success), str(folder_existed_count)))
