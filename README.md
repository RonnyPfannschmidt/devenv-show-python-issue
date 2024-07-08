# repo demonstrates the lack of mypy usable with nix based python


## with venv - no issues
```
$ nix develop .#venv --impure
$ mypy mc_convert.py # no issues

```


# with nix - mypy broken

```
$ nix develop .#nix --impure
$ mypy mc_convert.py # all errors
$ python -m mypy mv_convert.py # same
```

