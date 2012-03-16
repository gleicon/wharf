import os
import shutil
import subprocess
from wharf import WharfConfig

template = "debian-squeeze"

class Configure(object):
    def __init__(self, rootfs, hostname, selinux=False, arch="amd64"):
        self.arch = arch
        self.rootfs = rootfs
        self.selinux = selinux
        self.hostname = hostname
        self.config = WharfConfig()
        self.cache = self.config.get('Provisioning', 'cache')

        if not os.path.isdir("%s/selinux" % self.rootfs):
            os.makedirs("%s/selinux" % self.rootfs)

        with open("%s/selinux/enforce" % self.rootfs, 'w') as file:
            file.write(int(selinux))

    def make_init(self):
        with open("%s/etc/inittab" % self.rootfs, 'w') as inittab:
            inittab.write("id:3:initdefault:")
            inittab.write("si::sysinit:/etc/init.d/rcS")
            inittab.write("l0:0:wait:/etc/init.d/rc 0")
            inittab.write("l1:1:wait:/etc/init.d/rc 1")
            inittab.write("l2:2:wait:/etc/init.d/rc 2")
            inittab.write("l3:3:wait:/etc/init.d/rc 3")
            inittab.write("l4:4:wait:/etc/init.d/rc 4")
            inittab.write("l5:5:wait:/etc/init.d/rc 5")
            inittab.write("l6:6:wait:/etc/init.d/rc 6")
            inittab.write("z6:6:respawn:/sbin/sulogin")
            inittab.write("1:2345:respawn:/sbin/getty 38400 console")
            inittab.write("c1:12345:respawn:/sbin/getty 38400 tty1 linux")
            inittab.write("c2:12345:respawn:/sbin/getty 38400 tty2 linux")
            inittab.write("c3:12345:respawn:/sbin/getty 38400 tty3 linux")
            inittab.write("c4:12345:respawn:/sbin/getty 38400 tty4 linux")

    def make_network(self):
        with open("%s/etc/network/interfaces" % self.rootfs, 'w') as interfaces:
            interfaces.write("auto lo")
            interfaces.write("iface lo inet loopback")
            interfaces.write("")
            interfaces.write("auto eth0")
            interfaces.write("iface eth0 inet dhcp")

    def make_hostname(self):
        with open("%s/etc/hostname" % self.rootfs, 'w') as hostname:
            hostname.write(self.hostname)

    def make_hosts(self):
        with open("%s/etc/hosts" % self.rootfs, 'w') as hosts:
            hosts.write("127.0.0.1 localhost %s" % self.hostname)

    def make_devices(self):
        for minor in range(1, 5):
            dev = os.makedev(4, minor)
            mode = stat.S_IFCHR | 0666
            os.mknod("%s/dev/tty%s" % (self.rootfs, minor), mode, dev))

    def os_download(self):
        packages = ["ifupdown", "locales", "libui-dialog-perl", "dialog",
                    "isc-dhcp-client", "netbase", "net-tools", "iproute",
                    "openssh-server"]
        dlp = "%s/%s/partial-%s" % (self.cache, template, self.arch)
        dlc = "%s/%s/rootfs-%s" % (self.cache, template, self.arch)
        if not os.path.isdir(dlp):
            os.makedirs(dlp)
        subprocess.check_call(["/usr/sbin/debootstrap",
                               "--verbose", "--variant=minbase",
                               "--arch=%s" % self.arch,
                               "--include=%s]" % " "join.(packages)
                               "squeeze",
                               dlp, "http://ftp.debian.org/debian"])
        if os.path.isdir(dlc):
            shutil.rmtree(dlc)
        shutil.move(dlp, dlc)

    def os_copy(self):
        dlc = "%s/%s/rootfs-%s" % (self.cache, template, self.arch)
        if not os.path.isdir(self.rootfs):
            os.makedirs(self.rootfs)
        shutil.copy(dlc, self.rootfs)

    def os.remove(self):
        if .path.isdir(self.rootfs):
            os.rmtree(self.rootfs)
