import re
import os
from Crypto.PublicKey import RSA

DER_HEADER = b'\x30\x81\x89\x02\x81\x81\x00'
DER_SIZE = 140

def extract_public_certificates(exe, outdir):
    os.makedirs(outdir, exist_ok=True)
    certificates_matches = re.finditer(DER_HEADER, exe)
    certificate_found = 0
    for m in certificates_matches:
        certificate_found += 1
        index = m.start(0)
        print("Potential public DER certificate found at index %s" % hex(index))
        file = open('%s/%s.der' % (outdir, index), "wb")
        file.write(exe[index:index+DER_SIZE])
        file.close()
    print('%s potential public DER certificate(s) found' % certificate_found)

def generate_allods_certificate(outdir):
    os.makedirs(outdir, exist_ok=True)
    key = RSA.generate(1024)
    f = open('%s/private.der' % outdir, 'wb')
    f.write(key.export_key('DER'))
    print('Private certificate generated %s' % outdir + '/private.der')
    f.close()
    f = open('%s/public.der' % outdir, 'wb')
    f.write(key.publickey().export_key('DER')[-140:]) # allods uses truncated certificate
    print('Public certificate generated %s' % outdir + '/public.der')
    f.close()

def update_game_version_certificate(aogame_exe, certificate):
    f = open(aogame_exe, 'r+b')
    exe = f.read()
    certificate = re.match(DER_HEADER, exe) # game.version certificate is the first one
    if certificate != None:
        offset = certificate.start(0)
        f.seek(offset)
        f.write(certificate)
        f.close()


