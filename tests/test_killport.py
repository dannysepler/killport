from __future__ import annotations

import http.server
import re
import signal

import pytest

from killport import TERM_SIGNAL, get_processes, kill_ports

PORT = 2345


@pytest.fixture(scope='session', autouse=True)
def term_handler():
    # if a TERM_SIGNAL (such as SIGTERM) is given, pytest abruptly stops
    # https://github.com/pytest-dev/pytest/issues/5243

    def do_nothing(*args, **kwargs):
        ...

    orig = signal.signal(TERM_SIGNAL, do_nothing)
    yield
    signal.signal(TERM_SIGNAL, orig)


@pytest.fixture
def server() -> http.server.HTTPServer:
    Handler = http.server.BaseHTTPRequestHandler

    httpd = http.server.HTTPServer(('localhost', PORT), Handler)
    yield httpd
    httpd.server_close()


def test_get_processes_when_no_process():
    assert len(get_processes([PORT])) == 0


def test_get_processes_when_process(server):
    assert len(get_processes([PORT])) == 1


def test_kills_port_when_desired(server, capsys):
    kill_ports(ports=[PORT])

    output = capsys.readouterr().out
    assert re.match(
        'Killing:\n'
        rf'- \S* \(pid \d+\) on port {PORT}',
        output,
    )


def test_kills_processes_in_order_of_port(capsys):
    Handler = http.server.BaseHTTPRequestHandler

    # Spins off 5555 then 1111, we want to kill 1111 first
    httpd_5555 = http.server.HTTPServer(('localhost', 5555), Handler)
    httpd_1111 = http.server.HTTPServer(('localhost', 1111), Handler)

    kill_ports(ports=[5555, 1111])

    output = capsys.readouterr().out
    assert re.match(
        'Killing:\n'
        r'- \S* \(pid \d+\) on port 1111\n'
        r'- \S* \(pid \d+\) on port 5555',
        output,
    )

    httpd_5555.server_close()
    httpd_1111.server_close()


def test_doesnt_destroy_irrelevant_port(server, capsys):
    kill_ports(ports=[PORT + 1])

    output = capsys.readouterr().out
    assert output == ''


def test_view_only_doesnt_destroy_port(server, capsys):
    kill_ports(ports=[PORT], view_only=True)

    output = capsys.readouterr().out
    assert re.match(
        'Would kill:\n'
        rf'- \S* \(pid \d+\) on port {PORT}',
        output,
    )
