# pcfuzzer

A simple fuzzer using [pysource-codegen](https://github.com/15r10nk/pysource-codegen), targeting Python formatters.

## Usage

```shell
# example: black test.py
make arg=black==24.0.4

# check log
docker logs pcfuzzer:black-24.0.4
```

results will be stored at `results/` directory.

## TODO

- [ ] Support specific command and option in Dockerfile
- [ ] Reproducing using result json files
- [ ] Minimize pyload with [pysource-minimize](https://github.com/15r10nk/pysource-minimize)
