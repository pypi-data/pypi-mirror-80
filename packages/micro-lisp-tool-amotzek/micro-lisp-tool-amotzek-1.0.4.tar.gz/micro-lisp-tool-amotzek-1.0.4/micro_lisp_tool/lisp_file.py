Outside = 0
InString = 1
Escape = 2


class LispFile:
    def __init__(self, file):
        self.file = file
        self.content = None

    def read_if_needed(self):
        if self.content is None:
            self.content = ''
            for line in self.file:
                self.content += line
                self.content += ' '

    def available(self):
        self.read_if_needed()
        return len(self.content) > 0

    def next_list(self):
        self.read_if_needed()
        index = 0
        state = Outside
        brackets = 0
        expression = ""
        while index < len(self.content):
            current = self.content[index]
            if state == Outside:
                if current == '"':
                    state = InString
                elif current == '(':
                    brackets += 1
                elif current == ')':
                    brackets -= 1
                    if brackets == 0:
                        self.content = self.content[index + 1:]
                        expression += current
                        return expression
            elif state == InString:
                if current == '\\':
                    state = Escape
                elif current == '"':
                    state = Outside
            elif state == Escape:
                state = InString
            if brackets > 0 and (state != Outside or current != ' ' or expression[-1] != ' '):
                expression += current
            index += 1
        self.content = ""
        return None
