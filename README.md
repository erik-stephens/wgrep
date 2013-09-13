# wgrep

A grep-like utility for web content using CSS selectors

## Examples

To grep basic metadata:

    wgrep page.size page.ts page.url < common-crawl-file

To grep DOM elements:

    wgrep expr.title expr.twitter_handles < common-craw-file

assumes there is a python module `expr` with functions `title` and `twitter`:

    def title(page, jquery):
        return jquery('title').text()

    def twitter(page, pyqry):
        def handle(i, el):
            return '@' + pyqry(el).attr('href').split('twitter.com/', 1)[1]
        return ','.join(pyqry('a[href*="twitter.com/"]').map(handle))

## Setup

The following commands assume current working directory is the base
dir of wgrep checkout.

Create a python virtual environment somewhere (eg wgrep/.env).

    virtualenv .env

Install latest pyquery:

    pip install git+git://github.com/gawel/pyquery.git

Install all other required packages:

    pip install -r requirements.txt

If having trouble installing lxml on OS X, this might help:

    STATIC_DEPS=true pip install -v lxml

## Test Suite

From the base wgrep dir:

    PYTHONPATH=. nosetests -s -v wgrep.test
