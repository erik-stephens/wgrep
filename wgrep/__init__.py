"""
The wgrep package.
"""

import re
from collections import namedtuple


__all__ = ['Page', 'pages']


def pages(fPages):
    """
    Yield a new `Page` for each page in given input stream.

    The given input stream must start with these start-of-page lines:

        URL IP-ADDRESS TIMESTAMP CONTENT-TYPE BYTES
        PROTOCOL STATUS-CODE STATUS-MSG

    as in:

        http://searchengineland.com/Google-streamlines-search-options-30143 208.80.6.139 20120525125956 text/html 97819
        HTTP/1.1 200 OK
    """
    chunk = Chunk()
    for line in fPages:
        chunk.feed(line)
        next_chunk = chunk.get_next_chunk()
        if next_chunk:
            yield chunk.as_page()
            chunk = next_chunk
    if chunk.is_complete():
        yield chunk.as_page()


_Page = namedtuple('Page', [
    'url', 'ip', 'ts', 'content_type', 'size',
    'protocol', 'status', 'headers', 'body'])

class Page(_Page):
    """
    A read-only data structure with fields:
        - url:str
        - ip:str
        - ts:str
        - content_type:str
        - size:str - size of body in bytes
        - protocol:str (eg HTTP/1.1)
        - status:str (eg 200)
        - headers:dict
        - body:str
    """

is_status_line = re.compile('^(?P<protocol>HTTP/[01]\.\d) (?P<status>\d\d\d) [\S ]+[\r\n]+').match


def is_metadata_line(line):
    """
    True if looks like a valid metadata line.
    """
    # Trying to make sure a valid status line.  Not sure how robust a
    # check is needed here.
    return len(line.split()) == 5


class Chunk(object):

    @property
    def metadata_line(self):
        """
        The assumed 1st line of a page chunk.
        """
        return self.lines[0] if len(self.lines) >= 1 else None

    @property
    def status_line(self):
        """
        The assumed 2nd line of a page chunk.
        """
        return self.lines[1] if len(self.lines) >= 2 else None

    def __init__(self, lines=None):
        if lines:
            self.lines = list(lines)
        else:
            self.lines = []

    def feed(self, line):
        self.lines.append(line)

    def is_complete(self):
        """
        True if this chunk has valid metadata & status lines and a non-empty body
        """
        return len(self.lines) >= 3

    def at_next_chunk(self):
        """
        True if this chunk `is_complete` and at start of a new chunk.
        """
        return self.is_complete() and \
            is_metadata_line(self.lines[-2]) and \
            is_status_line(self.lines[-1])

    def get_next_chunk(self):
        """
        A new `Chunk` if `at_next_chunk`, otherwise None.
        """
        if self.at_next_chunk():
            return Chunk(self.lines[-2:])

    def as_page(self):
        """
        This chunk as a `Page`.
        """
        metadata = self.metadata_line.split()
        protocol, status, _ = self.status_line.split()

        headers = dict()
        header_pos = 2
        while self.lines[header_pos].strip():
            name, val = self.lines[header_pos].split(':', 1)
            headers[name.strip().lower()] = val.strip()
            header_pos += 1

        body_pos = None
        if self.at_next_chunk():
            body_pos = -2
        body = self.lines[header_pos+1:body_pos]

        return Page(
            url = metadata[0],
            ip = metadata[1],
            ts = metadata[2],
            content_type = metadata[3],
            size = metadata[4],
            protocol = protocol,
            status = status,
            headers = headers,
            body = body,
        )
