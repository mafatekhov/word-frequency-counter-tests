"""
Download all files from opened pull request
"""

import os
import sys

from requests import get
import urllib3


def get_by_url(url):
    d_req = dict(url=url)
    responce = get(**d_req)
    content = responce.json()
    return content


def download_file(from_url, to_url):
    http = urllib3.PoolManager()
    req = http.request('GET', from_url, preload_content=False)

    with open(to_url, 'wb') as out:
        while True:
            data = req.read(100)
            if not data:
                break
            out.write(data)
    req.release_conn()


def main():
    if "TRAVIS_COMMIT" not in os.environ or "FIPL_ACCESS_TOKEN" not in os.environ:
        print('Need proper environment variables')
        sys.exit(1)

    current_commit_hash = os.environ['TRAVIS_COMMIT']
    access_token = os.environ['FIPL_ACCESS_TOKEN']

    token = '?access_token={}'.format(access_token)
    base_url = 'https://api.github.com/repos/fipl-hse/word-frequency-counter-tests'

    content = get_by_url(url='{}/pulls{}&state=all'.format(base_url, token))
    for pull_req in content:
        pr_id = pull_req["number"]
        files_from_pr = get_by_url(
            url='{}/pulls/{}/files{}&state=all'.format(base_url, pr_id, token))
        for pr_file in files_from_pr:
            target_url = pr_file['raw_url']
            file_name = '/'.join(target_url.split('/')[-2:])
            source_hash = target_url.split('/')[-3]

            if source_hash == current_commit_hash:
                continue
            to_url = os.path.join('tmp',
                          '{}_{}.{}'.format(file_name.split('.')[0],
                                            source_hash,
                                            file_name.split('.')[1]))

            os.makedirs(os.path.dirname(to_url), exist_ok=True)

            download_file(from_url=target_url, to_url=to_url)

if __name__ == '__main__':
    main()
