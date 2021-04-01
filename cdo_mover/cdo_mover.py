import inspect, os, sys

def get_script_dir(follow_symlinks=True):
    if getattr(sys, 'frozen', False): # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

abspath = get_script_dir()
os.chdir(abspath)

dirlist = []
for filename in os.listdir():
    if os.path.isdir(os.path.join(filename)):
        dirlist.append(filename)

print('Путь к каталогу: ', abspath)
print()

if dirlist == []:
    print('В папке пусто')
else:
    print('Список внутренних каталогов: ', dirlist)
    print()

    for element in dirlist:
        os.chdir(element)
        student_dir_list = os.listdir()

        for file in student_dir_list:
            if file.endswith('.doc') or file.endswith('.docx') or file.endswith('.pdf'):
                split_name = file.split('.')
                student_name = str(element.replace('_assignsubmission_file_', '_') + str(student_dir_list.index(file)) + '.' + str(split_name[-1]))
                os.rename(file, student_name)
                print('Файл "', file, '" переименован в "', student_name, '"')
                new_files = os.listdir()

                for new_file in new_files:
                    if new_file.endswith('.doc') or new_file.endswith('.docx') or new_file.endswith('.pdf'):
                        os.replace(new_file, os.path.join(abspath, new_file))
                        print('Файл "', new_file, '" перемещён в корневую папку')
                    
        os.chdir(abspath)
    
        try:
            os.rmdir(element)
        except PermissionError:
            print('Папки не удалены, нужно запустить скрипт с правами администратора.')