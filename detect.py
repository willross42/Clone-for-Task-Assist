import requests
import csv
import logging



def sniff_contents(response):
    chunks_it = response.iter_content(chunk_size=1024, decode_unicode=True)
    chunk = next(chunks_it)

    if '<?xml' in chunk:
        logging.info("sniff_contents - <?xml in chunk")
        return "xml"
    print("<?xml not in chunk")
    logging.info("sniff_contents - <?xml not in chunk")

    try:
        dialect = csv.Sniffer().sniff(chunk)
        if dialect.delimiter == '\t':
            logging.info("sniff_contents - sniff_test concludes tsv")
            return 'tsv'
        elif dialect.delimiter == '|':
            logging.info("sniff_contents - sniff_test concludes csv")
            return 'csv'
        else:
            logging.info("sniff_contents - sniff_test concludes None")
            return None
    except Exception as e:
        logging.exception("sniff_test - exception: %s", e)
        return None


def file_ext_test(link):
    file_extensions = {
        'xml': ['.xml'],
        'csv': ['.csv'],
        'tsv': ['.tsv', '.tab'],
    }

    for file_type, extensions in file_extensions.items():
        for extension in extensions:
            if link.endswith(extension):
                logging.info("file_ext_test - file_ext_test result: %s", file_type)
                return file_type

    logging.info("file_ext_test - file_ext_test inconclusive")
    return None


# Try sniff_contents, exception: try file extension check, exception: return None
def detect_filetype(link):
    with requests.get(link, allow_redirects=True, stream=True) as response:
        print(response)
        response.raise_for_status()
        try:
            return sniff_contents(response)
        except Exception as e:
            logging.info("detect_filetype - sniff_test inconclusive: %s", e)

            try:
                return file_ext_test(link)
            except Exception as exc:
                logging.info("detect_filetype - file_type_test inconclusive: %s", e)
                raise exc
