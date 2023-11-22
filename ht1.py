import os
from pathlib import Path
import shutil
import re
import sys

content_types = {
    'images':  ('JPEG', 'PNG', 'JPG', 'SVG'),
    'video': ('AVI', 'MP4', 'MOV', 'MKV'),
    'docs': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives': ('ZIP', 'GZ', 'TAR')}

content_types_files = {
    'images':  [],
    'video': [],
    'docs': [],
    'music': [],
    'archives': [],
    'unknown': []
}

known_extens_found = []
unknown_extens_found = []

alph = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
        'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
        'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'YO',
        'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
        'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
        'Ц': 'C', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
        'Ю': 'U', 'Я': 'YA'}

path = r'd:\new\1'

def normalize(name):
    name = name.translate(str.maketrans(alph))
    name = re.sub(r'[^a-zA-Z0-9]', '_', name)
    return name

def delete_empty_folders(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder, topdown=False):
        # Copy the list of directories before deletion
        dirs_before_deletion = dirnames.copy()
        for subdir in dirs_before_deletion:
            subdir_path = os.path.join(dirpath, subdir)
            print(subdir_path)
            try:
                os.rmdir(subdir_path)
                print(f"Deleted empty folder: {subdir_path}")
            except OSError as e:
                print(f"Error deleting folder {subdir_path}: {e}")


def sort_content(path):


    if len(sys.argv) < 2:
        print("No required parameter")
    else:
        root_dir = sys.argv[1]
        root_dir = Path(root_dir)

    path_obj = Path(path)

    # in this loop we operate only of we find a file. After all files are finished we go to another loop where we iterate throuh
    # all folders recursively
    for i in os.listdir(path_obj):
        if os.path.isfile(path_obj / i):
            file_name, file_extension = (path_obj / i).stem, (path_obj / i).suffix
            normalized_name = normalize(file_name)
            normalized_name += file_extension
            os.rename(path_obj / i, path_obj / normalized_name)
            file_extension = file_extension[1:]

            # we are iterating through all content_types known extensions and if our "file_extension" is known_extens_found
            # we put it in the content_types_files[file_type] dict else we put it to "unknown"
            for file_type, extension in content_types.items():
                if file_extension.upper() in extension:
                    content_types_files[file_type] = content_types_files.get(file_type, []) + [normalized_name[:-4].upper()]
                    if file_extension.lower() not in known_extens_found:
                        known_extens_found.append(file_extension.lower())
                    dest_folder = root_dir / file_type
                    dest_folder.mkdir(exist_ok=True, parents=True)
                    shutil.move(path_obj/ normalized_name, dest_folder/ normalized_name)
                    if file_extension.upper() in content_types['archives']:
                        print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
                        os.chdir(dest_folder)
                        shutil.unpack_archive(normalized_name, dest_folder/normalized_name[:-4], 'zip')
                        os.chdir(dest_folder/normalized_name[:-4])
                        ss = os.getcwd()
                        print(ss)
                        print(dest_folder, normalized_name)
                        os.remove(dest_folder/ normalized_name)
                    break
            else:
                content_types_files['unknown'] = content_types_files.get('unknown', []) + [file_name.upper()]
                if file_extension.lower() not in unknown_extens_found:
                    unknown_extens_found.append(file_extension.lower())
        else:
            if i in content_types.keys():
                continue
            else:
                print(f'we are moving inside to {path}\\{i}')
                normalized_name = normalize(i)
                os.rename(path_obj / i, path_obj / normalized_name)
                sort_content(path + '\\' + normalized_name)


    return content_types_files, known_extens_found, unknown_extens_found


print(sort_content(sys.argv[1]))
delete_empty_folders(sys.argv[1])
