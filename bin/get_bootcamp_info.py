import sys
import yaml
import requests

def main(args):
    '''Main driver.'''

    reader, writer = setup(args)
    repositories = yaml.load(reader)

    results = []
    for repo in repositories:
        info = fetch(repo)
        info['slug'] = repo.split('/')[-1]
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

def fetch(repo):
    '''Fetch information from a single online repository.'''
    url = repo.replace('github.com', 'raw.github.com') + '/gh-pages/index.html'
    response = requests.get(url)
    header = response.text.split('---')[1]
    info = yaml.load(header)
    return info

if __name__ == '__main__':
    main(sys.argv[1:])
