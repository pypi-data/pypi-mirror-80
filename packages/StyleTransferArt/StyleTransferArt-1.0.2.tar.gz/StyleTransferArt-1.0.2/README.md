# Style Transfer Art Package to compose one image in the style of another image (ever wish you could paint like Picasso or Van Gogh?
```
Neural style transfer is an optimization technique used to take two images 
a content image and a style reference image (such as an artwork by a famous painter)
and blend them together so the output image looks like the content image,
 but “painted” in the style of the style reference image.
```
## about

Python Package to compose one image in the style of another image 

# Installation

```
pip install StyleTransferArt
or in colab google cloud
!pip install StyleTransferArt
```

## use this example  for get composed  image  
```
from StyleTransferArt import style_transfer

```
```
original_image='/content/o1.jpg'
style_image='/content/s1.jpg'
num_iterations=3000
out_image='new2.jpg'
style_transfer.style_transfer(original_image,style_image,num_iterations,out_image)
```

## Tutorial 
u can see tutorial in colab

https://colab.research.google.com/drive/13YpB8LaSIhEES7D9zzOVj9JtJtJ5Oam2?usp=sharing
