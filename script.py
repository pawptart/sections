from bs4 import BeautifulSoup as bs
import re
import os


def iterate(directory):
    for filename in os.listdir(directory):
        if filename.endswith('html'):
            file_object = parse(os.path.join(directory, filename))
            write_file(file_object, os.path.join('parsed_html', new_filename(filename)))
        else:
            continue

def parse(file_path):
    with open(file_path, 'r') as f:
        parser = bs(f.read(), 'lxml-html')
        
        file_headers_object = {}

        for section in parser.find_all('section'):
            section_headers = re.findall(r'(?=\#+\s).*', section.text)

            if len(section_headers) == 0:
                continue

            major_header = strip_header(section_headers[0])

            for header in section_headers[1:]:
                stripped_header = strip_header(header)
                if major_header in file_headers_object.keys():
                    if stripped_header not in file_headers_object[major_header]:
                        file_headers_object[major_header].append(stripped_header)
                else:
                    file_headers_object[major_header] = [stripped_header]

    return file_headers_object

def write_file(file_object, file_path):
    with open(file_path, 'w') as f:
        for key in file_object.keys():
            f.write(key + '\n')

            for item in file_object[key]:
                f.write(' - ' + item + '\n')

            f.write('\n')

def new_filename(filename):
    return 'parsed_' + re.sub('.html', '.txt', filename)

def strip_header(header):
    return re.sub(r'^\s?\#+\s', '', header)

if __name__ == '__main__':
    iterate('html')