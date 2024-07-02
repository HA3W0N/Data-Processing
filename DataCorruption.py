import cv2
import random
import numpy as np
import matplotlib.pyplot as plt

def Gaussian_Blur(img, sigma):
    result = cv2.GaussianBlur(img, (41,41), sigma)
    return result

def Downsampling(img, Factor):
    result = cv2.resize(img,(0 ,0), fx= Factor, fy=Factor)
    return result

def Resampling(img, Factor):
    result = cv2.resize(img, (0,0), fx = Factor, fy = Factor, interpolation= cv2.INTER_LINEAR)
    return result

def Additive_Noise(img, std):
    noise = np.random.normal(0, std, img.shape)
    result = noise + img
    result = np.clip(result,0,255).astype(np.uint8)
    return result

def JPEG_Compression(img, Factor):
    check, encoding_img = cv2.imencode('.jpeg', img, [int(cv2.IMWRITE_JPEG_QUALITY), Factor])
    result = cv2.imdecode(encoding_img, cv2.IMREAD_COLOR)
    return result

def Resizing(img):
    result = cv2.resize(img, (512,512))
    return result
    
'''
if __name__ == "__main__":
    # Gaussian Kernel Sigma 0 or for 1,10,0.1
    Gaussian_Sigma = (random.randint(0,100))/10
    if Gaussian_Sigma < 1 : Gaussian_Sigma = 0
    # Downsampling Factor
    DownSample_Factor = (random.randint(50,100))/100
    # Scale Factor for 0.8, 8, 0.1
    Scale_Factor = (random.randint(8,80))/10
    # Gaussian Noise for 0, 20, 1
    Gaussian_Noise = random.randint(0,20)
    # Quality Factor 0 or for 60, 100, 1
    Quality_Factor = random.randint(56,100)
    if Quality_Factor < 60 : Quality_Factor = 0

    print("Gaussian Sigma : {}, Scale Factor : {} , Gaussian Noise : {}, Quality Factor : {}".format(Gaussian_Sigma, Scale_Factor, Gaussian_Noise, Quality_Factor))


    #Test 
    
    img = cv2.imread("0Fi83BHQsMA/00002/000000.jpg")
    Downs = [0.9, 0.8, 0.7, 0.6, 0.5]; row,col,num = 1,len(Downs),1
    for down in Downs:
        Downsampleimg = Downsampling(img,down)
        Downsampleimg = cv2.cvtColor(Downsampleimg,cv2.COLOR_BGR2RGB)
        plt.subplot(row,col,num), plt.imshow(Downsampleimg), plt.title("With ScaleFactor {} ".format(down)),plt.axis('off')
        num += 1
        plt.savefig()
        plt.imsave("Result.jpg", Downsampleimg)

    # # Blur_image = Gaussian_Blur(img,Gaussian_Sigma)
    # Downsample_image = Downsampling(img, Scale_Factor)
    # Resample_image = Resampling(Downsample_image, Scale_Factor)
    # Noise_image = Additive_Noise(Resample_image, Gaussian_Noise)
    # Compressed_image = JPEG_Compression(Noise_image, Quality_Factor)
    # Final_result = Resizing(Compressed_image)

    # cv2.imwrite("DataCorruption.jpg", Final_result)
'''    