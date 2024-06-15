import pyautogui
import pyscreenshot as ImageGrab
import keyboard
import time
import subprocess

# Список целевых цветов
target_colors = []
is_running = True

def is_process_running(process_name):
    """Проверка, запущен ли процесс с заданным именем"""
    try:
        output = subprocess.check_output(['tasklist', '/fi', f'imagename eq {process_name}']).decode('cp866')
        return process_name.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False

def get_color(x, y):
    """Получить цвет пикселя по координатам (x, y)"""
    image = ImageGrab.grab(bbox=(x, y, x+1, y+1))
    color = image.getpixel((0, 0))
    return color

def add_color_under_cursor():
    """Добавить цвет под курсором в список целевых цветов"""
    x, y = pyautogui.position()
    color = get_color(x, y)
    target_colors.append(color)
    print(f"Added color: {color}")

def find_color_and_click(region):
    """Поиск заданного цвета в указанной области и клик по нему"""
    image = ImageGrab.grab(bbox=region)
    width, height = image.size

    for x in range(width):
        for y in range(height):
            color = image.getpixel((x, y))
            if color in target_colors:
                print(f"Found target color {color} at ({x}, {y})")
                pyautogui.click(region[0] + x, region[1] + y)
                return True
    return False

def main(region, interval=0.1):
    """Главная функция, выполняющая поиск и клик по цвету"""
    global is_running

    print("Checking if banana.exe is running...")
    if not is_process_running('banana.exe'):
        print("banana.exe is not running. Exiting...")
        return

    print("Entering main loop...")

    while is_running:
        if not is_process_running('banana.exe'):
            print("banana.exe is not running. Exiting...")
            break

        if keyboard.is_pressed('p'):
            print("P key pressed.")
            add_color_under_cursor()
            print("Color added under cursor. Script is running.")
            time.sleep(0.5)  # предотвращение множественных нажатий

        if find_color_and_click(region):
            print(f"Clicked at one of the target colors")

        if keyboard.is_pressed('s'):
            print("S key pressed. Emergency stop activated. Script stopped.")
            is_running = False

        time.sleep(interval)

    print("Script ended.")

if __name__ == "__main__":
    # Задайте область поиска в формате (лево, верх, право, низ)
    region = (0, 0, 1920, 1080)  # Пример: весь экран
    main(region)
