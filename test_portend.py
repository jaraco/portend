import socket
import contextlib
import os

import pytest

import portend


def socket_infos():
    """
    Generate addr infos for connections to localhost
    and if IPv6 is enabled to ::1 too.
    """
    host = None  # all available interfaces
    port = portend.find_available_local_port()
    if portend.is_ipv6_enabled():
        family = socket.AF_UNSPEC
    else:
        family = socket.AF_INET
    socktype = socket.SOCK_STREAM
    proto = 0
    flags = socket.AI_PASSIVE
    return socket.getaddrinfo(host, port, family, socktype, proto, flags)


def id_for_info(info):
	af, = info[:1]
	return str(af)


def build_addr_infos():
	params = list(socket_infos())
	ids = list(map(id_for_info, params))
	return locals()


@pytest.fixture(**build_addr_infos())
def listening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	if os.environ.get('TRAVIS') and af is socket.AF_INET6:
		pytest.xfail(reason="No IPv6 loopbak to connect; Ref #8.")
	sock = socket.socket(af, socktype, proto)
	sock.bind(sa)
	sock.listen(5)
	with contextlib.closing(sock):
		yield sa


@pytest.fixture(**build_addr_infos())
def nonlistening_addr(request):
	af, socktype, proto, canonname, sa = request.param
	return sa


class TestChecker:
	def test_check_port_listening(self, listening_addr):
		with pytest.raises(portend.PortNotFree):
			portend.Checker().assert_free(listening_addr)

	def test_check_port_nonlistening(self, nonlistening_addr):
		portend.Checker().assert_free(nonlistening_addr)
