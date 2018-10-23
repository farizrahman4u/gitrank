import requests
import sys

_cache = {}

def _read(url):
    text = _cache.get(url)
    if text is None:
        text = requests.get(url).text
        if not text:
            raise Exception('Empty response. Check connectivity.')
        _cache[url] = text
    return text


def get_contribs(username):
    url = 'https://www.github.com/' + username
    text = _read(url)
    if text.split('<title>')[1][:len(username)].lower() != username.lower():
        raise Exception('Invalid user name: ' + username)
    if 'contributions in the last year' not in text:
        return 0
    contribs = text.split('contributions in the last year')[0]
    contribs = contribs.split('>')[-1]
    contribs = ''.join(filter(lambda x: x <= '9' and x >= '0', contribs))
    contribs = int(contribs)
    return contribs


if sys.version_info[0] == 2:
    input = raw_input


input_file = input('Enter input file name: ')
output_file = input('Enter output file name (Default output.csv): ')

if not output_file.replace(' ', ''):
    output_file = 'output.csv'

def _username_from_row(row):
    x = row.split('github.com/')[1]
    x = x.split(',')[0]
    x = x.split('/')[0]
    return x


with open(input_file, 'r') as fin:
    with open(output_file, 'w') as fout:
        line0 = fin.readline()
        if 'github.com/' in line0:
            # no csv header
            username = _username_from_row(line0)
            print('Fetching contributions: ' + username)
            try:
                contribs = str(get_contribs(username))
            except Exception as e:
                print('Failed: ' + username)
                print(e)
                contribs = 'N/A'
            fout.write(line0[:-1] + ',' + contribs + '\n')
        else:
            fout.write(line0[:-1] + ',' + 'Github contributions\n')
        for line in fin:
            username = _username_from_row(line)
            print('Fetching contributions: ' + username)
            try:
                contribs = str(get_contribs(username))
            except Exception as e:
                print('Failed: ' + username)
                print(e)
                contribs = 'N/A'
            fout.write(line0[:-1] + ',' + contribs + '\n')
