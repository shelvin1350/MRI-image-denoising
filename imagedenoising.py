def denoise(image):
    import numpy as np
    import cv2
    from PIL import Image 
    import PIL 
  
    from matplotlib import pyplot as plt
    print("../static"+image)
    img = cv2.imread("E:\jeena project\MRI Image Denoising\clinicapp\static"+image)
    print(img)
    b,g,r = cv2.split(img)           # get b,g,r
    rgb_img = cv2.merge([r,g,b])     # switch it to rgb

    # Denoising
    dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
    
    b,g,r = cv2.split(dst)           # get b,g,r
    rgb_dst = cv2.merge([r,g,b])
    
    
       # switch it to rgb

    plt.subplot(211),plt.imshow(rgb_img)
    plt.subplot(212),plt.imshow(rgb_dst)
    plt.show()

    plt.imshow(rgb_dst)
    plt.show()
