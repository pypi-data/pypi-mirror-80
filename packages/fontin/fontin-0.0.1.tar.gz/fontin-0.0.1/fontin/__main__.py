import os
import tempfile
from pyunpack import Archive

from fontin.install_font import install_font
from fontin import FILE, clear

TEMPDIR = tempfile.gettempdir()

font_file_extensions = ('.ttf', '.otf', '.svg', '.eot', '.woff')

def extract():
    print('Extracting...')
    extracted_path = TEMPDIR + '\\fontin\\' + FILE + '\\'
    if not os.path.exists(extracted_path):
        os.makedirs(extracted_path)
    Archive(os.getcwd() + '\\' + FILE).extractall(extracted_path)
    clear()
    return extracted_path

def install_all(path):
    fonts = os.listdir(path)
    for font in fonts:
        if font.endswith(font_file_extensions):
            font_path = path + '\\' + font
            print('Installing font: ' + font)
            install_font(font_path)

def main():
    path = extract()
    install_all(path)
    print('--------')

if __name__ == '__main__':
    main()