import json
import argparse
import time
import math
import requests


def get_page(page_id, access_token, query):
    api_url = "https://api.github.com/search/issues?access_token={0}&q={1}&page={2}".format(access_token, query, page_id)
    r = requests.get(api_url)
    if r.status_code == 403:
        reset = r.headers['X-RateLimit-Reset']
        return int(reset)
    return r.json()


def parse_page(page, access_token):
    issues = []
    for i in page['items']:
        issue = {}
        issue['title'] = i['title']
        issue['body'] = i['body']
        if i['comments'] != 0:
            issue['comments'] = get_comments(i['comments_url'], access_token)
        else:
            issue['comments'] = []
        issues.append(issue)
    return issues, page['total_count']


def get_comments(commit_url, access_token):
    commit_url += '?access_token=' + access_token
    r = requests.get(commit_url)
    if r.status_code == 200:
        j = r.json()
        return [i['body'] for i in j]
    return []


def process_page(page_id, access_token, query):
    page = get_page(page_id, access_token, query)
    if isinstance(page, int) == int:
        print('Hit rate-limit; sleeping...')
        time.sleep(page - time.time())
        page = get_page(page_id, access_token, query)
    return parse_page(page, access_token)


def main():
    access_token = "ADD_GITHUB_TOKEN_HERE"

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', action='store', dest='query', help='search query', required=True)
    parser.add_argument('-o', action='store', dest='output', help='output file name', required=True)
    parser.add_argument('--user', action='store', dest='user', help='limit search to a specific user (equivalent to -q user:foo)')
    parser.add_argument('--org', action='store', dest='org', help='limit search to a specific user (equivalent to -q org:foo)')
    args = parser.parse_args()

    query = args.query
    output = args.output
    if args.user:
        query += ' user:' + args.user
    if args.org:
        query += ' org:' + args.org

    results = []
    issues, count = process_page(1, access_token, query)
    results += issues

    num_of_pages = int(math.ceil(float(count)/30))
    # Only the first 1000 results are available (ceil(float(1000) / 30) = 34 pages)
    if num_of_pages > 34:
        num_of_pages = 34

    print('page: 1/%d' % num_of_pages)

    for i in range(2, num_of_pages):
        issues, _ = process_page(i, access_token, query)
        results += issues
        print('page: %d/%d' % (i, num_of_pages))
        i += 1

    f = open(output, 'w')
    json.dump(results, f)
    f.close()

if __name__ == '__main__':
    main()
