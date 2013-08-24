import sys
import yaml
import requests

def main(args):
    '''Main driver.'''

    reader, writer = setup(args)
    all_urls = yaml.load(reader)

    results = []
    for url in all_urls:
        info = fetch(url)
        info['slug'] = url.split('/')[-1]
        info['url'] = 'http://swcarpentry.github.io/{0}/'.format(info['slug'])
        results.append(info)

    yaml.dump(results, writer)
    reader.close()
    writer.close()

def setup(args):
    '''Parse command-line arguments and return input and output streams.'''
    reader = sys.stdin
    writer = sys.stdout
    if len(args) > 0:
        reader = open(args[0], 'r')
    if len(args) > 1:
        writer = open(args[1], 'w')
    return reader, writer

def fetch(url):
    '''Fetch information from a single online repository.'''
    url = url.replace('github.com', 'raw.github.com') + '/gh-pages/index.html'
    response = requests.get(url)
    header = response.text.split('---')[1]
    info = yaml.load(header)
    return info

if __name__ == '__main__':
    main(sys.argv[1:])
