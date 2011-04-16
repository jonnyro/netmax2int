import sys
sys.path.append('../common')

import png2dds

#Run simple conversion
png2dds.png2dds('../test_data/png/boxes.png','../output_drop/boxes.dds')
