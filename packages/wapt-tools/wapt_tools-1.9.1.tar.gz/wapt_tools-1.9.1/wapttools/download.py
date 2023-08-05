import glob
import logging
import os
import requests
import sys

log = logging.getLogger()


def download(url, pathname, clean=True):
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
    else:
        log.debug('{} already exists'.format(pathname))
