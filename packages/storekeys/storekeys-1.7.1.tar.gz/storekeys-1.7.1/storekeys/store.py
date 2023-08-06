import argparse
import os.path
from print_table import Table   
from .errors import InvalidFileName,FileNotExists,ValueNotProvided,KeyNotProvided
from .load import LoadKeys
import base64
#resolved a small error4
class Store:
    def store_key(self,fileName,key,value):
        if(len(fileName)==0):
            raise InvalidFileName()
        if(len(fileName.split('.'))>1):
            s = fileName.split('.')
            if(s[-1]=='kys'):
                s.pop(-1)
            fileName = '.'.join(s)
        fileName+='.kys'
        keys = {}
        if(os.path.isfile(fileName)):
            keys = LoadKeys(fileName).get_keys()
        keys[key] = value
        with open(fileName,'w') as keyFile:
            for k,v in keys.items():
                keyFile.write(base64.b64encode(bytes(str(k)+'<key>'+str(v),'utf-8')).decode('utf-8')+'\n')

    def delete_key(self,fileName,key):
        if(len(fileName)==0):
            raise InvalidFileName()
        if(len(fileName.split('.'))>1):
            s = fileName.split('.')
            if(s[-1]=='kys'):
                s.pop(-1)
            fileName = '.'.join(s)
        fileName+='.kys'
        keys = {}
        if(os.path.isfile(fileName)):
            keys = LoadKeys(fileName).get_keys()
            try:
                keys.pop(key)
            except KeyError:
                pass
            with open(fileName,'w') as keyFile:
                for k,v in keys.items():
                    keyFile.write(base64.b64encode(bytes(str(k)+'<key>'+str(v),'utf-8')).decode('utf-8')+'\n')
        else:
            raise FileNotExists(fileName)
    
    def print_keys(self,fileName):
        if(len(fileName)==0):
            raise InvalidFileName()
        if(len(fileName.split('.'))>1):
            s = fileName.split('.')
            if(s[-1]=='kys'):
                s.pop(-1)
            fileName = '.'.join(s)
        fileName+='.kys'
        keys = {}
        if(os.path.isfile(fileName)):
            keys = LoadKeys(fileName).get_keys()
            table = Table(2).head(['KEY','VALUE'])
            for k,v in keys.items():
                table.row([k,v])
            table.printTable()



def main():
    parser = argparse.ArgumentParser(description='Store important keys and values together in a keys file.')
    parser.add_argument('fileName',nargs=1,help=' File Name of the kys file')
    parser.add_argument('--delete','-d',action='store_true',help='Set this flag to delete a key')
    parser.add_argument('--noprint','-np',action='store_false',help='Set this flag to not print the keys after the operation')
    parser.add_argument('--showkeys','-s',action='store_true',help='Set this flag to only print the keys')
    args = vars(parser.parse_args())
    if(args['delete']):
        key = input('Key to be deleted:')
        if(key==''):
            raise KeyNotProvided('No key provided to delete')
        Store().delete_key(args['fileName'][0],key)
    elif(args['showkeys']):
        pass
    else:
        key = input('Key to be stored or updated:')
        value = input('Value to be stored or updated:')
        if(key==''):
            raise KeyNotProvided('No key provided to store')
        if(value==''):
            raise ValueNotProvided('No value Provided to store')
        Store().store_key(args['fileName'][0],key,value)
    if(args['noprint']):
        Store().print_keys(args['fileName'][0])
