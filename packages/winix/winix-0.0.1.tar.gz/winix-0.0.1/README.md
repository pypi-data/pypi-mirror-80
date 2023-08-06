# Winix Controller

This is a Python library for controlling Winix C545 Air Purifier
devices. I reverse-engineered the API calls from the Android app. There
are a few weird idiosyncrasies with the Winix backends.

Included in this package is a CLI program `winixctl`.

## Setup


## `winixctl` CLI

```
~/dev/winix(master*) » winixctl                                                                                                                                                                                                 hfern@arrakis
usage: winixctl [-h] {login,refresh,devices,fan,power} ...

Winix C545 Air Purifier Control

positional arguments:
  {login,refresh,devices,fan,power}
    login               Authenticate Winix account
    refresh             Refresh account device metadata
    devices             List registered Winix devices
    fan                 Fan speed controls
    power               Power controls

optional arguments:
  -h, --help            show this help message and exit
```