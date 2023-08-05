Multi backend for Taxi
======================

This is a special "multi" backend for [Taxi](https://github.com/sephii/taxi).
It allows pushing your entries to multiple backends at once.

Installation
------------

```shell
taxi plugin install multi
```

Usage
-----

Run `taxi config` and use the `multi` protocol for your backend. The backends
parameter is a comma-separated list of the backends you want to push to.

```ini
[backends]
multi_backend = multi://?backends=my_tempo_backend,my_tipee_backend
```

Then define the backends a separate section:

```ini
[multi]
my_tempo_backend = tempo://...
my_tipee_backend = tipee://...
```
