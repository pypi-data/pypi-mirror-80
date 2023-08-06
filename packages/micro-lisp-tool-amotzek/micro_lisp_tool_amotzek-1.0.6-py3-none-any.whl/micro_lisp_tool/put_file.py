from time import sleep
from .lisp_file import LispFile
from .protocol import Protocol
from serial import Serial


def escape(expr):
    return expr.translate(str.maketrans({'"': '\\"'}))


def put_file(sourcename, port, destname='setup.lisp'):
    with open(sourcename) as f:
        with Serial(port, 115200, timeout=600) as s:
            lf = LispFile(f)
            p = Protocol(s)
            while not p.is_ready():
                sleep(10)
            s = p.send_receive('(gensym)')
            print(f'temporary variable is {s}')
            print(f'delete file {destname}')
            print(p.send_receive(f'(delete-file "{escape(destname)}")'))
            print(f'open file {destname}')
            p.send_receive(f'(setq {s} (open "{escape(destname)}"))')
            while lf.available():
                expr = lf.next_list()
                if expr is not None:
                    print(f'append {expr} to file {destname}')
                    print(p.send_receive(f'(write-char {s} "{escape(expr)}")'))
            print(f'close file {destname}')
            print(p.send_receive(f'(close {s})'))
            print(f'unbind temporary variable {s}')
            print(p.send_receive(f'(unbind (quote {s}))'))
            if destname == "setup.lisp":
                print('please reset your board')
