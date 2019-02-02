import numpy as np
import cv2
while True:
    img = cv2.imread('spotyPeople/andy.jpeg', 0)
    cv2.imshow('image', img)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    elif cv2.waitKey(0) & 0xFF == ord('s'): # wait for 's' key to save and exit
        cv2.imwrite('messigray.png', img)
        cv2.destroyAllWindows()