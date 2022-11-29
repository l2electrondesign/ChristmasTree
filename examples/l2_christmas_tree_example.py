# Tim Lauber
# L2 Electron Design

from l2_christmas_tree import l2_christmas_tree

christmas_tree = l2_christmas_tree('/dev/ttyUSB0')

christmas_tree.connect()
    
pixel_array = [[i,0,0,0,255] for i in range(12)]
christmas_tree.set_pixel_array(pixel_array)

christmas_tree.save()

christmas_tree.close()