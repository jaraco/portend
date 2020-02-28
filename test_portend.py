import socket
import contextlib

import pytest
from tempora import timing

import portend


def socket_infos():
    """
    Generate addr infos for connections to localhost
    """
    host = None  # all available interfaces
    port = portend.find_available_local_port()
    family = socket.AF_UNSPEC
    socktype = socket.SOCK_STREAM
    proto = 0
    flags = socket.AI_PASSIVE
    return socket.getaddrinfo(host, port, family, socktype, proto, flags)


def id_for_info(info):
    (af,) = info[:1]
    return str(af)


def build_addr_infos():
    params = list(socket_infos())
    ids = list(map(id_for_info, params))
    return locals()


@pytest.fixture(**build_addr_infos())
def listening_addr(request):
    af, socktype, proto, canonname, sa = request.param
    sock = socket.socket(af, socktype, proto)
    sock.bind(sa)
    sock.listen(5)
    with contextlib.closing(sock):
        yield sa


@pytest.fixture(**build_addr_infos())
def nonlistening_addr(request):
    af, socktype, proto, canonname, sa = request.param
    return sa


@pytest.fixture
def immediate_timeout(monkeypatch):
    monkeypatch.setattr(timing.Timer, 'expired', lambda: True)


class TestChecker:
    def test_check_port_listening(self, listening_addr):
        with pytest.raises(portend.PortNotFree):
            portend.Checker().assert_free(listening_addr)

    def test_check_port_nonlistening(self, nonlistening_addr):
        portend.Checker().assert_free(nonlistening_addr)

    def test_free_with_immediate_timeout(self, nonlistening_addr, immediate_timeout):
        host, port = nonlistening_addr[:2]
        portend.free(host, port, timeout=1.0)

    def test_free_with_timeout(self, listening_addr):
        host, port = listening_addr[:2]
        with pytest.raises(portend.Timeout):
            portend.free(*listening_addr[:2], timeout=0.3)

    def test_occupied_with_immediate_timeout(self, listening_addr, immediate_timeout):
        host, port = listening_addr[:2]
        portend.occupied(host, port, timeout=1.0)


def test_main(listening_addr):
    target = portend.HostPort.from_addr(listening_addr)
    portend._main([target, 'occupied'])


def test_main_timeout(listening_addr):
    target = portend.HostPort.from_addr(listening_addr)
    with pytest.raises(SystemExit):
        portend._main([target, 'free', '-t', '0.1'])
