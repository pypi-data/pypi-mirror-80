# wscreenshot

wscreenshot is a package which helps you to take screenshot of active windows running in windows OS.
You just have to specify the name of the window which you want to take screen shot.

If you don't specify name of any window it takes the default screenshot of current view.

Implemented using win32 library and numpy so that it can be directly used by opencv.

To take Default Screenshot

```python
from wscreenshot import Screenshot
import cv2 as cv
k = Screenshot()
x = k.screenshot()
cv.imshow('My Screenshot', x)
cv.waitKey(0) 
cv.destroyAllWindows()  
```

To list out the active windows you can use

```python
import wscreenshot
wscreenshot.list_window_names()
```
This prints all the active windows.

To take screenshot of only specific window use

```
obj = Screenshot('Name of the window')
```
or
```
obj = Screenshot(window_name = 'Name of the window')
```

Example to take the screenshot of File Explorer which is currently running

To get the exact name of the window use `wscreenshot.list_window_names()`

```python
from wscreenshot import Screenshot
import cv2 as cv
k = Screenshot('File Explorer')
x = k.screenshot()
cv.imshow('My Screenshot', x)
cv.waitKey(0) 
cv.destroyAllWindows()  
```

For taking the cropped screenshot you can specify `width` and `height` of the image

```
obj.screenshot(w = None, h = None)
```


Example:
```python
from wscreenshot import Screenshot
import cv2 as cv
k = Screenshot()
x = k.screenshot(w = 200)
cv.imshow('My Screenshot with width 200', x)
cv.waitKey(0) 
cv.destroyAllWindows()  
x = k.screenshot(h = 200)
cv.imshow('My Screenshot with height 200', x)
cv.waitKey(0) 
cv.destroyAllWindows()  
x = k.screenshot(w = 200, h = 200)
cv.imshow('My Screenshot with width and height 200', x)
cv.waitKey(0) 
cv.destroyAllWindows()  
```


## Advance stuff

This can be used to process games and lot many stuff

To capture each frame we can use

```python
from wscreenshot import Screenshot
from time import time
import cv2 as cv
wincap = Screenshot('name of some active window')
loop_time = time()
while True :
    screenshot = wincap.screenshot()
    cv.imshow('Computer Vision', screenshot)
    print(f'FPS { 1 / (time() - loop_time) }')
    loop_time = time()
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done.')
```
This can be used from processing a game or many image processing application where you can capture each frame and process the image.

## Limitations

It will take blank screenshot for applications build using electron and some other framework.
Will try to resolve in next update