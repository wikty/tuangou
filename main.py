import sys

from tornado.options import define

from cfg import SYS_ENCODING
from server import run

# initialize environment
if sys.getdefaultencoding() != SYS_ENCODING:
    reload(sys)  # after reload sys, sys has attribute setdefaultencoding
    sys.setdefaultencoding(SYS_ENCODING)
    
# define tornado server listen port
define("port", default=5000, type=int)

if __name__ == '__main__':
	run()
