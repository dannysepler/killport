# `killport`

Kill processes using a given port on your laptop.

## Installation

`pip install killport`

## Usage

`killport 1111`
- kills any process using the 1111 port on your laptop

`killport 1111 2222`
- kills any process using either the 1111 or 2222 ports on your laptop

`killport 1111 --view-only`
- Displays the processes that would be deleted, but doesn't actually delete them.

## How does this differ from...

- [freeport](https://github.com/yashbathia/freeport/) -- Windows support, since this uses `psutil` rather than `lsof`
- [kill-port](https://github.com/tiaanduplessis/kill-port) -- Very similar, but this is available in PyPI vs NPM
