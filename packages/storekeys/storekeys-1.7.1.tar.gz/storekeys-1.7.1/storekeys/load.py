import os.path
from .errors import InvalidKeysInFile,FileNotExists,InvalidFileName
import base64
import os

class LoadKeys:
    def __init__(self,fileName=''):
        if(len(fileName)==0):
            filesIn = os.listdir()
            filesIn = [f for f in filesIn if f.split('.')[-1]=='kys' and os.path.isfile(f)]
            if(len(filesIn)==1):
                fileName = filesIn[0]
            else:
                raise InvalidFileName('No keys files found or more than one found')
        if(len(fileName.split('.'))>1):
            s = fileName.split('.')
            if(s[-1]=='kys'):
                s.pop(-1)
            fileName = '.'.join(s)
        
        self.fileName = str(fileName)

    def get_keys(self):
        keys = {}
        if(os.path.isfile(self.fileName+'.kys')):
            with open(self.fileName+'.kys','r') as keyFile:
                for i in keyFile:
                    line = base64.b64decode(bytes(i.strip(),'utf-8')).decode("utf-8").strip()
                    if(len(line.split('<key>'))==2):
                        pair = line.split('<key>')
                        keys[pair[0]]=pair[1]
                    else:
                        raise InvalidKeysInFile(self.fileName)
            return keys
        else:
            raise FileNotExists(self.fileName)


