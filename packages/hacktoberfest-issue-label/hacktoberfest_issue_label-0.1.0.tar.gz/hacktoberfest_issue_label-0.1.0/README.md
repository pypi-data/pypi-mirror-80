# Hacktoberfest Label

#### Add Hacktoberfest to Github issues

By default, this script will add the issue label `Hacktoberfest` to any issue with the label `good first issue` on https://github.com/conan-io/conan.
However, you can customize the repository and issue label by arguments.

#### Usage

```
usage: hacktoberfest.py [-h] [--token TOKEN] [--repository REPOSITORY] [--issue ISSUE] [--label LABEL]

Apply Hacktoberfest label to Github issues.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Github API Token
  --repository REPOSITORY
                        Github organization/repository name
  --issue ISSUE, -i ISSUE
                        Update only one Github issue
  --label LABEL, -l LABEL
                        Update ALL issues based on label name
```

#### Authentication

The script consumes the developer [tokens](https://github.com/settings/tokens) for authentication.
It can be passed by the argument `--token`, or by the environment variable `GITHUB_OAUTH_TOKEN`.

#### Examples

* Add `Hacktoberfest` issue label to https://github.com/conan-io/conan, to all issues with `good first issue` (Default behavior)

    python hacktoberfest.py 

* Add `Hacktoberfest` issue label to https://github.com/foo/bar issue #5

    python hacktoberfest.py --repository=foo/bar --issue=5  

* Add 'Hacktoberfest' issue label to issue label to all issues with `bug`

    python hacktoberfest.py --label=bug

#### LICENSE
[MIT](LICENSE)
