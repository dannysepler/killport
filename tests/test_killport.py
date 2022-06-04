from __future__ import annotations

import http.server

import pytest

from killport import get_processes, kill_ports

PORT = 2345


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


@pytest.mark.skip('Figure out how to test this')
def test_kills_port_when_desired(server):
    assert len(get_processes([PORT])) == 1
    kill_ports(ports=[PORT])
    assert len(get_processes([PORT])) == 0


def test_doesnt_destroy_irrelevant_port(server):
    assert len(get_processes([PORT])) == 1
    kill_ports(ports=[PORT + 1])
    assert len(get_processes([PORT])) == 1


def test_view_only_doesnt_destroy_port(server):
    assert len(get_processes([PORT])) == 1
    kill_ports(ports=[PORT], view_only=True)
    assert len(get_processes([PORT])) == 1
