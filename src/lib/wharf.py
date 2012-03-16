#!/usr/bin/python

import os
import sys
import redis
import cfengine
import subprocess
import ConfigParser

class WharfConfig(object):
    config_file = '/etc/wharf/wharf.config'

    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp('/etc/wharf/wharf.config')
        self.__setup__()

    def get(self, *args, **kwargs)
        return self.config.get(*args, **kwargs)

class Templates(object):
    def __init__(self, distro):
        self.distro, self.function = distro, None

    def deploy(self):
        import self.distro as distro
        linux = distro.Configure()
        linux.make_init()
        linux.make_network()
        linux.make_hostname()
        linux.make_hosts()
        linux.make_devices()
        linux.os_download()
        linux.os_copy()

    def remove(self):
        import self.distro as distro
        linux = distro.Configure()
        linux.remove()

class Provisioning(object):
    def __init__(self):
        self.config = WharfConfig()

    def bootstrap(self, **kwargs):
        base_storage = self.config.get('Provisioning', 'base_storage')
        template = Template(kwargs[disto])
        template.deploy(kwargs[disto], kwargs[name])
        lxc_config = ManageConfig()
        lxc_config.add('lxc.network.type', 'veth')
        lxc_config.add('lxc.network.flags', 'up')
        lxc_config.add('lxc.network.hwaddr', kwargs[hwaddr])
        lxc_config.add('lxc.network.mtu', '1500')
        lxc_config.add('lxc.network.name', 'eth0')
        lxc_config.add('lxc.network.ipv4', kwargs[ipv4])
        action = cfengine.Action()
        action.packages('add', ['iproute2', 'bind-utils'])
        action.files('server_copy', {'/etc/resolv.conf', {'from': '$(masterfiles)/etc/resolv.conf'}})
        bundle = cfengine.Bundle('config_%s' % name)
        bundle.agent.add(bundle)
        promise = cfengine.Promise('config_%s' % name)
        promise.add(bundle)
        promise.write()

    def quota(self, **kwargs):
        pass

    def device(self):
        pass

class ManageConfig(object):
    def __init__(self):
        self.config = WharfConfig()

    def add(self, namespace, value):
        pass

    def get(self, namespace, value):
        pass

    def list(self):
        pass

    def keys(self, namespace=None):
        pass

    def load(self, file):
        pass

    def save(self, file):
        pass

    def write(self, file=None):
        pass

