#! /usr/bin/env python3

import argparse
import getpass
import os
from image_prep.image_prep import ImagePrep


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(dest="image_file")
    parser.add_argument(dest="output_file")

    parser.add_argument(
        "--bypass-space-checks", action="store_true", default=False, dest="bypass_space_check",
        help="If you think you're smarter than the computer, bypass the disk space checks.",
    )

    parser.add_argument(
        "--pause", action="store_true", default=False, dest="inspection_pause",
        help="Pause for inspection before closing image",
    )

    local_group = parser.add_argument_group("Localization Options")

    parser.add_argument(
        "--locale", dest="locale", type=str,
        help="set the system locale, example: en_US.UTF-8",
    )

    parser.add_argument(
        "--timezone", dest="timezone", type=str,
        help="Set the timezone name, example: America/Chicago",
    )

    auth_group = parser.add_argument_group("Authentication Options")

    auth_group.add_argument(
        "--root-pw", action="store_true", dest="root_pw", default=False,
        help="Change root password",
    )

    auth_group.add_argument(
        "--root-keys", nargs="*", dest="root_keys", default=[],
        help="Authorized key files for the root user",
    )

    auth_group.add_argument(
        "--pi-pw", action="store_true", dest="pi_pw", default=False,
        help="Change the pi user password",
    )

    auth_group.add_argument(
        "--pi-keys", nargs="*", dest="pi_keys", default=[],
        help="Authorized key files for the pi user",
    )

    ssh_group = parser.add_argument_group("SSH Options")
    ssh_group.add_argument(
        "--enable-ssh", action="store_true", default=False, dest="enable_ssh",
        help="enable ssh on first boot",
    )

    nw_group = parser.add_argument_group("Network Options")
    nw_group.add_argument(
        "--hostname", type=str, default=False, dest="hostname",
        help="raspberry pi hostname",
    )

    wifi_group = parser.add_argument_group("WiFi Options")
    wifi_group.add_argument(
        "--wifi-ssid", type=str, default="", dest="wifi_ssid",
        help="wifi ssid",
    )
    wifi_group.add_argument(
        "--wifi-country", type=str, default="US",
        help="2 letter ISO 3166-1 country code for wifi.",
    )

    cfg_group = parser.add_argument_group("Configuration Options")
    cfg_group.add_argument(
        "--install-packages", dest="install_packages", nargs="*", default=[],
        help="packages to install on first boot",
    )

    args = parser.parse_args()

    root_pw = os.getenv("ROOT_PW")
    if not root_pw and args.root_pw:
        root_pw = getpass.getpass("Please enter the root password for the image:")

    pi_pw = os.getenv("PI_PW")
    if not pi_pw and args.pi_pw:
        pi_pw = getpass.getpass("Please enter the pi user password for the image:")

    wifi_pass = os.getenv("WIFI_PASS")
    if not wifi_pass and args.wifi_ssid:
        wifi_pass = getpass.getpass("Please enter wifi password:")


    ip = ImagePrep(args, root_pw, pi_pw, wifi_pass)
    ip.run()
