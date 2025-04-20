#!/usr/bin/env python3
import os
import platform
import socket
import psutil
import subprocess
import time
from colorama import init, Fore, Back, Style
import sys
import tty
import termios

# Инициализация colorama
init()

# Настройка цветов
BACKGROUND_COLOR = Back.BLUE
TEXT_COLOR = Fore.WHITE
HIGHLIGHT_COLOR = Fore.YELLOW + Back.BLUE + Style.BRIGHT
NORMAL_COLOR = TEXT_COLOR + BACKGROUND_COLOR
CLEAR_SCREEN = lambda: os.system('clear')

def getch():
    """Функция для чтения нажатий клавиш в Linux"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Это escape-символ?
            ch += sys.stdin.read(2)  # Читаем ещё 2 символа
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def get_ip_address():
    """Получает IP-адрес компьютера"""
    try:
        # Получаем IP-адрес для соединения с внешним миром
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "Не удалось получить IP-адрес"

def get_pc_name():
    """Получает имя компьютера"""
    return socket.gethostname()

def get_os_info():
    """Получает информацию об операционной системе"""
    try:
        with open('/etc/os-release') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=')[1].strip().strip('"')
    except:
        pass
    return f"{platform.system()} {platform.release()} (Версия: {platform.version()})"

def get_cpu_info():
    """Получает информацию о процессоре"""
    try:
        with open('/proc/cpuinfo') as f:
            for line in f:
                if line.strip() and 'model name' in line.lower():
                    return line.split(':')[1].strip()
    except:
        pass
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
        disks.append(f"{part.device} -> {part.mountpoint} - Всего: {round(usage.total / (1024**3), 2)} GB | Свободно: {round(usage.free / (1024**3), 2)} GB")
    return "\n".join(disks) if disks else "Нет доступных дисков"

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
        output = subprocess.check_output(f"ping -c 4 {host}", shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def display_menu(selected_index):
    """Отображает меню с подсветкой выбранного пункта"""
    CLEAR_SCREEN()
    print(BACKGROUND_COLOR + TEXT_COLOR + Style.BRIGHT)
    print("=" * 50)
    print(" ИНСТРУМЕНТЫ ДЛЯ ПК (Linux) ".center(50))
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
        "9. Получить информацию о температуре CPU",
        "10. Выход"
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
    getch()  # Ожидание нажатия любой клавиши

def get_cpu_temperature():
    """Получает температуру CPU"""
    try:
        # Попробуем прочитать температуру из /sys/class/thermal
        thermal_zones = [f for f in os.listdir('/sys/class/thermal') if f.startswith('thermal_zone')]
        temps = []
        for zone in thermal_zones:
            try:
                with open(f'/sys/class/thermal/{zone}/type') as f:
                    type_ = f.read().strip()
                if 'cpu' in type_.lower():
                    with open(f'/sys/class/thermal/{zone}/temp') as f:
                        temp = int(f.read().strip()) / 1000.0
                        temps.append(f"{type_}: {temp}°C")
            except:
                continue
        
        if temps:
            return "\n".join(temps)
        
        # Альтернативный метод для Raspberry Pi
        if os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp') as f:
                temp = int(f.read().strip()) / 1000.0
                return f"CPU Temperature: {temp}°C"
        
        return "Не удалось получить температуру CPU (не поддерживается на этой системе)"
    except Exception as e:
        return f"Ошибка при получении температуры CPU: {str(e)}"

def main():
    selected_index = 0
    menu_items_count = 10
    
    while True:
        display_menu(selected_index)
        
        # Ожидание нажатия клавиши
        key = getch()
        
        # Обработка нажатий клавиш
        if key == '\x1b[A':  # Стрелка вверх
            selected_index = (selected_index - 1) % menu_items_count
        elif key == '\x1b[B':  # Стрелка вниз
            selected_index = (selected_index + 1) % menu_items_count
        elif key == '\r' or key == '\n':  # Enter
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
                show_result("ТЕМПЕРАТУРА CPU", get_cpu_temperature())
            elif selected_index == 9:
                CLEAR_SCREEN()
                print(Style.RESET_ALL)
                exit()
        elif key == '\x1b':  # ESC
            CLEAR_SCREEN()
            print(Style.RESET_ALL)
            exit()

if __name__ == "__main__":
    try:
        CLEAR_SCREEN = lambda: os.system('clear')
        main()
    except KeyboardInterrupt:
        CLEAR_SCREEN()
        print(Style.RESET_ALL)
        exit()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        input("Нажмите Enter для выхода...")