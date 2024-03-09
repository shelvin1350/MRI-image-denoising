

### What is gaussian Kernel #####
import numpy 
import cv2
from matplotlib import pyplot as plt

def gaussian_kernel(size, size_y=None):
    size = int(size)
    if not size_y:
        size_y = size
    else:
        size_y = int(size_y)
    x, y = numpy.mgrid[-size:size+1, -size_y:size_y+1]
    g = numpy.exp(-(x**2/float(size)+y**2/float(size_y)))
    return g / g.sum()
 

gaussian_kernel_array = gaussian_kernel(3)
print(gaussian_kernel_array)
plt.imshow(gaussian_kernel_array, cmap=plt.get_cmap('jet'), interpolation='nearest')
plt.colorbar()
plt.show()

############################ Denoising filters ###############
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage import img_as_ubyte, img_as_float
from matplotlib import pyplot as plt
from skimage import io
import numpy as np

img = img_as_float(io.imread("images.jpg"))
#Need to convert to float as we will be doing math on the array

from scipy import ndimage as nd
gaussian_img = nd.gaussian_filter(img, sigma=3)
plt.imsave("images/gaussian.jpg", gaussian_img)


median_img = nd.median_filter(img, size=3)
plt.imsave("images/median.jpg", median_img)

gaussian_img = nd.gaussian_filter(img, sigma=3)
plt.imsave("images/gaussian.jpg", gaussian_img)


##### NLM#####

sigma_est = np.mean(estimate_sigma(img, multichannel=True))

patch_kw = dict(patch_size=5,      
                patch_distance=3,  
                multichannel=True)

denoise_img = denoise_nl_means(img, h=1.15 * sigma_est, fast_mode=False,
                               patch_size=5, patch_distance=3, multichannel=True)
"""
denoise_img = denoise_nl_means(img, h=1.15 * sigma_est, fast_mode=False,
                           **patch_kw)
"""
denoise_img_as_8byte = img_as_ubyte(denoise_img)

plt.imshow(denoise_img)
#plt.imshow(denoise_img_as_8byte, cmap=plt.cm.gray, interpolation='nearest')
plt.imsave("images/NLM.jpg",denoise_img)


image = cv2.imread('images/NLM.jpg')
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(image, -1, sharpen_kernel)

cv2.imshow('sharpen', sharpen)
cv2.waitKey()


import cv2
import numpy as np
import matplotlib.pyplot as plt
import maxflow 

# Important parameter
# Higher values means making the image smoother
smoothing = 110

# Load the image and convert it to grayscale image 
# image_path = 'sharpen'
img = cv2.imread(sharpen)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = 255 * (img > 128).astype(np.uint8)

# Create the graph.
g = maxflow.Graph[int]()
# Add the nodes. nodeids has the identifiers of the nodes in the grid.
nodeids = g.add_grid_nodes(img.shape)
# Add non-terminal edges with the same capacity.
g.add_grid_edges(nodeids, smoothing)
# Add the terminal edges. The image pixels are the capacities
# of the edges from the source node. The inverted image pixels
# are the capacities of the edges to the sink node.
g.add_grid_tedges(nodeids, img, 255-img)

# Find the maximum flow.
g.maxflow()
# Get the segments of the nodes in the grid.
sgm = g.get_grid_segments(nodeids)

# The labels should be 1 where sgm is False and 0 otherwise.
img_denoised = np.logical_not(sgm).astype(np.uint8) * 255

# Show the result.
plt.subplot(121)
plt.imshow(img, cmap='gray')
plt.title('Binary image')
plt.subplot(122)
plt.title('Denoised binary image')
plt.imshow(img_denoised, cmap='gray')
plt.show()

# Save denoised image
cv2.imwrite('img_denoised.png', img_denoised)