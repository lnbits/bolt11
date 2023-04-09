Lightning BOLT11 utils
======================

[![github-tests-badge]][github-tests]
[![github-mypy-badge]][github-mypy]
[![codecov-badge]][codecov]
[![pypi-badge]][pypi]
[![pypi-versions-badge]][pypi]
[![license-badge]](LICENSE)


This is an implementation of the Lightning BOLT11 specification,
based on previous work by [Rusty Russell][rusty], the [Electrum Wallet team][electrum],
and the LNbits bolt11 helpers created by [@fiatjaf][fiatjaf].


[github-tests]: https://github.com/lnbits/bolt11/actions?query=workflow%3A%22tests%22
[github-tests-badge]: https://github.com/lnbits/bolt11/workflows/tests/badge.svg
[github-mypy]: https://github.com/lnbits/bolt11/actions?query=workflow%3A%22mypy%22
[github-mypy-badge]: https://github.com/lnbits/bolt11/workflows/mypy/badge.svg
[codecov]: https://codecov.io/gh/lnbits/bolt11
[codecov-badge]: https://codecov.io/gh/lnbits/bolt11/branch/master/graph/badge.svg
[pypi]: https://pypi.org/project/bolt11/
[pypi-badge]: https://badge.fury.io/py/bolt11.svg
[pypi-versions-badge]: https://img.shields.io/pypi/pyversions/bolt11.svg
[license-badge]: https://img.shields.io/badge/license-MIT-blue.svg

[electrum]: https://github.com/spesmilo/electrum
[fiatjaf]: https://github.com/fiatjaf
[rusty]: https://github.com/rustyrussell/lightning-payencode


### resources
* [Bolt11 Spec](https://github.com/lightning/bolts/blob/master/11-payment-encoding.md )
* [bolt11.org](https://www.bolt11.org/)
* [lightningdecoder](https://lightningdecoder.com/)


### installing
```console
git clone https://github.com/lnbits/bolt11
cd bolt11
poetry install
```

### running CLI
```console
poetry run bolt11 --help
poetry run bolt11 decode
poetry run bolt11 encode
```

### run all checks and tests
```console
make
```

### using pre-commit as git hook
```console
poetry run pre-commit install
```
