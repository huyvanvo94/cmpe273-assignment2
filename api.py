import app
import sys

if __name__ == '__main__':
    try:
        port = sys.argv[1]
        print('client made at {}'.format(port))

        app.app.run(host='localhost', port=int(port))

    except:
        print('error')