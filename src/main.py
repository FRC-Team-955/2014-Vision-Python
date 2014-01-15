import vision_color_detection as vision
import time

################################################################################
#
# main
#
################################################################################
# if this script is run directly by python, then __name__ is '__main__'.  If it
# is run because it is imported, then __name__ is the module name.
if __name__ == '__main__': 
  while  True:
    vision.update()
    time.sleep(1)