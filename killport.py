from __future__ import annotations

import argparse
from signal import SIGINT
from typing import NamedTuple

import psutil


class ProcessInfo(NamedTuple):
    port: int
    process: psutil.Process


def get_processes(ports: list[int]) -> list[ProcessInfo]:
    processes = set()
    for process in psutil.process_iter():
        try:
            conns = process.connections(kind='inet')
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue

        for conn in conns:
            port = conn.laddr.port
            if port in ports:
                processes.add(ProcessInfo(port=port, process=process))

    return sorted(processes, key=lambda p: (p.port, p.process.name()))


def kill_ports(*, ports: list[int], view_only: bool = False) -> int:
    processes = get_processes(ports)
    if processes:
        print('Killing:' if not view_only else 'Would kill:')

    for pinfo in processes:
        process = pinfo.process
        print(f'- {process.name()} (pid {process.pid}) on port {pinfo.port}')
        if not view_only:
            process.send_signal(SIGINT)

    return 1 if processes else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('ports', type=int, nargs='*')
    parser.add_argument('--view-only', action='store_true')
    args = parser.parse_args()

    return kill_ports(ports=args.ports, view_only=args.view_only)


if __name__ == '__main__':
    raise SystemExit(main())
