import os
import shutil

def get_all_files_recursive(path_to_get):
    all_content = []
    all_folders = []
    queue = [ os.path.join(path_to_get, item) for item in os.listdir(path_to_get)]
    while queue:
        curr_item = queue.pop()
        if os.path.isfile(curr_item):
            all_content.append(curr_item)
        if os.path.isdir(curr_item):
            all_folders.append(curr_item)
            new_items = [os.path.join(curr_item, item) for item in os.listdir(curr_item)]
            queue.extend(new_items)
    return all_folders, all_content

def change_top_folder(folders, content, new_folder):
    new_folders = [os.path.join(new_folder, *f.split(os.path.sep)[1:]) for f in folders]
    new_content = [os.path.join(new_folder, *f.split(os.path.sep)[1:]) for f in content]
    return new_folders, new_content

def remove_all_files(path):
    if not os.path.exists(path):
        print("No such path")
        os.mkdir(path)
        return None
    shutil.rmtree(path)
    os.mkdir(path)
    return None

def move_recursive(path_src, path_dest):
    all_folders, all_content = get_all_files_recursive(path_src)
    new_folders, new_content = change_top_folder(all_folders, all_content, path_dest)
    for folder in new_folders:
        os.mkdir(folder)
    for file_old, file_new in zip(all_content, new_content):
        shutil.copy(file_old, file_new)

def process_files(path_src, path_dest):
    remove_all_files(path_dest)
    move_recursive(path_src, path_dest)

