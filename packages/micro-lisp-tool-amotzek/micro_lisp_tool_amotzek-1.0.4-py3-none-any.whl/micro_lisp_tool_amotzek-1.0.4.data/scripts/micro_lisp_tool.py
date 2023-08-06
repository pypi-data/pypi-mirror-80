import sys
from micro_lisp_tool import run_file, put_file


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
