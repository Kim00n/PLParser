import os


class TextFile:
    @staticmethod
    def __is_eof__(file_ref):
        # Retrieve current position reading of the file
        line_pos = file_ref.tell()
        file_size = os.stat(file_ref.fileno()).st_size
        return line_pos >= file_size

    @staticmethod
    def read (source_path):
        # open the file
        file_ref = open(source_path)
        file_content = ""
        # loop until the end
        while not TextFile.__is_eof__(file_ref):
            line = file_ref.readline()
            file_content += line
        # close the file
        file_ref.close
        # return result
        return file_content

from src.archive.fileHandling import TextFile
