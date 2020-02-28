2.6
===

Package refresh.

2.5
===

#10: Fix race condition in ``occupied`` and ``free``.

2.4
===

#6: ``find_available_local_port`` now relies on
    ``socket.getaddrinfo`` to find a suitable address
    family.

2.3
===

Package refresh.

2.2
===

Merge with skeleton, including embedded license file.

2.1.2
=====

Fix README rendering.

2.1.1
=====

#5: Restored use of ``portend.client_host`` during
    ``assert_free`` check on Windows, fixing check
    when the bind address is *ADDR_ANY.

2.1
===

Use tempora.timing.Timer from tempora 1.8, replacing
boilerplate code in occupied and free functions.

#1: Removed ``portend._getaddrinfo`` and its usage in
    ``Checker.assert_free``.

Dropped support for Python 2.6.

1.8
===

Remove dependency on ``jaraco.compat`` and instead just
copy and reference the ``total_seconds`` compatibility
function for Python 2.6.

1.7.1
=====

* 2: Use tempora, replacing deprecated jaraco.timing.

1.7
===

Expose the port check functionality as ``portend.Checker`` class.

1.6.1
=====

Correct failures on Python 2.6 where
``datetime.datetime.total_seconds``
and argparse are unavailable.

1.6
===

Add support for Python 2.6 (to support CherryPy).

1.5
===

Automatically deploy tagged versions via Travis-CI.

1.4
===

Moved hosting to Github.

1.3
===

Added ``find_available_local_port`` for identifying a local port
available for binding.

1.2
===

Only require ``pytest-runner`` when pytest is invoked.

1.1
===

Renamed functions:

 - wait_for_occupied_port: occupied
 - wait_for_free_port: free

The original names are kept as aliases for now.

Added execution support for the portend module. Invoke with
``python -m portend``.

1.0
===

Initial release based on utilities in CherryPy 3.5.
