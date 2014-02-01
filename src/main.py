import vision as vision
import ntClient as NetworkTable
import time

################################################################################
#
# main
#
################################################################################
# if this script is run directly by python, then __name__ is '__main__'.  If it
# is run because it is imported, then __name__ is the module name.

tableName = "/955/"
distanceName = ""

if __name__ == '__main__': 

	table = NetworkTable(tableName)
	while  True:
    	vision.update()
    	time.sleep(1.0 / 4.0)