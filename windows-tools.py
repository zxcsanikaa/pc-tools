import os
import platform
import socket
import psutil
import subprocess
import time
from colorama import init, Fore, Back, Style
import msvcrt  # Для работы с клавиатурой в Windows

init()  # Инициализация colorama для цветного вывода в CMD

# Настройка цветов
BACKGROUND_COLOR = Back.BLUE
TEXT_COLOR = Fore.WHITE
HIGHLIGHT_COLOR = Fore.YELLOW + Back.BLUE + Style.BRIGHT
NORMAL_COLOR = TEXT_COLOR + BACKGROUND_COLOR
CLEAR_SCREEN = lambda: os.system('cls')

def set_console_title(title):
    """Устанавливает заголовок окна консоли"""
    os.system(f'title {title}')

def get_ip_address():
    """Получает IP-адрес компьютера"""
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except:
        return "Не удалось получить IP-адрес"

def get_pc_name():
    """Получает имя компьютера"""
    return socket.gethostname()

def get_os_info():
    """Получает информацию об операционной системе"""
    return f"{platform.system()} {platform.release()} (Версия: {platform.version()})"

def get_cpu_info():
    """Получает информацию о процессоре"""
    return platform.processor()

def get_ram_info():
    """Получает информацию об оперативной памяти"""
    ram = psutil.virtual_memory()
    return f"Всего: {round(ram.total / (1024**3), 2)} GB | Используется: {round(ram.used / (1024**3), 2)} GB | Свободно: {round(ram.free / (1024**3), 2)} GB"

def get_disk_info():
    """Получает информацию о дисках"""
    disks = []
    for part in psutil.disk_partitions(all=False):
        if 'cdrom' in part.opts or part.fstype == '':
            continue
        usage = psutil.disk_usage(part.mountpoint)
        disks.append(f"{part.device} - Всего: {round(usage.total / (1024**3), 2)} GB | Свободно: {round(usage.free / (1024**3), 2)} GB")
    return "\n".join(disks)

def get_network_info():
    """Получает информацию о сетевых интерфейсах"""
    interfaces = []
    for name, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                interfaces.append(f"{name}: {addr.address}")
    return "\n".join(interfaces) if interfaces else "Нет доступных сетевых интерфейсов"

def ping_test(host="google.com"):
    """Выполняет ping указанного хоста"""
    try:
        output = subprocess.check_output(f"ping {host} -n 2", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def display_menu(selected_index):
    """Отображает меню с подсветкой выбранного пункта"""
    CLEAR_SCREEN()
    print(BACKGROUND_COLOR + TEXT_COLOR + Style.BRIGHT)
    print("=" * 50)
    print(" ИНСТРУМЕНТЫ ДЛЯ ПК ".center(50))
    print("=" * 50)
    print()
    
    menu_items = [
        "1. Получить IP-адрес",
        "2. Получить имя компьютера",
        "3. Получить информацию об ОС",
        "4. Получить информацию о процессоре",
        "5. Получить информацию об оперативной памяти",
        "6. Получить информацию о дисках",
        "7. Получить информацию о сетевых интерфейсах",
        "8. Выполнить ping тест (google.com)",
        "9. Выход"
    ]
    
    for i, item in enumerate(menu_items):
        if i == selected_index:
            print(HIGHLIGHT_COLOR + "> " + item)
        else:
            print(NORMAL_COLOR + "  " + item)
    
    print("\n" + "=" * 50)
    print(" Используйте стрелки ВВЕРХ/ВНИЗ для выбора ".center(50))
    print(" ENTER - выбрать, ESC - выход ".center(50))
    print("=" * 50 + Style.RESET_ALL)

def show_result(title, content):
    """Отображает результат выбранной операции"""
    CLEAR_SCREEN()
    print(BACKGROUND_COLOR + TEXT_COLOR + Style.BRIGHT)
    print("=" * 50)
    print(f" {title} ".center(50))
    print("=" * 50)
    print(NORMAL_COLOR + "\n" + str(content) + "\n")
    print("=" * 50)
    print(" Нажмите любую клавишу для возврата в меню ".center(50))
    print("=" * 50 + Style.RESET_ALL)
    msvcrt.getch()  # Ожидание нажатия любой клавиши

def main():
    set_console_title("Инструменты для ПК")
    selected_index = 0
    menu_items_count = 9
    
    while True:
        display_menu(selected_index)
        
        # Ожидание нажатия клавиши
        key = ord(msvcrt.getch())
        if key == 224:  # Коды стрелок
            key = ord(msvcrt.getch())
        
        # Обработка нажатий клавиш
        if key == 72:  # Стрелка вверх
            selected_index = (selected_index - 1) % menu_items_count
        elif key == 80:  # Стрелка вниз
            selected_index = (selected_index + 1) % menu_items_count
        elif key == 13:  # Enter
            if selected_index == 0:
                show_result("IP-АДРЕС", get_ip_address())
            elif selected_index == 1:
                show_result("ИМЯ КОМПЬЮТЕРА", get_pc_name())
            elif selected_index == 2:
                show_result("ИНФОРМАЦИЯ ОБ ОС", get_os_info())
            elif selected_index == 3:
                show_result("ИНФОРМАЦИЯ О ПРОЦЕССОРЕ", get_cpu_info())
            elif selected_index == 4:
                show_result("ИНФОРМАЦИЯ ОБ ОПЕРАТИВНОЙ ПАМЯТИ", get_ram_info())
            elif selected_index == 5:
                show_result("ИНФОРМАЦИЯ О ДИСКАХ", get_disk_info())
            elif selected_index == 6:
                show_result("СЕТЕВЫЕ ИНТЕРФЕЙСЫ", get_network_info())
            elif selected_index == 7:
                show_result("PING ТЕСТ (google.com)", ping_test())
            elif selected_index == 8:
                CLEAR_SCREEN()
                print(Style.RESET_ALL)
                exit()
        elif key == 27:  # ESC
            CLEAR_SCREEN()
            print(Style.RESET_ALL)
            exit()

if __name__ == "__main__":
    try:
        CLEAR_SCREEN = lambda: os.system('cls')
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        input("Нажмите Enter для выхода...")