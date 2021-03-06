import os
import shutil
import sys
import time
import tempfile
from datetime import datetime as DT


from plexapi.video import Episode, Show, Movie
from plexapi.media import MediaPart
import pytest

fp = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bw_plex')

# I dont like it..
sys.path.insert(1, fp)

import bw_plex

TEST_ROOT = os.path.join(tempfile.gettempdir(), 'bw_plex_test_root')

# Delete any old test this was this shit keeps filling my disks.
# cba with travis.
if 'TRAVIS' not in os.environ and os.path.exists(TEST_ROOT):
    shutil.rmtree(TEST_ROOT)

bw_plex.init(folder=os.path.join(tempfile.gettempdir(), 'bw_plex_test_root'), debug=True)

# Do not remove these imports..
import bw_plex.plex as plex
import bw_plex.misc as misc
import bw_plex.hashing as hashing
import bw_plex.credits as credits
import bw_plex.edl as edl
from bw_plex.db import session_scope, Processed

TEST_DATA = os.path.join(os.path.dirname(__file__), 'test_data')


@pytest.fixture()
def outro_file():
    fp = os.path.join(TEST_DATA, 'out.mkv')
    return fp


@pytest.fixture()
def intro_file():
    fp = os.path.join(TEST_DATA, 'dexter_s03e01_intro.mkv')
    return fp


@pytest.fixture(scope='session')
def HT():
    return misc.get_hashtable()


@pytest.fixture()
def in_db(ratingkey):
    rk = int(ratingkey)
    with session_scope() as se:
        try:
            item = se.query(Processed).filter_by(ratingKey=rk).one()
            return item
        except NoResultFound:
            return


@pytest.fixture()
def episode(mocker):

    ep = mocker.MagicMock(spec=Episode)
    ep.TYPE = 'episode'
    ep.name = ''
    ep.title = ''
    ep.grandparentTitle = 'Dexter'
    ep.ratingKey = 1337
    ep.parentRatingKey = 1337
    ep._server = ''
    ep.title = 'Dexter'
    ep.index = 1
    ep.parentIndex = 1
    ep.grandparentRatingKey = 1337
    ep.grandparentTheme = ''
    ep.duration = 60 * 60 * 1000  # 1h in ms
    ep.updatedAt = DT(1970, 1, 1)

    def _prettyfilename():
        return 'Dexter.s01.e01'

    p = mocker.MagicMock(spec=MediaPart)
    p.file = os.path.join(TEST_DATA, 'dexter_s03e01_intro.mkv')

    def _iterParts():
        yield p

    ep._prettyfilename = _prettyfilename
    ep.iterParts = _iterParts

    return ep


@pytest.fixture()
def film(mocker):
    ep = mocker.MagicMock(spec=Movie)
    ep.TYPE = 'movie'
    ep.name = 'Random'
    ep.title = 'Random'
    ep.ratingKey = 7331
    ep._server = ''
    ep.duration = 60 * 60 * 1000  # 1h in ms
    ep.updatedAt = DT(1970, 1, 1)

    def _prettyfilename():
        return 'Random'

    p = mocker.MagicMock(spec=MediaPart)
    p.file = os.path.join(TEST_DATA, 'dexter_s03e01_intro.mkv')

    def _iterParts():
        yield p

    ep._prettyfilename = _prettyfilename
    ep.iterParts = _iterParts

    return ep


@pytest.fixture()
def media(mocker, episode):
    media = mocker.Mock(spec=Show)
    media.TYPE = 'show'
    media.name = 'dexter'
    media.ratingKey = 1337
    media.theme = ''
    media._server = ''
    media.title = 'dexter'

    def _episodes():
        return [episode]

    media.episodes = _episodes

    return media
