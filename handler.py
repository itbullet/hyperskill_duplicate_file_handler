import os
import sys
import hashlib
# import argparse


# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("directory")
#     args = parser.parse_args()
#
#     if args.directory:
#         os.chdir(args.directory)
#         for root, dirs, files in os.walk('.'):
#             for name in files:
#                 print(os.path.join(root, name))
#             for name in dirs:
#                 print(os.path.join(root, name))
#################################################
def file_type():
    f_type = input('\nEnter file format:\n')
    if f_type:
        return f".{f_type}"
    return None


def sort_options():
    print("\nSize sorting options:\n"
          "1. Descending\n"
          "2. Ascending\n")
    while True:
        s_option = input('Enter a sorting option:\n')
        if s_option in ['1', '2']:
            return s_option
        else:
            print('\nWrong option\n')


def read_file(path_):
    with open(path_, 'rb') as file:
        return file.read()


def find_in_list_of_list(list_, index_):
    for sub_list in list_:
        if index_ in sub_list:
            return list_.index(sub_list)


def delete_files(file_list_):
    answer = input("\nDelete files?\n")
    if answer.lower() == 'no':
        return True
    elif answer.lower() == 'yes':
        while True:
            print("\nEnter file numbers to delete:")
            # files_delete_list = [int(x) for x in input().split()]
            try:
                files_delete_list = list(map(int, input().strip().split()))
            except ValueError:
                print("\nWrong format")
            else:
                if not len(files_delete_list) or (max(files_delete_list) > len(file_list_)):
                    print("\nWrong format")
                else:
                    space_sum = 0
                    for num in files_delete_list:
                        index = find_in_list_of_list(file_list_, num)
                        os.remove(file_list_[index][1])
                        space_sum += file_list_[index][2]
                    print(f'\nTotal freed up space: {space_sum} bytes')
                    break
        return True
    else:
        return False


def check_duplicates(files_dict_, s_type_):
    answer = input("\nCheck for duplicates?\n")
    if answer.lower() == 'no':
        return True
    elif answer.lower() == 'yes':
        i = 1
        file_list = []
        for key, val in sorted(files_dict_.items(), reverse=s_type_):
            hash_dict = {}
            if len(val) > 1:
                print(f'\n{key} bytes')
                for v in val:
                    md5 = hashlib.md5()
                    md5.update(read_file(v))
                    if md5.hexdigest() in hash_dict:
                        hash_dict[md5.hexdigest()].append(v)
                    else:
                        hash_dict[md5.hexdigest()] = [v]
            for key_, val_ in hash_dict.items():
                if len(val_) > 1:
                    print(f'Hash: {key_}')
                    for v in val_:
                        print(f'{i}. {v}')
                        file_list.append([i, v, key])
                        i += 1
        while True:
            if delete_files(file_list):
                break
            else:
                print("\nWrong choice")
        return True
    else:
        return False


def main():
    files_dict = {}
    args = sys.argv
    if len(args) < 2:
        print('Directory is not specified')
    else:
        f_type = file_type()
        s_type = sort_options()
        os.chdir(args[1])
        full_path = os.getcwd()
        for root, dirs, files in os.walk(full_path):
            for name in files:
                path = os.path.join(root, name)
                size = os.path.getsize(path)
                ext = os.path.splitext(path)
                if size in files_dict and (ext[1] == f_type or f_type is None):
                    files_dict[size].append(path)
                elif ext[1] == f_type or f_type is None:
                    files_dict[size] = [path]
        if s_type == '1':
            s_type = True
        elif s_type == '2':
            s_type = False
        for key, val in sorted(files_dict.items(), reverse=s_type):
            if len(val) > 1:
                print(f'\n{key} bytes')
                print(*val, sep='\n')
        while True:
            if check_duplicates(files_dict, s_type):
                break


if __name__ == '__main__':
    main()
