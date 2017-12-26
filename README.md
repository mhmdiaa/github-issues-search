# github-issues-search

A simple command-line tool to search GitHub issues.

**Note**: this tool can fetch up to 1000 results per query due to [GitHub API search limit](https://developer.github.com/v3/search/). If you need more, [be clever](https://stackoverflow.com/a/37639739).

## Output Schema
The output is saved as a JSON file following this schema
```
[
    {
        "title": "title",
        "body": "body",
        "comments": [
            "comment1",
            "comment2"
        ]
    }
]
```

## Installation
1. Install `requests`.
```
pip install requests
```

2. Replace the value of the `access_token` variable with your [GitHub token](https://github.com/settings/tokens) (doesn't need to have any permissions; therefore don't give it any).
```
access_token = "ADD_GITHUB_TOKEN_HERE"
```

## Usage
```
usage: github-issues.py [-h] -q QUERY -o OUTPUT [--user USER] [--org ORG]

optional arguments:
  -h, --help   show this help message and exit
  -q QUERY     search query
  -o OUTPUT    output file name
  --user USER  limit search to a specific user (equivalent to -q user:foo)
  --org ORG    limit search to a specific user (equivalent to -q org:foo)
```
