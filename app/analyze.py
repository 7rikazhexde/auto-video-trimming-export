import cv2
import numpy as np
import scipy.stats as sstats

def analyze_frame(im_cv):
    # Grayscaling
    img = cv2.cvtColor(im_cv, cv2.COLOR_RGB2GRAY)
    # one-dimensional array
    img = np.array(img).flatten()
    # Calculate the average of the luminance values
    mean = img.mean()
    #std = np.std(img)
    #median = np.median(img)
    #mode = sstats.mode(img,keepdims=True)[0][0]
    return mean#,std,median,mode

if __name__ == '__main__':
    path = './media/images/lena.png'
    im_cv = cv2.imread(path)
    mean = analyze_frame(im_cv)
    print('image_path:', path)
    print('mean:', mean)