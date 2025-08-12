import os 

#Функии поиска файлов в системе
def search_one_word(user_text):
    founded_files = []
    other_dirs = []
    other_files = []
    for root, dir, files in os.walk(r'C:\Users') :
        try:
            
            for file in files:
                for word in user_text:
                    if word in file.lower():
                        full_path = os.path.join(root, file)
                        founded_files.append(f"{file} -- {full_path} \n")   #возвращает только founded_files
            #             found_in_this_dir = True
            #             for i in dir:
            #                 other_dirs.append(i)
            # if found_in_this_dir:
            #     for file in files:
            #         is_target = any(word in file.lower() for word in user_text)
            #         if not is_target:
            #             other_files.append(file)
        except PermissionError:
            print("Недостаточно прав")
    
    return founded_files, other_dirs, other_files
    

def search_many_words(user_text):
    founded_files = []
    for root, dir, files in os.walk(r'C:\Users') :
        try:
            for file in files:
                for word in user_text:
                    if word in file.lower():
                        full_path = os.path.join(root, file)
                        founded_files.append(f"{file} -- {full_path} \n")
        except PermissionError:
            print("Недостаточно прав")
    return founded_files


#Фунция прочтения файлов 
def read_file_fu(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        text_extensions = ['.txt', '.py', '.js', '.html', '.css', '.md', '.json', '.xml', '.csv']
        if ext in text_extensions:
            with open(file_path, 'r', encoding="utf-8") as file:
                return file.read()
        else:
            return f"Бинарный файл {ext} - содержимое не может быть отображено как текст"
        
    except Exception as e:
        print('Ошибка  чтения файла')

#Функия отправки файла в боте

# print(read_file_fu(r"C:\PythonVSCODE\venv\BotForStill\utils.py"))

#Просмотрт содержимого в папке

def show_files(user_text="", default_path=r'C:\\'):
    if user_text.strip():
        search_path = os.path.join(default_path, user_text.strip())
    else:
        search_path = default_path
    
    files_list = []
    try:
        if os.path.exists(search_path):
            items = os.listdir(search_path)
            for item in items:
                full_path = os.path.join(search_path, item)
                if os.path.isdir(full_path):
                    files_list.append(f"📁 {item}")
                else:
                    files_list.append(f"📄 {item}")
        else:
            files_list.append("Путь не существует")
    except PermissionError:
        files_list.append("ГНедостаточно прав")
    except Exception as e:
        files_list.append(f"Ошибка: {e}")
    
    return files_list


def find(directory, find_file):
    results = []
    
    for root, dirs, files in os.walk(rf'C:\{directory}'):
        try:
            if "-f" in find_file:
                search_words = [word for word in find_file if word != "-f"]
                for filename in files:
                    if filename in search_words:
                        full_path = os.path.join(root, filename)
                        results.append(f"{filename} ----- {full_path}")
            else:
                for filename in files:
                    for word in find_file:
                        if word.lower() in filename.lower(): 
                            full_path = os.path.join(root, filename)
                            results.append(f"{filename} ----- {full_path}")
                            break

                for dirname in dirs:
                    for word in find_file:
                        if word.lower() in dirname.lower():
                            full_path = os.path.join(root, dirname)
                            results.append(f"[ПАПКА] {dirname} ----- {full_path}")
                            break
                            
        except PermissionError:
            results.append("Недостаточно прав для некоторых папок")
            continue
    
    return results if results else ["Ничего не найдено"]
# print(search_one_word("nude"))