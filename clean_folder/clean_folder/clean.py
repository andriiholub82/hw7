import shutil
import sys
from pathlib import Path


def read_folder(work_dir):
    """Функія приймає шлях до робочої папки й повертає список папок й файлів"""
    list_file = []
    list_folder = []
    if work_dir.exists():
        for item in work_dir.glob("**/*"):
            if item.is_file():
                list_file.append(item)
            if item.is_dir():
                list_folder.append(item)
        return list_file, list_folder
    else:
        return "Folder not find ..."


def create_dict(file):
    """Функія приймає текстовий файл, з якого сворюється словник,
    в якому: ключі - це папки, а значення - це список розширеннь файлів, які потрібно в ці папки перемістити"""
    result = {}
    with open(file, "r") as file:
        line = file.readlines()
        for item in line:
            item = item.replace('\n', '').replace(' ', '')
            result[item.split(":")[0]] = item.split(":")[1].split(",")

    return result


def create_folder(dict, work_dir):
    """Функія приймає шлях до робочої папки й словник, з якого сворюються папки в які будут переміщуватися сортовані файли"""
    for i in dict:
        if not work_dir.joinpath(i).exists():
            work_dir.joinpath(i).mkdir()


def sort_files(work_dir: Path):
    """Функція сортування файлів та видалення пустих папок"""
    ext_dict = create_dict("dict_dir.txt")
    list_file, list_folder = read_folder(work_dir)
    for file in list_file:
        file = Path(file)
        trans = normalize(file.name)
        if file.suffix in ext_dict['documents']:
            file.replace(work_dir / 'documents' / trans)
        elif file.suffix in ext_dict['music']:
            file.replace(work_dir / 'music' / trans)
        elif file.suffix in ext_dict['video']:
            file.replace(work_dir / 'video' / trans)
        elif file.suffix in ext_dict['images']:
            file.replace(work_dir / 'images' / trans)
        elif file.suffix in ext_dict['archives']:
            shutil.unpack_archive(file, work_dir / 'archives' / trans)
            file.replace(work_dir / 'archives' / file.name)
        else:
            if not work_dir.joinpath('other').exists():
                work_dir.joinpath('other').mkdir()
            file.replace(work_dir / 'other' / file.name)
    for folder in list_folder:
        folder = Path(folder)
        try:
            if folder.name not in ['music', 'video', 'images', 'archives', 'documents', 'other']:
                shutil.rmtree(folder)
        except Exception as err:
            continue
    return f"Files in {work_dir} were sorted successfully!"


CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_",
               "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")

TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def normalize(name):
    """Функція """
    return name.translate(TRANS)


def start_sorting():
    """Головна функція скрипта"""
    try:
        path = sys.argv[1]
    except IndexError:
        print("No folder. Input folder ...")
        path = input(
            'Enter path for folder: ')  # якщо користувач не ввів шлях, при запуску скрипта - то просимо його ввести зараз

    work_dir = Path(path)
    create_dict("dict_dir.txt")
    read_folder(work_dir)
    create_folder(create_dict("dict_dir.txt"), work_dir)
    print(sort_files(work_dir))


if __name__ == '__main__':
    start_sorting()
