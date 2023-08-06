from time import sleep


class Protocol:
    def __init__(self, serial):
        self.serial = serial

    def available(self):
        return self.serial.in_waiting > 0

    def write_line(self, line):
        for c in line:
            self.serial.write(bytes(c, 'ASCII'))
            sleep(0.05)
        self.serial.write(bytes('\r\n', 'ASCII'))

    def read_line(self):
        return str(self.serial.readline(), 'ASCII')

    def send_receive(self, command):
        self.serial.reset_input_buffer()
        self.write_line(command)
        self.serial.flush()
        response = self.read_line()
        while self.available():
            response += '\r\n'
            response += self.read_line()
        return response

    def is_ready(self):
        response = self.send_receive('t')
        return response.startswith('t')

    def drain_tasks(self):
        response = self.send_receive('(drain-tasks)')
        try:
            return int(response)
        except:
            return None
