
import os
from nose.tools import raises, assert_equal
from pprint import pprint
from io import StringIO
import wgrep


def data_path(path):
    "Absolute path to test data file."
    return os.path.join(os.path.dirname(__file__), 'data', path)


def test_pages0():
    "wgrep.pages('')"
    pages = tuple(wgrep.pages(StringIO(u'')))
    assert_equal(0, len(pages))


@raises(TypeError)
def test_pages1():
    'wgrep.pages(None)'
    tuple(wgrep.pages(None))


def test_pages2():
    'wgrep.pages(SIMPLE)'
    pages = tuple(wgrep.pages(open(data_path('simple-small-pages'))))
    assert_equal(2, len(pages))
    page = pages[0]
    assert_equal(7, len(page.body))
    page = pages[1]
    assert_equal(2, len(page.body))


def test_pages3():
    'wgrep.pages(NO PAGES)'
    pages = tuple(wgrep.pages(StringIO(u'HTTP/1.0 200 OK')))
    assert_equal(0, len(pages))


def test_pages4():
    'wgrep.pages(EMBEDDED STATUS)'
    pages = tuple(wgrep.pages(open(data_path('page-with-embedded-status'))))
    assert_equal(1, len(pages))
    page = pages[0]
    assert_equal(7, len(page.body))
