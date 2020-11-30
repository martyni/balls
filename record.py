
import pyautogui
FRAME = 0
while True:
   pyautogui.screenshot().save('screenshots/s{}.png'.format(FRAME))
   FRAME +=1

