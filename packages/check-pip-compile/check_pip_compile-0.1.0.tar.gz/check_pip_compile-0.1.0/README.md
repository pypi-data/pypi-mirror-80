# check_pip_compile

Automatically verify if you need to run pip-compile.

## Usage

You can use it as a pre-commit hook:

```yaml
-   repo: https://github.com/MartinThoma/check-pip-compile
    rev: 0.1.0
    hooks:
    -   id: check-pip-compile
        args: ['.']  # it's recommended to specify the files you want
```

or via command line:

```
$ check_pip_compile .
Run 'pip-compile requirements-dev.in' (2020-09-22 22:47:11.551971), as requirements-dev.txt (2020-09-02 09:53:58.287945) might be outdated
Run 'pip-compile setup.py', as no corresponding txt file exists

$ check_pip_compile setup.py requirements-lint.in
Run 'pip-compile setup.py', as no corresponding txt file exists
```
