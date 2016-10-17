__author__ = 'teemu kanstren'

class FileData:

    def __init__(self, dst_ip, src_path, dst_path, dst_port):
        self.dst_ip = dst_ip
        self.src_path = src_path
        self.dst_path = dst_path
        self.dst_port = int(dst_port)


    def __str__(self):
        return "dst_ip="+self.dst_ip+", src_path="+self.src_path+", dst_path="+self.dst_path


    def __repr__(self):
        return "dst_ip=" + self.dst_ip + ", src_path=" + self.src_path + ", dst_path=" + self.dst_path


    #http://stackoverflow.com/questions/4005318/how-to-implement-a-good-hash-function-in-python
    def __eq__(self, other):
        return other and self.dst_ip == other.dst_ip and self.src_path == other.src_path and self.dst_path == other.dst_path


    def __ne__(self, other):
        return not self.__eq__(other)


    def __hash__(self):
        my_hash = hash((self.dst_ip, self.src_path, self.dst_path))
        #print(str(self)+" :: "+my_hash)
        return my_hash
