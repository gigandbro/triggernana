import pyautogui
import pyscreenshot as ImageGrab
import keyboard
import time
import random

# Устанавливаем скорость перемещения курсора
pyautogui.FAILSAFE = True  # Активируем защиту от случайного движения в углы экрана
pyautogui.PAUSE = 0.1  # Задержка между действиями pyautogui
pyautogui.MINIMUM_DURATION = 0  # Минимальное время перемещения
pyautogui.MINIMUM_SLEEP = 0  # Минимальное время ожидания

# Список целевых цветов
target_colors = []
is_running = True

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
                # Используем меньший разброс в координатах
                offset_x = random.randint(-50, 50)
                offset_y = random.randint(-50, 50)
                # Вычисляем новые координаты для перемещения курсора
                new_x = region[0] + x + offset_x
                new_y = region[1] + y + offset_y
                # Перемещаем курсор и выполняем клик
                pyautogui.moveTo(new_x, new_y, duration=0.001)
                pyautogui.click()
                return True
    return False

def main(region):
    """Главная функция, выполняющая поиск и клик по цвету"""
    global is_running

    print("Entering main loop...")

    while is_running:
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

if __name__ == "__main__":
    # Задайте область поиска в формате (лево, верх, право, низ)
    region = (0, 0, 1920, 1080)  # Пример: весь экран
    main(region)
