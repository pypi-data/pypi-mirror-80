import anybadge
import bs4
import logging
import json
import re
import requests
import os
from .config import loadControl, loadVersionCheck

log = logging.getLogger()

chat_message = """
New version of *{package}* have beed released.

Current version: {old_version}
Latest version: *{new_version}*

Jump to {homepage}
"""


def latestVersion():
    """ Extract latest version defined by version-check.json

    Returns
    -------
    version: string
        version extracted from web page
    """
    config = loadVersionCheck()

    content = requests.get(config['url_version']).text.strip()

    if config['html'] is True:
        soup = bs4.BeautifulSoup(content, 'html.parser')
        if 'index' in config:
            index = config['index']
        else:
            index = 0
        latest_version = soup.select(config['selector'])[index].contents[0].strip()
    else:
        latest_version = content

    if 'cleaners' in config and len(config['cleaners']) > 0:
        for cleaner in config['cleaners']:
            latest_version = re.sub(cleaner['pattern'], cleaner['rewrite'], latest_version, flags=re.DOTALL).strip()

    return latest_version


def versionChecker(chat=False, badge=False):
    """ Compare latest version defined by version-check.json, versus WAPT/control one

    Parameters
    ----------
    chat: bool
        send results to chat
    badge: bool
        generate upstream badge

    Returns
    -------
    results: bool
        version mismatch
    """
    log.debug('versionChecker')

    control = loadControl()
    log.info('Current {} version: {}'.format(control['name'], control['version']))

    latest_version = latestVersion()
    log.info('Latest {} version: {}'.format(control['name'], latest_version))

    if control['version'] != latest_version:
        log.info('New version available, please upgrade package')

        if chat:
            log.debug('Sending message to Chat webhook ...')
            if 'CHAT_WEBHOOK_URL' in os.environ:
                requests.session().post(
                    os.environ['CHAT_WEBHOOK_URL'],
                    data=json.dumps({
                        'text': chat_message.format(
                            package=control['name'],
                            old_version=control['version'],
                            new_version=latest_version,
                            homepage=control['homepage'])
                    }),
                    headers={'Content-Type': 'application/json; charset=UTF-8'}
                )
            else:
                log.warning('CHAT_WEBHOOK_URL environment variable not defined, unable to send chat message')
            log.debug('... done.')

        if badge:
            log.debug('generating badge ...')
            badge = anybadge.Badge(label='upstream', value='new', default_color='red')
            badge.write_badge('upstream.svg')

        return True

    if badge:
        log.debug('generating badge ...')
        badge = anybadge.Badge(label='upstream', value='ok', default_color='green')
        badge.write_badge('upstream.svg')

    return False
