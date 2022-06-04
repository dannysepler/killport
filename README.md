# `killport`

Kill processes using a given port on your laptop.

## Installation

`pip install killport`

## Usage

`killport 1234`
- kills any process using the 1234 port on your laptop

`killport 1234 2345`
- kills any process using either the 1234 or 2345 ports on your laptop

`killport 1234 --view-only`
- Displays the processes that would be deleted, but doesn't actually delete them.
