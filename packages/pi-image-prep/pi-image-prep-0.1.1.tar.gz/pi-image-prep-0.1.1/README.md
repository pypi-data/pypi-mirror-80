# pi-image-prep

[![PyPI version](https://badge.fury.io/py/pi-image-prep.svg)](https://badge.fury.io/py/pi-image-prep)

```bash
pip install pi-image-prep
```

## Overview

This is a script I created to help prepare Rasbian image before the first boot. My goal was to set up an image with some basic features, up to the point where I could pass off control to my configuration management system.

I was inspired to replicate the functionality of [PiBakery](https://www.pibakery.org/), but I wanted something simple and lightweight that would run on Linux.

## Features:

- set system Locale
- set system timezone
- set user passwords for root and pi users
- add authorized keys for the root and pi users
- enable ssh
- set hostname
- enable wifi
- install packages by name


## Usage:

**On most systems, this will need to be run as root, or with sudo.** This is because the image partitions need to be mounted and unmounted, and most non-root users cannot do this by default.

The full usage is below. Nothing is enabled by default, unless specified in a cli flag.

The following options will enable a prompt in the script, but the values can be set via environment variables to prevent this.

- `--pi-pw`: can be overridden by setting the environment variable `PI_PW`
- `--root-pw`: can be overridden by setting the environment variable `ROOT_PW`
- `--wifi-ssid`: This will cause a prompt for the wifi password, which can be overridden by specifing an environment variable `WIFI_PASS`.

Note: I chose not to make those options available via cli flags to discourage passing sensitive information to the command line.

```
$ pi-image-prep.py -h
usage: pi-image-prep.py [-h] [--bypass-space-checks] [--pause]
                        [--locale LOCALE] [--timezone TIMEZONE] [--root-pw]
                        [--root-keys [ROOT_KEYS [ROOT_KEYS ...]]] [--pi-pw]
                        [--pi-keys [PI_KEYS [PI_KEYS ...]]] [--enable-ssh]
                        [--hostname HOSTNAME] [--wifi-ssid WIFI_SSID]
                        [--wifi-country WIFI_COUNTRY]
                        [--install-packages [INSTALL_PACKAGES [INSTALL_PACKAGES ...]]]
                        image_file output_file

positional arguments:
  image_file
  output_file

optional arguments:
  -h, --help            show this help message and exit
  --bypass-space-checks
                        If you think you're smarter than the computer, bypass
                        the disk space checks.
  --pause               Pause for inspection before closing image
  --locale LOCALE       set the system locale, example: en_US.UTF-8
  --timezone TIMEZONE   Set the timezone name, example: America/Chicago

Authentication Options:
  --root-pw             Change root password
  --root-keys [ROOT_KEYS [ROOT_KEYS ...]]
                        Authorized key files for the root user
  --pi-pw               Change the pi user password
  --pi-keys [PI_KEYS [PI_KEYS ...]]
                        Authorized key files for the pi user

SSH Options:
  --enable-ssh          enable ssh on first boot

Network Options:
  --hostname HOSTNAME   raspberry pi hostname

WiFi Options:
  --wifi-ssid WIFI_SSID
                        wifi ssid
  --wifi-country WIFI_COUNTRY
                        2 letter ISO 3166-1 country code for wifi.

Configuration Options:
  --install-packages [INSTALL_PACKAGES [INSTALL_PACKAGES ...]]
                        packages to install on first boot
```

## A Note on Sudo and Virtual Environments

If installed into a virtual environment, a `sudo pi-image-prep.py` call will mostly likely fail, since the root user would not have sourced the activate file. The easiest way to bypass this is to either install into the system python install or call the executable by full path.

## Wishlist

These are features I think would be great additions to the script. I may or may not have time to add them, so contributions are always welcome:

- SSH Host key management: either copy pre-existing keys or generate new then display an authorized_keys compabile entry to stdout.
- Windows Compatibility: I won't use it, but I'd entertain cross compatbility features
- Remove password for pi user
- Use sudo with the mount/umount commands
