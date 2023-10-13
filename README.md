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
$ git clone https://github.com/lnbits/bolt11
$ cd bolt11
$ poetry install
```

### running CLI
```console
$ poetry run bolt11 --help
$ poetry run bolt11 decode
```

### run all checks and tests
```console
$ make
```

### using pre-commit as git hook
```console
$ poetry run pre-commit install
```


### running CLI
```console
$ poetry run bolt11 --help
```

### running CLI decode
```
$ poetry run bolt11 decode lnbc20m1pvjluez.....
{
  "currency": "bc",
  "amount": 2000000000,
  "timestamp": 1496314658,
  "signature": "6a6586db4e8f6d40e3a5bb92e4df5110c627e9ce493af237e20a046b4e86ea200178c59564ecf892f33a9558bf041b6ad2cb8292d7a6c351fbb7f2ae2d16b54e",
  "description_hash": "3925b6f67e2c340036ed12093dd44e0368df1b6ea26c53dbe4811f58fd5db8c1",
  "features": {
    "var_onion_optin": "required",
    "payment_secret": "required"
  },
  "fallback": "1RustyRX2oai4EYYDpQGWvEL62BBGqN9T",
  "route_hints": [
    {
      "public_key": "029e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255",
      "short_channel_id": "66051x263430x1800",
      "base_fee": 1,
      "ppm_fee": 20,
      "cltv_expiry_delta": 3
    },
    {
      "public_key": "039e03a901b85534ff1e92c43c74431f7ce72046060fcf7a95c37e148f78c77255",
      "short_channel_id": "197637x395016x2314",
      "base_fee": 2,
      "ppm_fee": 30,
      "cltv_expiry_delta": 4
    }
  ],
  "min_final_cltv_expiry": 9,
  "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
  "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
  "payee": "03e7156ae33b0a208d0744199163177e909e80176e55d97a2f221ede0f934dd9ad"
}
```

### running CLI encode
```
$ poetry run bolt11 encode '{
  "currency": "bc",
  "amount_msat": 1000,
  "date": 1590000000,
  "payment_hash": "0001020304050607080900010203040506070809000102030405060708090102",
  "payment_secret": "1111111111111111111111111111111111111111111111111111111111111111",
  "description": "description"
}' e126f68f7eafcc8b74f54d269fe206be715000f94dac067d1c04a8ca3b2db734
