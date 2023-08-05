import numpy as np
import win32gui, win32ui, win32con, win32api

class Screenshot:
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name = None):
        try:
            if window_name is not None:
                self.hwnd = win32gui.FindWindow(None, window_name)
                window_rect = win32gui.GetWindowRect(self.hwnd)
                self.w = window_rect[2] - window_rect[0]
                self.h = window_rect[3] - window_rect[1]
            else:
                self.w = win32api.GetSystemMetrics(0)
                self.h = win32api.GetSystemMetrics(1)
        except Exception as e:
            raise Exception(e)


    def screenshot(self, w = None, h = None):
        try:
            if w:
                tempw = self.w
                self.w = w
            if h:
                temph = self.h
                self.h = h
            wDC = win32gui.GetWindowDC(self.hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (self.h, self.w, 4)
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            if w:
                self.w = tempw
            if h:
                self.h = temph
            return img
        except Exception as e:
            raise Exception(e)

def list_window_names():
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)
