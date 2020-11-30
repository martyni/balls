from PIL import Image
import os
FILENAME = 'output.gif'
MOVIE_LENGTH = len([i for i in os.walk('screenshots')][0][2])
SCREENSHOTS = [ 'screenshots/s{}.png'.format(_) for _ in range(MOVIE_LENGTH)]

print('Loading images')
IMAGES = [ Image.open(scrnsht) for scrnsht in SCREENSHOTS ]

print('Saving images')
# Save into a GIF file that loops forever
IMAGES[0].save(FILENAME, format='GIF',
               append_images=IMAGES[1:],
               save_all=True,
               duration=100, loop=0)
print('Done, please check ' + FILENAME)
