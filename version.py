import io
import os
from zlib import decompress
from Crypto.Signature import pss
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from tqdm import tqdm

MD5_LEN = 16
SALT_BYTES = 8
BYTEORDER = 'little'

def read_int(stream):
    return int.from_bytes(stream.read(4), BYTEORDER)

def read_string(stream):
    size = read_int(stream)
    return stream.read(size).decode('utf-8')

def parse_index(bytes):
    files = []
    stream = io.BytesIO(bytes)
    foldercount = read_int(stream)

    for _ in range(foldercount):

        stream.read(4) # unknown value
        foldername = read_string(stream)
        filecount = read_int(stream)
        
        for _ in range(filecount):

            filename = read_string(stream)
            filesize = read_int(stream)
            md5 = stream.read(MD5_LEN).hex()
            stream.read(17) # unknown value
            files.append(FileVersion(foldername + filename, filesize, md5))

    return files

class Version:

    @staticmethod
    def parse(stream):
        body_size = read_int(stream)
        body = stream.read(body_size)
        md5 = MD5.new(body)
        signature_size = read_int(stream)
        signature = stream.read(signature_size)
        stream.seek(4) # go back to begining of body to parse
        ver = stream.read(4).decode('utf-8')
        id = read_string(stream)
        compressed_data_size = read_int(stream)
        compressed_data = stream.read(compressed_data_size)
        files = parse_index(decompress(compressed_data))
        return Version(ver, id, md5, files, signature)

    def __init__(self, ver, id, md5, files, signature):
        self.ver = ver
        self.id = id
        self.files = files
        self.signature = signature
        self.md5 = md5

    def __str__(self):
        out = ['ver: %s' % self.ver, 'id: %s' % self.id, 'md5: %s' % self.md5.hexdigest(), '\n%-100s%-20s%s\n' % ('File', 'Size', 'MD5')]
        for file in self.files:
            out.append('%-100s%-20s%s' % (file.filename, file.size, file.md5))
        return '\n'.join(out)

    def validate(self, rsa_key):
        verifier = pss.new(RSA.import_key(rsa_key), salt_bytes=SALT_BYTES)
        try:
            verifier.verify(self.md5, self.signature)
            return True
        except (ValueError, TypeError):
            return False

    def validate_game(self, game_folder):
        invalid_files = []
        pbar = tqdm(total=len(self.files))
        for file in self.files:
            path = game_folder + file.filename
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    content = f.read()
                    hash = MD5.new(content).hexdigest()
                    if len(content) != file.size and hash != file.md5:
                        invalid_files.append((file, 'incorrect MD5'))
            else:
                invalid_files.append((file, 'missing file'))
            pbar.update(1)
        pbar.close()
        return invalid_files
        
class FileVersion:

    def __init__(self, filename, size, md5):
        self.filename = filename
        self.size = size
        self.md5 = md5

    def validate(self, size, md5):
        return self.size == size and self.md5 == md5
