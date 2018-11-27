from __future__ import absolute_import

import os.path

from ansible import constants as C
import pytest
from six.moves import range


@pytest.fixture
def host(ansible_adhoc, monkeypatch):
    # Monkeypatch Ansible's plugin lookup path to cover our lookup plugins
    monkeypatch.setattr(
        C,
        "DEFAULT_LOOKUP_PLUGIN_PATH",
        C.DEFAULT_LOOKUP_PLUGIN_PATH + [os.path.dirname(__file__)],
    )
    return ansible_adhoc(inventory="localhost,").localhost


def test_cached(host, tmpdir):
    original_contents = "old"
    new_contents = "new"

    path = tmpdir.join("file.txt")
    path.write(original_contents)

    # Cache the original contents
    cached_result = host.debug(msg="{{ lookup('cached', 'file', '%s') }}" % path)
    assert len(cached_result) == 1
    assert cached_result.localhost.is_ok
    assert cached_result.localhost["msg"] == original_contents

    # An un-cached lookup gets the new contents
    path.write(new_contents)
    uncached_result = host.debug(msg="{{ lookup('file', '%s') }}" % path)
    assert len(uncached_result) == 1
    assert uncached_result.localhost.is_ok
    assert uncached_result.localhost["msg"] == new_contents

    # All cached results will return the original contents
    for _ in range(4):
        result = host.debug(msg="{{ lookup('cached', 'file', '%s') }}" % path)

        assert len(result) == 1
        assert result.localhost.is_ok
        assert result.localhost["msg"] == original_contents


def test_invalid_lookup(host):
    expected_msg = "lookup plugin (veryfake) not found"

    uncached_result = host.debug(msg="{{ lookup('veryfake', 'arg1 arg2') }}")
    result = host.debug(msg="{{ lookup('cached', 'veryfake', 'arg1 arg2') }}")
    assert len(uncached_result) == len(result) == 1

    assert uncached_result.localhost == {"msg": expected_msg, "_ansible_no_log": False}
    assert result.localhost["msg"].endswith("original message: %s" % expected_msg)
