import requests
import csv
import logging


def by_file_name(link):
    file_extensions = {
        'xml': ['.xml'],
        'csv': ['.csv'],
        'tsv': ['.tsv', '.tab'],
    }

    for file_type, extensions in file_extensions.items():
        for extension in extensions:
            if link.endswith(extension):
                logging.info("detect.by_file_name: %s", file_type)
                return file_type

    logging.info("detect.by_file_name: None")
    return None


def by_content_type(response):
    # content_types = {
    #     'xml': (['text/xml', 'application/xml'], ['xml']),
    #     'csv': (['text/csv'], []),
    #     'tsv': (['text/tab-separated-values'], []),
    # }
    content_types = {
        'xml': ['xml'],
        'csv': ['text/csv'],
        'tsv': ['text/tab-separated-values'],
    }

    response_content_type = response.headers.get('Content-Type')
    logging.info("detect.by_content_type: response.headers - %s", response_content_type)
    if not response_content_type:
        return None

    # match = content_types.match(content_type)
    # if match is None:
    #     return None

    # (media_type, suffix) = (match['media_type'], match['suffix'])
    #
    for file_type, content_type in content_types.items():
        for item_type in content_type:
            if item_type in response_content_type:
                logging.info("detect.by_content_type: %s", file_type)
                return file_type
    logging.info("detect.by_content_type: None")


def by_sniff_contents(response):
    chunks_it = response.iter_content(chunk_size=1024, decode_unicode=True)
    chunk = next(chunks_it)

    if '<?xml' in chunk:
        logging.info("detect.by_sniff_contents: <?xml in chunk")
        return "xml"
    logging.info("detect.by_sniff_contents: <?xml not in chunk. Continue sniff")

    try:
        dialect = csv.Sniffer().sniff(chunk)
        if dialect.delimiter == '\t':
            logging.info("detect.by_sniff_contents: tsv")
            return 'tsv'
        elif dialect.delimiter == '|':
            logging.info("detect.by_sniff_contents: csv")s
            return 'csv'
        else:
            logging.info("detect.by_sniff_contents: None")
            return None
    except Exception as e:
        logging.exception("detect.by_sniff_contents: exception - %s", e)
        return None


# Try sniff_contents, exception: try file extension check, exception: return None
def detect_filetype(link):
    with requests.get(link, allow_redirects=True, stream=True) as response:
        logging.info("detect.detect_filetype: %s", response)
        response.raise_for_status()
        return (by_file_name(link) or by_content_type(response) or by_sniff_contents(response))
