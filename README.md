# envdiff

Compare environment files without printing their values. Useful before switching deployments.

## Commands

Python 3.9+; no runtime packages.

```sh
python3 -m envdiff diff examples/local.env examples/staging.env
python3 -m envdiff diff examples/local.env examples/staging.env --ignore 'API_*' --json
python3 -m envdiff check examples/local.env examples/schema.json
```

Diff output contains names and `added`, `removed`, or `changed`, never values.
A difference or validation failure exits 1; unreadable or malformed input exits 2.
Schema checks support required values, integer bounds, booleans and choices.
Empty required values fail validation. Unknown variables are allowed.

The parser supports optional `export`, single or double quotes, and trailing
comments. Double quotes support escaped newline, tab, quote and backslash.
It does not execute shell code, expand variables, source files, or accept multiline
assignments. Duplicate names are errors. Key names themselves are not redacted;
do not put secrets in variable names.

```sh
python3 -m pip install -r requirements-dev.txt
make test
make lint
```
