# oh-my-stars

Search your stars locally.

```
usage: __main__.py [-h] [-l LANGUAGE [LANGUAGE ...]] [-u] [-r] [-a] [-3] [-i]
                   [-v]
                   [keywords [keywords ...]]

a CLI tool to search your starred Github repositories.

positional arguments:
  keywords              Search by keywords

optional arguments:
  -h, --help            show this help message and exit
  -l LANGUAGE [LANGUAGE ...], --language LANGUAGE [LANGUAGE ...]
                        Filter by language
  -u, --update          Create(first time) or update the local stars index
  -r, --reindex         Re-create the local stars index
  -a, --alfred          Format search result as Alfred XML
  -3, --alfred3
  -i, --install         Import Alfred workflow
  -v, --version         show program's version number and exit
```

##### Works with Alfred Workflow

![oh-my-stars-alfred-workflow](https://raw.github.com/wolfg1969/my-stars-pilot/master/oh-my-stars-alfred-workflow.png)

##### v1.3.3
- Output Alfred 3 JSON ouput with "-a -3" option.
- Import Alfred Workflow with "-i" (append "-3" for Alfred 3) option.

##### v1.2.3
- Get user + password from netrc. @jhermann.
- Use pipenv to manage project requirements.

##### v1.1.3
- Upgrade to TinyDB 3.7.0.
- Build index when updating.
- Search result pagination.

*Note*
- Uninstall existing version.
- Rebuild existing index with `mystars -r`.

##### v1.0.2
- Rename to oh-my-stars.

##### v1.0.1
- Support Github two-factor authentication. @yanyaoer

##### v1.0.0

- Replace kc with [TinyDB](https://github.com/msiemens/tinydb), no more non-python dependencies.
- Only update stars since last time.

##### Installation (Mac OSX)
```
$ pip install oh-my-stars --upgrade
$ mystars --help
$ mystars --update
$ mystars angular upload
$ mystars --language python
$ mystars awesome python
``` 

if install failed, try following commands
```
$ pip uninstall distribute
$ pip install setuptools
$ pip install --upgrade setuptools
```

![oh-my-stars](https://raw.github.com/wolfg1969/my-stars-pilot/master/oh-my-stars.png)
