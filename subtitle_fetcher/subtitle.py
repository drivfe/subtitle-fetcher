from __future__ import print_function
import os
import hashlib
import sys
import requests

USER_AGENT = 'SubDB/1.0 (ajayrfhp/0.1; https://github.com/ajayrfhp/subtitle-fetcher)'
BASE_URL = 'http://api.thesubdb.com/?'
CONTENT = {
    'action': 'download',
    'language': 'en'
}

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def get_subtitle(path):
    hashed = get_hash(path)
    content = CONTENT
    content.update({'hash': hashed})

    headers = {'User-Agent': USER_AGENT}
    subtitles = requests.get(BASE_URL, params=content, headers=headers).content

    file_name = os.path.splitext(path)[0] + '.srt'
    with open(file_name, 'wb') as f:
        f.write(subtitles)

    print('Subtitles for {} downloaded.'.format(os.path.basename(path)))

def main(path=None):
    args = ' '.join(sys.argv[1:])
    files = []
    extensions = ['.mp4', '.mkv', '.flv', '.wmv', '.avi']

    if len(sys.argv) < 2:
        args = os.getcwd()

    if os.path.isdir(args) and os.path.exists(args):
        files = [os.path.join(args, f) for f in os.listdir(args) if os.path.splitext(f)[1] in extensions]
        if len(files) < 1:
            sys.exit('No video files found in {}.'.format(args))

    if os.path.isfile(args) and os.path.exists(args):
        files = [args]
        
    if len(files) < 1:
        sys.exit('File {} does not exist.'.format(args))

    for f in files:
        subtitle = get_subtitle(f)

if __name__ == '__main__':
    main()