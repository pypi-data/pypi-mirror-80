#! /usr/bin/env python3

import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

from string import Template
from textwrap import dedent
from pathlib import Path

def hostname_check(try_hostname):
    """ returns boolean value """

    # try the instant disqualifier
    if not isinstance(try_hostname, str):
        return False

    if try_hostname.endswith('.'):
        try_hostname = try_hostname[:-1]

    # make sure none of the items in the hosts file are mentioned
    illegal_hostnames = set([
        "127.0.0.1",
        "127.0.1.1",
        "localhost",
        "ip6-localhost",
        "ip6-loopback",
        "ip6-allnodes",
        "ip6-allrouters",
        "ff02::1",
        "ff02::2",
    ])
    if try_hostname in illegal_hostnames:
        return False

    
    if len(try_hostname) < 1 or len(try_hostname) > 253:
        return False

    pattern = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$", re.IGNORECASE)

    return all(pattern.match(x) for x in try_hostname.split('.'))


class DiskPartition:

    def mount(self, mount_in_dir):

        self.mount_point = os.path.join(mount_in_dir, self.mount_name)
        os.mkdir(self.mount_point)
        subprocess.check_call([
            self.mount_exe, "-v", "-o",
            "offset={o},sizelimit={s}".format(o=self.offset, s=self.sizelimit),
            "-t", self.disk_type, self.device, self.mount_point,
        ])

    def dismount(self):
        if not self.mount_point:
            return None

        subprocess.check_call([self.umount_exe, self.mount_point])
        self.mount_point = False



    def __init__(self,
        device: str, disk_size: int, disk_start: int, disk_type: str,
        block_size=512,
    ):
        self.device = device
        self.offset = block_size * disk_start
        self.disk_type = {"c": "vfat", "83": "ext4"}.get(disk_type)
        self.mount_name = {"c": "piboot", "83": "piroot"}.get(disk_type)
        self.sizelimit = block_size * disk_size
        self.mount_exe = shutil.which("mount")
        self.umount_exe = shutil.which("umount")
        self.mount_point = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dismount()

class ImagePrep:

    def __init__(self, args, root_pw, pi_pw, wifi_pass):

        logging.basicConfig(level=logging.INFO)
        self.args = args

        self.pi_pw = pi_pw
        self.root_pw = root_pw

        self.hostname = False
        if args.hostname:
            if hostname_check(args.hostname):
                self.hostname = args.hostname
            else:
                logging.error("Hostname {} is invalid, skipping".format(args.hostname))


        # check for executable names
        for i in ["sfdisk", "mount", "umount"]:
            if not shutil.which(i):
                logging.fatal("Count not locate {} executable".format(i))

        # get the wifi supplicant info
        if args.wifi_ssid:
            self.wifi_supplicant = dedent("""
                ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
                update_config=1
                country={country}

                network={{
                    ssid="{ssid}"
                    psk="{psk}"
                }}
            """).strip().format(
                country=args.wifi_country,
                ssid=args.wifi_ssid,
                psk=wifi_pass,
            )
        else:
            self.wifi_supplicant = False

        self.wd = tempfile.TemporaryDirectory(dir=os.getcwd())
        logging.debug("Using temporary directory {}".format(os.path.abspath(self.wd.name)))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ unmount volumes and clean up temp dir """
        if self.piroot and self.piroot.mount_point:
            self.piroot.dismount()
        if self.piboot and self.piboot.mount_point:
            self.piboot.dismount()
        self.wd.cleanup()


    @staticmethod
    def get_mount_avail(mountp):
        """ returns a mount size in megabytes """
        statvfs = os.statvfs(mountp)
        f_size = float(statvfs.f_frsize * statvfs.f_bavail) / float(1048576)
        return round(f_size, 2)

    def check_avail_space(self, image_size, output_dir):

        fail = False
        wd_mount_size = self.get_mount_avail(self.wd.name)
        logging.info("Working directory space: {} MB".format(wd_mount_size))
        dest_mount_size = self.get_mount_avail(output_dir)
        logging.info("Destination directory space: {} MB".format(dest_mount_size))

        img_sz_mb = round((float(image_size) / float(1048576)), 2)
        logging.info("Image Size: {} MB".format(img_sz_mb))


        if (img_sz_mb * 2) > wd_mount_size:
            logging.warning("The image has a size of {} MB. There may not be enough room in the working directory {}.".format(
                img_sz_mb,
                os.path.abspath(self.wd.name),
            ))
            fail = True

        if (img_sz_mb * 2) > dest_mount_size:
            logging.warning("The image has a size of {} MB. There may not be enough room in the destination directory {}.".format(
                img_sz_mb,
                os.path.abspath(output_dir),
            ))
            fail = True

        if fail and not self.args.bypass_space_check:
            logging.fatal("The space checks failed. See previous errors. Either clear those up or use the '--bypass-space-checks' argument.")
            sys.exit(1)


    def run(self):
        """ extract the image if necessary, then call methods to modify """

        original_image = self.args.image_file
        output_file = self.args.output_file

        if not os.path.isfile(original_image):
            logging.fatal("File not found.")
            sys.exit(1)


        if os.path.splitext(original_image)[1].lower() == ".zip":
            # unzip here
            logging.debug("This is a zip file.")
            z = zipfile.ZipFile(original_image)
            img_files = [x for x in z.namelist() if (os.path.splitext(x)[1].lower() == ".img")]
            
            if not img_files:
                logging.fatal("No .img files found in the archive.")
                sys.exit(1)

            elif len(img_files) > 1:
                logging.fatal("More than 1 .img files found in the zip. Not sure how to handle this yet.")
                sys.exit(1)

            # run a file check
            self.check_avail_space(
                z.getinfo(img_files[0]).file_size,
                os.path.dirname(os.path.abspath(output_file)),
            )

            logging.info("Extracting image file: {}".format(img_files[0]))
            z.extract(img_files[0], path=self.wd.name)
            wip_image = os.path.join(self.wd.name, img_files[0])
            assert os.path.isfile(wip_image)
            del img_files
            z.close()

        elif os.path.splitext(original_image)[1].lower() != ".img":
            logging.fatal("Unknown file type. Needs to be either a .zip or .img")
            sys.exit(1)

        else:
            self.check_avail_space(
                os.path.getsize(original_image),
                os.path.dirname(output_file),
            )
            logging.info("Copying image to temporary location")
            wip_image = os.path.join(self.wd.name, original_image.split[1])
            shutil.copyfile(original_image, wip_image)

        logging.debug("Gathering info from image")

        # get json, and parse it
        sfdisk_out = subprocess.check_output([shutil.which("sfdisk"), "-l", "--json", wip_image])
        disk_info = json.loads(sfdisk_out.decode("utf-8")).get('partitiontable')

        # get DiskPartition Objects
        disks = map(
            lambda x: DiskPartition(disk_info.get('device'), x.get('size'), x.get('start'), x.get('type')),
            disk_info.get('partitions'),
        )
        disks = {x.mount_name:x for x in disks}

        self.piroot = disks.get('piroot')
        self.piboot = disks.get('piboot')

        if self.args.enable_ssh or self.wifi_supplicant:
            self.modify_piboot()
        else:
            logging.debug("No need to mount the boot partition")

        if any([
            self.hostname, self.args.root_keys, self.root_pw, self.args.pi_keys, self.pi_pw,
            self.args.install_packages or self.args.timezone or self.args.locale,
        ]):
            self.modify_piroot()
        else:
            logging.debug("No need to mount the root partition")

        # put the image in it's final destination
        # wip_image, output_file
        if os.path.splitext(output_file)[1].lower() == ".zip":
            logging.info("specified a zip image format, compressing image to {}".format(output_file))
            with zipfile.ZipFile(output_file, compression=zipfile.ZIP_DEFLATED, mode="w") as z:
                z.write(wip_image)
            os.remove(wip_image)

        else:
            logging.info("Moving completed image to {}".format(output_file))
            shutil.move(wip_image, output_file)

    def modify_piboot(self):

        logging.info("Mounting the boot partition")
        self.piboot.mount(self.wd.name)

        # enable ssh
        try:
            ssh_file = os.path.join(self.piboot.mount_point, "ssh")
            if self.args.enable_ssh and not os.path.isfile(ssh_file):
                logging.info("Enabling SSH")
                Path(ssh_file).touch()
                if os.path.isfile(ssh_file):
                    logging.debug("Successfully enabled ssh")
                else:
                    logging.error("Failed to enable ssh")
            elif self.args.enable_ssh and os.path.isfile(ssh_file):
                logging.info("SSH was already enabled")
        except Exception as e:
            logging.error("Failed to enable ssh: {}".format(e))

        # enable wifi
        try:
            wifi_file = os.path.join(self.piboot.mount_point, "wpa_supplicant.conf")
            if self.wifi_supplicant:
                logging.info("Enabling WiFi")
                with open(wifi_file, "w") as wifi_fd:
                    wifi_fd.write(self.wifi_supplicant)
        except Exception as e:
            logging.error("Failed to enable wifi: {}".format(e))

        if self.args.inspection_pause:
            input("Press Enter to continue...")
        self.piboot.dismount()

    @staticmethod
    def add_auth_keys(auth_key_file: str, authorized_keys: list, uid: int):
        """ make a directory and copy files """

        logging.info("Adding {} keys to {}".format(len(authorized_keys), auth_key_file))

        # make the directory, set permissions
        os.makedirs(os.path.dirname(os.path.abspath(auth_key_file)), exist_ok=True)
        os.chmod(os.path.dirname(os.path.abspath(auth_key_file)), 0o700)
        shutil.chown(os.path.dirname(os.path.abspath(auth_key_file)), user=uid, group=uid)

        # read keys
        def simple_read_file(file_path):
            with open(file_path, "r") as f:
                contents = f.read()
            return contents
        authorized_keys = os.linesep.join([simple_read_file(x) for x in authorized_keys])


        # write the file, set permissions
        with open(auth_key_file, "w") as f:
            f.write(authorized_keys)
        shutil.chown(auth_key_file, user=uid, group=uid)
        os.chmod(auth_key_file, 0o600)

    def set_user_password(self, username: str, password: str):
        """ set a username and password on first boot """

        logging.info("setting password for the {} user".format(username))

        if username not in ["root", "pi"]:
            # little safety check
            return False

        script_name = "set_{}_password.sh".format(username)

        pw_script = Template(dedent("""
            #! /bin/bash

            set -e

            # change a password
            echo "$username:$password" | /usr/sbin/chpasswd

            # delete my cron and myself
            rm -rf {cron_loc}
            rm -rf {script_loc}
        """).lstrip()).safe_substitute(
            username=username,
            password=password,
        )

        self.temp_cron_script(pw_script, script_name)

    def write_install_package_script(self):
        """ write a script to install packages on reboot """

        logging.info("Setting up package installs for: {}".format(", ".join(self.args.install_packages)))

        pkg_install_list = " ".join(self.args.install_packages)
        install_script = Template(dedent("""
            #! /bin/bash

            set -e
            apt-get update
            apt-get install -y $pkg_list

            rm -rf {cron_loc}
            rm -rf {script_loc}
        """).lstrip()).safe_substitute(pkg_list=pkg_install_list)

        self.temp_cron_script(install_script, "initial_package_installer.sh")

    def set_locale(self):
        """ set the locale """

        avail_locale_file = os.path.join(self.piroot.mount_point, "etc", "locale.gen")

        with open(avail_locale_file, "r") as f:
            avail_locales = map(
                lambda x: x.split()[0],
                filter(
                    lambda x: len(x) >= 2,
                    map(
                        lambda x: x.strip(os.linesep).strip("# "),
                        f.readlines(),
                    ),
                ),
            )
            avail_locales = [x for x in avail_locales if x]
            f.seek(0)
            avail_locales_text = f.read()

        if not self.args.locale in avail_locales:
            logging.error("Invalid Locale, it will not be changed: {}".format(self.args.locale))
            return None

        with open(avail_locale_file, "w") as f:
            f.write(avail_locales_text.replace(
                "# {}".format(self.args.locale),
                self.args.locale,
            ))

        locale_script = Template(dedent("""
            #! /bin/bash

            set -e

            /usr/sbin/locale-gen

            localectl set-locale LANG=$locale

            rm -rf {cron_loc}
            rm -rf {script_loc}
        """).lstrip()).safe_substitute(locale=self.args.locale)

        self.temp_cron_script(locale_script, "set_locale.sh")

    def set_timezone(self):
        """ queue up setting timezone """

        logging.info("Setting up timezone change to {}.".format(self.args.timezone))

        tz_script = Template(dedent("""
            #! /bin/bash

            set -e
            timedatectl set-timezone '$tz'

            touch /var/run/reboot-required

            rm -rf {cron_loc}
            rm -rf {script_loc}
        """).lstrip()).safe_substitute(tz=self.args.timezone)

        self.temp_cron_script(tz_script, "timezone_setter.sh")

    def temp_cron_script(
        self, script_contents: str, script_name: str,
        script_dir="/usr/local/bin", run_user="root", cron_schedule="* * * * *",
        script_uid=0, script_gid=0, script_mode=0o700,
    ):
        """
        shortcut code to write a script and add a cron entry for it.

        the script contents will be formatted with the following entries to assist in self-cleanup:
        script_loc: the script location as found on the pi
        cron_loc: the cron location as found on the pi
        """

        # data checks.  I'll write something more elegant later.
        assert script_dir[0] == "/"
        assert script_name == os.path.split(script_name)[1]

        # get the script name without an extension
        script_basename = os.path.splitext(script_name)[0]

        # where the script is found in the temp mount
        script_img_loc = os.path.join(
            self.piroot.mount_point,
            script_dir.lstrip("/"),
            script_name,
        )
        # where the script is found on the pi
        script_pi_loc = os.path.join(script_dir, script_name)

        # where the cron entry is written on the temp mount
        cron_img_loc = os.path.join(
            self.piroot.mount_point,
            "etc", "cron.d",
            script_basename,
        )
        # where the cron entry is found on the pi
        cron_pi_loc = os.path.join("/etc", "cron.d", script_basename)

        # format the cron entry
        # this needs to end in a newline, otherwise, cron will ignore it.
        cron_entry = "{sched} {usr} /usr/bin/flock -n /tmp/{base}.lock {script}{ls}".format(
            sched=cron_schedule,
            usr=run_user,
            base=script_basename.strip(),
            script=script_pi_loc,
            ls=os.linesep,
        )

        # add the script and cron locations to the script, write it, secure it.
        with open(script_img_loc, "w") as f:
            f.write(script_contents.format(
                script_loc=script_pi_loc,
                cron_loc=cron_pi_loc,
            ))
        shutil.chown(script_img_loc, user=script_uid, group=script_gid)
        os.chmod(script_img_loc, script_mode)

        # write and secure the cron entry
        with open(cron_img_loc, "w") as f:
            f.write(cron_entry)
        shutil.chown(cron_img_loc, user=0, group=0)
        os.chmod(cron_img_loc, 0o644)

    def modify_piroot(self):

        # options requiring the root vol to be booted.
        logging.info("Mounting the root partition")
        self.piroot.mount(self.wd.name)

        if self.hostname:

            try:
                hostname_file = os.path.join(self.piroot.mount_point, "etc", "hostname")
                hosts_file = os.path.join(self.piroot.mount_point, "etc", "hosts")

                with open(hostname_file, "r") as f:
                    current_hostname = f.read().strip()

                if current_hostname == self.hostname:
                    logging.info("Current hostname already matches specified hostname: {}".format(self.hostname))
                else:
                    logging.info("Updating hostname from {} to {}".format(current_hostname, self.hostname))

                    with open(hostname_file, "w") as f:
                        f.write(self.hostname)

                    with open(hosts_file, "r") as f:
                        current_hosts = f.read()
                    with open(hosts_file, "w") as f:
                        f.write(current_hosts.replace(current_hostname, self.hostname))

            except Exception as e:
                logging.error("Failed to set hostname: {}".format(e))



        if self.pi_pw:
            try:
                self.set_user_password("pi", self.pi_pw)
            except Exception as e:
                logging.error("Failed to set pi user password: {}".format(e))

        if self.root_pw:
            try:
                self.set_user_password("root", self.root_pw)
            except Exception as e:
                logging.error("Failed to set root user password: {}".format(e))


        # add pi user authorized keys 
        pi_keys = [x for x in self.args.pi_keys if os.path.isfile(x)]
        if pi_keys:
            try:
                auth_key_file = os.path.join(
                    self.piroot.mount_point,
                    "home", "pi", ".ssh", "authorized_keys",
                )
                self.add_auth_keys(auth_key_file, pi_keys, 1000)
            except Exception as e:
                logging.error("Failed to add auth keys for pi user")

        # add root user authorizied keys
        root_keys = [x for x in self.args.root_keys if os.path.isfile(x)]
        if root_keys:
            try:
                auth_key_file = os.path.join(
                    self.piroot.mount_point,
                    "root", ".ssh", "authorized_keys",
                )
                self.add_auth_keys(auth_key_file, root_keys, 0)
            except Exception as e:
                logging.error("Failed to add auth keys for root user")

        if self.args.install_packages:
            self.write_install_package_script()

        if self.args.timezone:
            self.set_timezone()

        if self.args.locale:
            self.set_locale()

        if self.args.inspection_pause:
            input("Press Enter to continue...")
        self.piroot.dismount()