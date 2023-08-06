class Error(Exception):
    pass

class InvalidKeysInFile(Error):
    def __init__(self, fileName,message = 'Keys are in invalid format'):
        self.file = fileName
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message} in the file {self.file}'

class FileNotExists(Error):
    def __init__(self, fileName,message = ''):
        self.file = fileName
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f'{self.message}The file {self.file} does not exists'

class InvalidFileName(Error):
    pass

class ValueNotProvided(Error):
    pass

class KeyNotProvided(Error):
    pass