import os

class OSMango:
    @staticmethod
    def convert_to_absolute_path(relative_path):
        absolute_path = os.path.abspath(relative_path)
        valid_path = os.path.normpath(absolute_path)
        return valid_path

if __name__=='__main__':
    relative_path = "my_folder/file.txt"
    absolute_path = OSMango.convert_to_absolute_path(relative_path)
    print(absolute_path)