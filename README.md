# wgrep

A grep-like utility for common crawl files using a jquery-like api (pyquery).

Standing on the shoulders of pyquery & lxml, this utility produces
line-oriented data using a jquery-like api to search elements from
common crawl pages.

Home page: https://github.com/erik-stephens/wgrep

[![Build Status](https://api.travis-ci.org/erik-stephens/wgrep.png?branch=master,develop)](http://travis-ci.org/erik-stephens/wgrep)

## Expressions

Search is performed by defining expressions to evaluate against each
page.  Expressions must be defined in a separate python package or
module somewhere in your PYTHONPATH.  Expression functions accept a
`wgrep.Page` instance and a `pyquery.PyQuery` instance and should
return a string.

There is a special "module" `page` that exposes some built-in page
data as expressions.  The following attributes are available:

- url:str
- ip:str
- ts:str
- content_type:str
- size:str - size of body in bytes
- protocol:str (eg HTTP/1.1)
- status:str (eg 200)
- headers:dict
- body:str

An example:

    DELIM=$'\t' wgrep page.url expr.title expr.twitter < common-crawl-file

assumes there is a python module `expr` with functions `title` and `twitter`:

    def title(page, pyqry):
        return pyqry('title').text()

    def twitter(page, pyqry):
        def handle(i, el):
            return '@' + pyqry(el).attr('href').split('twitter.com/', 1)[1]
        return ','.join(pyqry('a[href*="twitter.com/"]').map(handle))

## Development

Please report any defects or feature requests via Github Issues.
Developed using python virtualenv and should work for versions 2.7 and
3.3.  The following commands assume current working directory is the
base dir of wgrep checkout.

Create a python virtual environment somewhere (eg .env).

    virtualenv ~/.pyenv/wgrep
    source ~/.pyenv/wgrep/bin/activate

Install required packages:

    pip install -r requirements.txt --use-mirrors

If having trouble installing lxml on OS X, this might help:

    STATIC_DEPS=true pip install -v lxml

To run the tests:

    nosetests
