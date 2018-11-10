import app
import sys
from servers import *

if __name__ == '__main__':
    try:
        port = sys.argv[1]
        print('client made at {}'.format(port))

        app.app.run(host='localhost', port=int(port))

    except:
        print('error')