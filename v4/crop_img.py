import numpy as np
import math

class Crop:
    def __init__(self, img_array) -> None:
        self.img_array = img_array
        self.img_size = img_array.shape[0]    

    # Crop images begfore prediction
    def top_crop(self):
        for i in range(0, self.img_size):
            if np.amin(self.img_array[i]) < 255:
                return i - 10
    def bottom_crop(self):
        for i in range(self.img_size-1, 0, -1):
            if np.amin(self.img_array[i]) < 255:
                return i + 10
    def left_crop(self):
        print(self.img_size)
        for i in range(0, self.img_size):
            for b in range(0, self.img_size):
                if np.mean(self.img_array[b][i]) < 255:
                    return i - 10
    def right_crop(self):
        for i in range(self.img_size-1, 0, -1):
            for b in range(0, self.img_size):
                if np.mean(self.img_array[b][i]) < 255:
                    return i + 10

    def w_h(self):
        l = Crop.left_crop(self)
        t = Crop.top_crop(self)
        r = Crop.right_crop(self)
        b = Crop.bottom_crop(self)
        if None not in [l,t,r,b]:
            height = b - t
            width = r - l
            if height < width:
                x = (width - height) / 2
                return l, math.floor(t-x), r, math.floor(b+x)
            else:
                x = (height - width) / 2
                return math.floor(l-x), t, math.floor(r+x), b
        else:
            return 0, 0, 300, 300
