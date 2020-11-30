from PIL import Image
FILENAME = 'output.gif'

SCREENSHOTS = [ 'screenshots/s{}.png'.format(_) for _ in range(20)]

print('Loading images')
IMAGES = [ Image.open(scrnsht) for scrnsht in SCREENSHOTS ]

print('Saving images')
# Save into a GIF file that loops forever
IMAGES[0].save(FILENAME, format='GIF',
               append_images=IMAGES[1:],
               save_all=True,
               duration=50, loop=0)
print('Done, please check ' + FILENAME)
