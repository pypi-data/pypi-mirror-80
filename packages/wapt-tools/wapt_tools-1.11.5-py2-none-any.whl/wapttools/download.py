import glob
import logging
import os
import requests
import sys
from .hash import sha256sum

log = logging.getLogger()


def save_url_to_file(url, pathname):
    try:
        r = requests.get(url, stream=True)
        if not r.ok:
            log.critical('failed to download {} from {}, 404 not found'.format(os.path.basename(pathname), url))
            sys.exit(1)

        with open(pathname, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        del r
    except Exception as e:
        log.critical('failed to download {} from {}, {}'.format(os.path.basename(pathname), url, e))
        sys.exit(1)


def download(url, pathname, clean=True, checksum=None):
    """ Download the file at a given url and save it to pathname.

    The files existing in the same folder and with the same extension are removed if clean=True.

    Parameters
    ----------
    url: string
        url of the file to be dowloaded
    pathname: string
        pathname of the file to be saved
    clean: boolean
        cleanup needed
    """
    extension = os.path.splitext(pathname)[1]

    dirname = os.path.dirname(pathname)

    if clean:
        pattern = os.path.join(dirname, '*{}'.format(extension))
        log.debug('cleaning files {} except {}'.format(pattern, pathname))
        for file in glob.glob(pattern):
            if file != pathname:
                log.debug('removing {}'.format(file))
                os.remove(file)

    log.info('downloading {} from {}'.format(os.path.basename(pathname), url))

    if not os.path.exists(pathname):
        save_url_to_file(url, pathname)
    else:
        if checksum:
            computed = sha256sum(pathname)
            if computed != checksum:
                log.info('{file} checksum mismatch, downloading'.format(file=pathname))
                os.remove(pathname)
                save_url_to_file(url, pathname)
        else:
            log.debug('{} already exists'.format(pathname))

    if checksum:
        computed = sha256sum(pathname)
        if computed != checksum:
            os.remove(pathname)
            log.critical('{file} checksum mismatch, downloaded file deleted'.format(file=pathname))
            sys.exit(1)
