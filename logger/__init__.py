class log:
    def __init__(self, fileName):
        self.fileName = fileName

    def info(self, msj, newLineInStart=False):
        if newLineInStart:
            print()

        print(f'[{self.fileName}] {msj}')
