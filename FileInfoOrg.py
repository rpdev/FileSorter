'''

'''
from Utility import get_file_type, hash_calc
import imghdr
import pyexiv2
import hashlib

class FileTypeSet(object):
    '''
    classdocs
    '''

    def __init__(self, file_type, detail_file_type=None):
        '''
        Constructor
        '''
        self.file_type = file_type
        self.detail_file_type = detail_file_type
        self.hash_file_dict = dict()
        
    def add_file(self, file_path):
        f_type = get_file_type(file_path)
        if self.file_type != f_type and not self.file_type in f_type:
            raise TypeError("Types don't match '" + self.file_type + " <> " + f_type + "'")
        file_data = FileData(file_path)
        if not file_data.hash_sum in self.hash_file_dict:
            self.hash_file_dict[file_data.hash_sum] = []
        self.hash_file_dict[file_data.hash_sum].append(file_data)
        
class FileData(object):
    '''
    classdocs
    '''
    
    __exif_time_tags__ = ['Exif.Image.DateTime','Exif.Photo.DateTimeOriginal','Exif.Photo.DateTimeDigitized']
    def __init__(self, file_path):
        '''
        Constructor
        '''
        self.file_path = file_path # save file path
        self.hash_sum = hash_calc(file_path, hashlib.sha1()) # calc hash sum
        self.is_image = imghdr.what(self.file_path) is not None # see if file is an image
        if self.is_image: # if so test if photo
            try:
                metadata = pyexiv2.ImageMetadata(self.file_path) # get metadata
                metadata.read() # get metadata
                self.is_photo = len(metadata.exif_keys) > 0 # if any exif tags mark as photo
                if self.is_photo: # is photo
                    self.metadata = metadata # store exif data
                    self.is_maybe_not_photo = not FileData.__overlaps__(self.__exif_time_tags__, self.metadata.exif_keys)
            except IOError as e: # http://docs.python.org/tutorial/errors.html
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
                self.is_photo = False
        else:
            self.is_photo = False
            self.is_maybe_not_photo = False
    
    def printExifKeys(self):
        if not self.is_photo or self.is_maybe_not_photo:
            print("File: '" + self.file_path + "' has no Exif data")
        else:
            print("Exif data for file: '" + self.file_path + "'")
            for tag in self.metadata.exif_keys:
                print("\t"+tag + " s " + str(self.metadata[tag]))
        
    @staticmethod
    def __overlaps__(a, b):
        return bool(set(a) & set(b))        