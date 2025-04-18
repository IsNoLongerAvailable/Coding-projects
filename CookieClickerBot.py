# Hey I don't really know how this site works but I am too lazy to figure it out at 3:45 am, So I will just add my notes here.
# If you can give me like constructive criticism to help me learn or show what features or stuff I could've done to improve the code than go ahead.
# This is my first coding project and I did get some help with the threading from chatgpt but I will try not to use it in my future projects.
# You can also laugh or point out how bad my code is but also point out what I could've changed or done better to make it better please.
# That's all to the Two people who see this.
# Also the pos values and stuff are different for me since I had my browser half the size because I wanted to write and test the code in a more efficient manner
# THE GOLDEN COOKIE DETECTOR ONLY WORKS IF YOUR PC DATE IS SET TO MARCH 31ST! BECAUSE THE DEFAULT GOLDEN COOKIE RGB VALUES ARE TOO SIMILAR TO THE BIG COOKIE!


import pyautogui
import keyboard
import time
from PIL import ImageGrab
import threading

# info
cookie_pos = (125, 493)
building_pos = x1, y1, x2, y2 = 640, 318, 867, 1019
gold_pos = x3, y3, x4, y4 = 45, 140, 809, 1000
upg_rgb = (56, 52, 43)
upg_pos = (650, 249)
pyautogui.PAUSE = 0
click_count = 0


latest_building = None
latest_cookie = None

# Data collector
def upgrades_thread():
    global latest_building
    while True:
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image = screenshot.load()
        lowest_y = -1
        best_x = -1
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                if image[x, y] == (255, 255, 255) and y > lowest_y:
                    lowest_y = y
                    best_x = x
        if best_x != -1 and lowest_y != -1:
            full_X = x1 + best_x
            full_Y = y1 + lowest_y
            latest_building = (full_X, full_Y)
        else:
            latest_building = None
        time.sleep(1)

def gold_cookie_thread():
    global latest_cookie
    target_color = (255, 255, 177)
    tolerance = 17
    while True:
        screenshot = ImageGrab.grab(bbox=(x3, y3, x4, y4))
        image = screenshot.load()
        found = None
        for x in range(screenshot.width):
            for y in range(screenshot.height):
                pixel = image[x, y]
                if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
                    found = (x + x3, y + y3)
                    break
            if found:
                break
        latest_cookie = found
        time.sleep(0.3)


threading.Thread(target=upgrades_thread, daemon=True).start()
threading.Thread(target=gold_cookie_thread, daemon=True).start()

# CLICKER!!!!!!
while True:
    if keyboard.is_pressed("tab"):
        print("Stop!")
        break

    for _ in range(5):
        pyautogui.click(cookie_pos)
        click_count += 1

    if pyautogui.pixelMatchesColor(upg_pos[0], upg_pos[1], upg_rgb, tolerance=20):
        pyautogui.click(upg_pos)

    if click_count %2500 == 0 and latest_building:
        pyautogui.click(latest_building)
        for _ in range(10):
            pyautogui.click()

    if latest_cookie:
        pyautogui.click(latest_cookie)
        print("GOLD COOKIE CLICKED")
        latest_cookie = None

    time.sleep(0)
