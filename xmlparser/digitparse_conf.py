import os
import time
"""
This is nokiaxmlparser.py configuration file
"""
# MO_LIST_FILTER filters items from the source file. If list is empty it filters nothing means
# will parse everyting
# MO_LIST_FILTER = ['BSC']#["BSC", "BCF", "BTS", "TRX", "LAPD", "RNC", "WBTS", "WCEL", "IPNB",
#                  "MRBTS", "LNBTS", "LNCEL", "IPADDRESSV4", "IPIF", "VLANIF", "IPRT",
#                  "RTPOL", "SMOD_R", "RMOD_R", "SMOD",
#                  "ADCE", "ADJW", "ADJG", "ADJI", "ADJS", "ADJL", "LNADJL", "LNADJW",
#                  "EXGCE", "EXUCE", "EXENBF"]

# Database Name
DB_NAME = 'nokia.db'

# CHUNK_SIZE defines how many managed object will be per splited xml file. Depending on RAM size this
# count can be increased. With limited system memory, memory exception can occur. Default is 10000
MO_CHUNK_SIZE = 20000


# Source file archive usually (.xml.gz) to parse. Default is nokia.xml.gz
SOURCE_FILE = 'nokiadump_'+time.strftime("%y%m%d")+'.xml.gz'

# Object to be captured during file split operation. Default is managedObject
MO_NAME = 'managedObject'

# Absolute path. Starting from the current directory of the script nokiaxmlparser.py
ABS_PATH = 'ToBeParsed'

# Full path of script directory. Only uncomment this line if you need to schedule a job in linux m/c.
# CRONPATH_LINUX = '/root/scripts/bl'


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IS_ZIP_DB = True

IS_WEEKLY_BAKUP = True
