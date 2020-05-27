import argparse
import os
from version import Version
from certificate import extract_public_certificates, generate_allods_certificate, update_game_version_certificate

parser = argparse.ArgumentParser()

subparser = parser.add_subparsers(dest='command')

show_parser = subparser.add_parser('show')
show_parser.add_argument('-v', '--version', type=argparse.FileType('rb'), help='game.version file', default='Profiles/game.version')

validate_parser = subparser.add_parser('validate', help='validate game files according to game.version file')
validate_parser.add_argument('-f', '--folder', type=str, help='game root folder', default='.')
validate_parser.add_argument('-v', '--version', type=argparse.FileType('rb'), help='game.version file', default='Profiles/game.version')
validate_parser.add_argument('-c', '--certificate', type=argparse.FileType('rb'), help='RSA certificate')
validate_parser.add_argument('--full', action='store_true', help='game.version will be validated first with certificate')

extract_cert_parser = subparser.add_parser('extract_certificate', help='extract public RSA certificate in DER format ')
extract_cert_parser.add_argument('file', type=argparse.FileType('rb'), help='file to extract public RSA certficates')
extract_cert_parser.add_argument('-o', '--out', type=str, help='output folder', default='certificates')

generate_cert_parser = subparser.add_parser('generate_certificate', help='generate public and private RSA certificates for Allods Online exe files')
generate_cert_parser.add_argument('-o', '--out', type=str, help='output folder', default='certificates')

update_cert_parser = subparser.add_parser('update_certificate', help='update game.version RSA certificate in Launcher.exe')
update_cert_parser.add_argument('exe', type=argparse.FileType('rb'), help='file to update public certficates')
update_cert_parser.add_argument('certificate', type=argparse.FileType('rb'), help='public RSA certificate to write in DER format')

args = parser.parse_args()


def show(stream):
    version = Version.parse(stream)
    stream.close()
    print(version)

def validate(folder, version_file, certificate, full):
    v = Version.parse(version_file)
    version_file.close()
    if full:
        if not v.validate(certificate.read()):
            print('game.version file is invalid for given RSA certificate')
        else:
            print('game.version is valid for given RSA certificate')
        certificate.close()
    invalid_files = v.validate_game(folder)
    if len(invalid_files) == 0:
        print('All files are validated')
    else:
        print('%i files are invalid' % len(invalid_files))
        print('%-100s%s' % ('File', 'Reason'))
        for file, reason in invalid_files:
            print('%-100s%s' % file.filename, reason)

if args.command == 'show':
    show(args.version)
elif args.command == 'validate':
    validate(args.folder, args.version, args.certificate, args.full)
elif args.command == 'extract_certificate':
    extract_public_certificates(args.file.read(), args.out)
    args.file.close()
elif args.command == 'generate_certificate':
    generate_allods_certificate(args.out)
elif args.command == 'update_certificate':
    update_game_version_certificate(args.exe.read(), args.certificate.read())
    args.exe.close()
    args.certficate.close()
