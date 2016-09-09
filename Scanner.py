'''
FileSorter is a very simple program for sorting files...work in progress
'''
import os, sys
from Utility import get_limited_file_type, print_available_hash_algorithms
from FileInfoOrg import FileTypeSet

def scan_folders(path, debug = False, ignore = None):
    file_types_dict = dict()
    for (dirpath, dirnames, filenames) in os.walk(path):
        if debug:
            print "dirpath: " + str(dirpath)
            print "dirnames: " + str(dirnames)
        for f in filenames:
            f_name = os.path.join(dirpath, f)
            f_type, f_less_type = get_limited_file_type(f_name)
            if f_less_type is not None and f_less_type not in file_types_dict:
                file_types_dict[f_less_type] = FileTypeSet(f_less_type, f_type)
            elif f_less_type is None and f_type not in file_types_dict:
                file_types_dict[f_type] = FileTypeSet(f_type)
            file_types_dict[f_type if f_less_type is None else f_less_type].add_file(f_name)
    return file_types_dict

def view_data(file_types_dict):
    valid_input = {1:'print all keys', 2:'select value',3:'print selected files',4:'print help',5:'Find duplicated',0:'Exit'}
    for k,v in valid_input.items():
        print (str(k) + ":" + v)
    select_value = None
    while True:
        print("==========")
        choice = int(raw_input())
        if choice is 1:
            i = 0
            for k,v in file_types_dict.items():
                print(str(i) + " " + k + " " + str(len(v.hash_file_dict)))
                i += 1
        elif choice is 2:
            num = int(raw_input())
            select_value = file_types_dict.values()[num]
        elif choice is 3:
            for k,v in select_value.hash_file_dict.items():
                print(k)
                for vv in v:
                    print(vv.file_path)
        elif choice is 4:
            for k,v in valid_input.items():
                print (str(k) + ":" + v)
        elif choice is 5:
            for k,v in file_types_dict.items():
                for kk, vv in v.hash_file_dict.items():
                    if len(vv) > 1:
                        print(str(k) +  " " + str(kk))
                        for vvv in vv:
                            print(vvv.file_path)
        elif choice is 0:
            return
            
            

if __name__ == '__main__':
    if(len(sys.argv) == 2):
        view_data(scan_folders(sys.argv[1]))
    else:
        print "len args " + str(len(sys.argv))
        for a in sys.argv:
            print a
    