import sys
from .run_file import run_file
from .put_file import put_file


def main():
    command = sys.argv[1]
    filename = sys.argv[2]
    index_port = sys.argv.index('--port')
    port = sys.argv[index_port + 1]
    if command == 'run':
        run_file(filename, port)
    elif command == 'put':
        put_file(filename, port)


if __name__ == '__main__':
    main()
