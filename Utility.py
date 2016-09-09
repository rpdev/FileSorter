'''
Created on 29 aug 2012

'''
import magic
import hashlib

def get_file_type(file_path):
    ms = magic.open(magic.MAGIC_NONE)
    ms.load()
    file_type = ms.file(file_path)
    ms.close()
    if file_type.count(',') > 2:
        return file_type[:file_type.index(',', file_type.index(',')+1)]
    else:
        return file_type

def get_limited_file_type(file_path, limited_keys = ['JPEG','GIF','PNG','PDF','HTML']):
    file_type = get_file_type(file_path)
    for value in limited_keys:
        if str(file_type).startswith(value):
            return file_type, value
    return file_type, None  

def hash_calc(f, algorithm = hashlib.md5(), read_size = 2**20):
    fo = open(f)
    while True:
        s = fo.read(read_size)
        if not s:
            break
        algorithm.update(s)
    return algorithm.hexdigest()

def print_available_hash_algorithms():
    '''
    Print those hash algorithms that is supported
    for this system
    '''
    for algorithm in hashlib.algorithms:
        print algorithm