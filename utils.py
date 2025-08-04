import os 

#Функии поиска файлов в системе
def search_one_word(user_text):
    founded_files = []
    other_dirs = []
    other_files = []
    for root, dir, files in os.walk(r'C:\Users') :
        try:
            found_in_this_dir = False
            for file in files:
                for word in user_text:
                    if word in file.lower():
                        full_path = os.path.join(root, file)
                        founded_files.append(f"{file} -- {full_path} \n")
                        found_in_this_dir = True
                        for i in dir:
                            other_dirs.append(i)
            if found_in_this_dir:
                for file in files:
                    is_target = any(word in file.lower() for word in user_text)
                    if not is_target:
                        other_files.append(file)
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

print(read_file_fu(r"C:\PythonVSCODE\venv\BotForStill\utils.py"))
