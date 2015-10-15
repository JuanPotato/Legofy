from subprocess import call
import shutil
from PIL import Image
import sys
import os

brickh = 30
brickw = 30
brick = "brick30.png"

cmdargs = sys.argv[1]

if len(cmdargs) < 2:
	print("No input file specified, please use the command \"python legoGif.py gifname.gif\" to create a legofied version of \"gifname.gif\". It will automatically be saved as \"lego_gifname.gif\"")
	sys.exit(0)

filename = cmdargs

# function that iterates over the gif's frames
def iter_frames(imageToIter):
	try:
		i = 0
		while 1:
			imageToIter.seek( i )
			imframe = imageToIter.copy()
			if i == 0: 
				palette = imframe.getpalette()
			else:
				imframe.putpalette( palette )
			yield imframe
			i += 1
	except EOFError:
		pass

# small function to apply an effect over an entire image
def applyEffect( image, effect ):
	width, height = image.size
	poa = image.load()
	for x in range( width ):
		for y in range( height ):
			poa[x, y] = effect( poa[x, y] )
	return image

# create a lego brick from a single color
def makeLegoBrick( overlayRed, overlayGreen, overlayBlue ):
	# colorizing the brick function
	def colorize( blockColors ):
		newRed = 133 - overlayRed
		if newRed > 100: newRed = 100
		if newRed < -100: newRed = -100
		
		newGreen = 133 - overlayGreen
		if newGreen > 100: newGreen = 100
		if newGreen < -100: newGreen = -100
		
		newBlue = 133 - overlayBlue
		if newBlue > 100: newBlue = 100
		if newBlue < -100: newBlue = -100
		
		return ( blockColors[0] - newRed, blockColors[1] - newGreen, blockColors[2] - newBlue, 255 )
	
	return applyEffect( Image.open( brick ), colorize )

# create a lego version of an image from an image
def makeLegoImage( baseImage ):
	baseWidth, baseHeight = baseImage.size
	basePoa = baseImage.load()

	legoImage = Image.new("RGB", (baseWidth * brickw, baseHeight * brickh), "white")

	for x in range( baseWidth ):
		for y in range( baseHeight ):
			bp = basePoa[x, y]
			isinstance( bp, ( int, long ) )
			legoImage.paste( makeLegoBrick( bp[0], bp[1], bp[2] ), ( x * brickw, y * brickh, ( x + 1 ) * brickw, ( y + 1 ) * brickh ) )
	return legoImage

# open gif to start splitting
gifImage = Image.open( filename )

newSize = gifImage.size

# scale image
scale = 1

if newSize[0] > 30 or newSize[1] > 30:
	if newSize[0] < newSize[1]:
		scale = newSize[1] / 30
	else:
		scale = newSize[0] / 30
	
	newSize = ( int( round( newSize[0] / scale ) ), int( round( newSize[1] / scale ) ) )

# check if dir exists, if not, make it
if not os.path.exists( "./tmp_frames/" ):
	os.makedirs( "./tmp_frames/" )

# for each frame in the gif, save it
for i, frame in enumerate( iter_frames( gifImage ) ):
	frame.save( './tmp_frames/frame_{}.png'.format( ( "0" * ( 4 - len( str( i ) ) ) ) + str( i ) ), **frame.info )

# make lego images from gif
for file in os.listdir("./tmp_frames"):
	if file.endswith(".png"):
		print("Working on {}".format(file))
		im = Image.open("./tmp_frames/{}".format(file)).convert("RGBA")
		if scale != 1:
			im.thumbnail(newSize, Image.ANTIALIAS)
		makeLegoImage(im).save("./tmp_frames/{}".format(file))

# make new gif "convert -delay 10 -loop 0 *.png animation.gif"
delay = gifImage.info["duration"] / len(os.listdir("./tmp_frames"))
print(["convert", "-delay", str( delay / 10 ), "-loop", "0", "./tmp_frames/*.png", "lego_" + filename])
call(["convert", "-delay", str(delay/10), "-loop", "0", "./tmp_frames/*.png", "lego_" + filename])

shutil.rmtree('./tmp_frames')

print("finished")
