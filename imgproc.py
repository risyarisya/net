import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def loadRawDataFromFile(filename, width, height, chNum):	
	img = np.fromfile(filename, dtype=np.uint8)
	if chNum==0:
		print("error!")
		return false;
	img.shape = (height, width, chNum)
	return Image.fromarray(img) 

def makePatch(data, patchX, patchY, stride, outpath, prefix):
	currX = 0
	currY = 0
	width, height = data.size
	cnt = 0
	if not os.path.isdir(outpath):
		os.mkdir(outpath)
	while currY+patchY<=height:
		while currX+patchX<=width:
			tmp = resized.crop((currX, currY, currX+patchX, currY+patchY)) 
			tmp.save("%s/%s%d.jpg"%(outpath, prefix, cnt), 'JPEG')
			cnt += 1
			currX += stride
		currX = 0
		currY += stride

#imgdata = loadRawDataFromFile('DSC00568.data', 4240, 2832, 3)

#cropped = imgdata.crop((0, 0, 2120, 2832))
#resized = cropped.resize((2832, 1060)) 

#patchX = 32
#patchY = 32
#stride = 16


#makePatch(resized, patchX, patchY, stride, './image1patch', 'patch') 
#result.save('hoge', 'JPEG')


#cmyk = resizeimg.convert('CMYK')
#c,m,y,k = cmyk.split()
#print(np.asarray(c).shape)

#plt.imshow(result)
#plt.savefig("yourNewImage.png")
