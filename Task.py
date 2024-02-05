import filecmp
import os
import shutil
import sys
import time

folder_path = sys.argv[1]
replica_path = sys.argv[2]
logfile_path = folder_path + 'logfile.txt'
with open(logfile_path, 'w'):
    pass

while True:
    if not os.path.exists(logfile_path):  # in case if logfile was deleted while script is running
        print("Can't find logfile, creating...")
        with open(logfile_path, 'w'):
            pass

    try:
        os.mkdir(replica_path)
    except FileExistsError:
        pass

    folder_file_list = os.listdir(folder_path)  # takes list of files in folder
    for file in folder_file_list:
        replica_file_path = replica_path + file  # creates full file path from replica folder
        folder_file_path = folder_path + file  # creates full file path from original folder
        if os.path.isfile(folder_file_path):  # if chosen file is file type
            if file == 'logfile.txt':  # skip logfile to copy
                continue
            if not os.path.exists(replica_file_path) or not filecmp.cmp(folder_file_path, replica_file_path):
                shutil.copyfile(folder_file_path, replica_file_path)  # if chosen file doesnt exist or different from the chosen one, copying it
                with open(logfile_path, 'a') as logfile:
                    logfile.write('Copied file ' + folder_file_path + ' in ' + replica_path + '\n')
                print('Copied file ' + folder_file_path + ' in ' + replica_path)

        elif os.path.isdir(folder_file_path):  # if chosen file is folder type
            compare = filecmp.dircmp(folder_file_path, replica_file_path)
            if not os.path.exists(replica_file_path):  # if chosen folder doesnt exists in replica folder
                shutil.copytree(folder_file_path, replica_file_path)
                with open(logfile_path, 'a') as logfile:
                    logfile.write('Copied folder ' + folder_file_path + ' in ' + replica_path + '\n')
                print('Copied folder ' + folder_file_path + ' in ' + replica_path)
            elif compare.left_only or compare.right_only or compare.diff_files:  # if chosen folder not the same with folder in replica directory (including subfolders)
                shutil.rmtree(replica_file_path)  # we use this way in case if content of the folders differ
                shutil.copytree(folder_file_path, replica_file_path)  # it deletes folder in replica directory and swap it with original folder
                with open(logfile_path, 'a') as logfile:
                    logfile.write('Removed folder ' + replica_file_path + ' from ' + replica_path + '\n')
                    logfile.write('Copied folder ' + folder_file_path + ' in ' + replica_path + '\n')
                print('Removed folder ' + folder_file_path + ' from ' + replica_path)
                print('Copied folder ' + folder_file_path + ' in ' + replica_path)


    replica_file_list = os.listdir(replica_path)  # now we should check if there are any files which were renamed and not exist in original directory
    for file in replica_file_list:                # for example in case if they were renamed
        original_file_path = folder_path + file
        replica_file_path = replica_path + file
        if not os.path.exists(original_file_path):
            if os.path.isdir(replica_file_path):
                shutil.rmtree(replica_file_path)
                with open(logfile_path, 'a') as logfile:
                    logfile.write('Removed folder ' + replica_file_path + ' from ' + replica_path + '\n')
                print('Removed folder ' + replica_file_path + ' from ' + replica_path)
            elif os.path.isfile(replica_file_path):
                os.remove(replica_file_path)
                with open(logfile_path, 'a') as logfile:
                    logfile.write('Removed file ' + replica_file_path + ' from ' + replica_path + '\n')
                print('Removed file ' + replica_file_path + ' from ' + replica_path)


    try:
        time.sleep(float(sys.argv[3]))  # sleep for time, which was specified as 3rd argument
    except ValueError:
        print("Error, can't convert third argument into number")


