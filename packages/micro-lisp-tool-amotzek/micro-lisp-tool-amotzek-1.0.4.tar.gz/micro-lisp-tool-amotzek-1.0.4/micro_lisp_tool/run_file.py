from time import sleep
from .lisp_file import LispFile
from .protocol import Protocol
from serial import Serial


def run_file(sourcename, port):
    with open(sourcename) as f:
        with Serial(port, 115200, timeout=600) as s:
            lf = LispFile(f)
            p = Protocol(s)
            while not p.is_ready():
                sleep(10)
            p.drain_tasks()
            while lf.available():
                expr = lf.next_list()
                if expr is not None:
                    print('>' + expr)
                    print(p.send_receive(expr))
            while True:
                req = input('>')
                if len(req) == 0:
                    break
                res = p.send_receive(req)
                print(res)
