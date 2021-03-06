'''
	Simulate a cloudless satellite view by removing temporarily bright pixels from a time series, then averaging the rest.
	Method: Charlie Loyd, 2012. 
	Code skeleton: Charlie Loyd, 2010.
	Tacking of method onto code skeleton: Chris Black, 2012.
'''

from sys import argv, exit, path
path.append('/Library/Python') # If your PIL is broken in the same way as mine
from PIL import Image
from numpy import *

def gridwalk((width,height)):
	for y in range(height):
		for x in range(width):
			yield(x,y)

if len(argv) < 3:
    exit('Usage: <input image>* <output image>. Output is a PNG.')

stacktype = uint8
channel_max_val = 255
n = len(argv)-2 # -1 for our filename, -1 for the output file

imgnum = 0
for imgfile in argv[1:-1]:
	try: img = Image.open(imgfile)
	except: exit('Could not read "%s"!' % (imgfile))
	
	if imgnum == 0:
		stack = asarray(img).copy()
		stack.resize((n,) + stack.shape)
		stack = stack.astype(stacktype)
	
	else:
		if img.size != (stack.shape[2], stack.shape[1]): # img.size: (y,x). stack.shape: (z,x,y,rgb)
			exit('"%s" is not the same shape as the earlier images!' % (imgfile))
		
	stack[imgnum] = asarray(img)
	imgnum = imgnum + 1

for i,j in gridwalk(stack[0].shape[:-1]):
	px = stack[:,i,j]
	saturation = px.max(axis=1) - px.min(axis=1)
	darkness = 3*channel_max_val - px.sum(axis=1)
	quality = saturation + darkness/3.0
	stack[:,i,j] = px[quality.argsort()]

bestz = stack[n/3:].mean(axis=0, dtype=float64)

outimg = Image.fromarray(bestz.astype(uint8))
outimg.save(argv[-1])

# (use if you want to dump the whole sorted stack)	
#for i in range(stack.shape[0]):
#	outimg = Image.fromarray(stack[i].astype(uint8))
#	outimg.save(str(i)+argv[-1])
	
	