class RedirectionMock:
    def __init__(self, url):
        self.url = url


class ResponseMock:
    def __init__(self, headers={}, urls=[], fd=None, error=None):
        self.error = error
        self.headers = headers

        self.history = [RedirectionMock(url) for url in urls[:-1]]
        last_url = 'http://localhost/'
        for last_url in urls:
            pass
        self.url = last_url
        self.fd = fd

    def iter_content(self, chunk_size, decode_unicode):
        return ChunkIterator(self.fd, chunk_size)

    def raise_for_status(self):
        if self.error is not None:
            raise self.error

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.fd is not None:
            self.fd.close()
            self.fd = None


class ChunkIterator:
    def __init__(self, fd, chunk_size):
        self.fd = fd
        self.chunk_size = chunk_size

    def __next__(self):
        return self.fd.read(self.chunk_size)
