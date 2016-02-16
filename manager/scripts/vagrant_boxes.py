from django.conf import settings

import os
import subprocess
import collections
import tempfile

'''
Module to get information (output) of Vagrant,
and haveit in a usable structure (yaml¿?) for later use
i.e for django views/templates

_box_list.- 'vagrant box list --machine-readable' output
_global_status.- 'vagrant global-status
_add_box.- 'vagrant box add ...'
_deps_versions.- checks vbox and vagrant versions'
_init_env.-'vagrant init -m -f TEST_ENV'
'''

def run(*args):
    '''
    run attribute for runscript (python-extensions)
    '''
    if 'box_list' in args:
        _box_list()
    if 'global_status' in args:
        _global_status()

def _vagrant_command(args):
    '''
    Return stdout of a vagrant command,
    agrs are in list format:
    i.e ['box', 'list', '--machine-readable']
    '''
    command = _args_to_str(args)
    vagrant_cmd = subprocess.check_output(command, shell=True, universal_newlines=True)
    return vagrant_cmd

def _vagrant_call_command(cmd, *args):
    '''
    Return None on a sucessfull vagrant command,
    cmd is in list format.
    '''
    command = _args_to_str(cmd)
    vagrant_cmd = subprocess.check_call(command, shell=True, universal_newlines=True)
    return vagrant_cmd

def _args_to_str(args):
    '''
    get args list i.e ['box', 'list', '--machine-readable']
    and return as a string
    '''
    command = str.join(' ', args)
    return 'vagrant ' + command

def _box_list():
    cmd = ['box', 'list', '--machine-readable']
    output = _vagrant_command(cmd)
    parsed_lines = [line.split(',', 4) for line in output.splitlines() if line.strip()]
    parsed_lines = list(filter(lambda x: x[2] !='ui' and x[2] !='metadata', parsed_lines))

    boxes = []
    Box = collections.namedtuple('Box', ['name', 'provider', 'version'])

    name = provider = version = None
    for timestamp, extra, field, data in parsed_lines:
        if field == 'box-name':
            if name is not None:
                boxes.append(Box(name=name, provider=provider, version=version))
            name = data
            provider = version = None
        elif field == 'box-provider':
            provider = data
        elif field == 'box-version':
            version = data
    if name is not None:
        boxes.append(Box(name=name, provider=provider, version=version))

    return boxes

def _global_status():
    cmd = ['global-status', '--machine-readable']
    output = _vagrant_command(cmd)
    parsed_lines = [line.split(',', 4) for line in output.splitlines() if line.strip()]
    del parsed_lines[-2:]
    del parsed_lines[:7]
    parsed_lines = list(filter(lambda x: x[4] !='', parsed_lines))

    vagrant_status = []
    Vagrant_Status = collections.namedtuple('Environment', ['uid', 'name', 'provider', 'state', 'path'])

    # get data field into a new list and then splitit evenly 
    # for have the status of each machine in each line list.
    # i.e input:
    #           parsed_lines = ['9a44804  ', 'master   ', 'virtualbox ', 'poweroff ', '/home/speedlight/Vagrant/vagrant-salt  ', 'd4e6800  ', 'minion01 ', 'virtualbox ', 'poweroff ', '/home/speedlight/Vagrant/vagrant-salt  ']
    # output:
    #           new_parsed_lines = [['9a44804  ', 'master   ', 'virtualbox ', 'poweroff ', '/home/speedlight/Vagrant/vagrant-salt  '], ['d4e6800  ', 'minion01 ', 'virtualbox ', 'poweroff ', '/home/speedlight/Vagrant/vagrant-salt  ']]

    temp_lst = []
    uid = name = provider = state = path = None
    for timestamp, extra, ui, info, data in parsed_lines:
        if data is not None:
            temp_lst.append(data)
    parsed_lines = [temp_lst[x:x+5] for x in range(0, len(temp_lst), 5)]
    
    for line in parsed_lines:
        vagrant_status.append(Vagrant_Status(*line))

    return vagrant_status

def _add_box(opts, provider=False, force=False):
    """
    Add a box in vagrant.
    opts argument is in format: ['box-name', 'user/box-name']
    method call is i.e like: _add_box(args, 'virtuabox', force')
    """
    cmd = ['box', 'add']
    if provider is not False:
        cmd.append('--provider ' + str(provider))
    if not force:
        cmd.append('--force')
    
    if len(opts) == 2:
        cmd.append('--name ' + str(opts[0]))
        cmd.append(opts[1])
    else:
        cmd.append(opts[0])

    return _vagrant_call_command(cmd)

def _remove_box(opts, provider=False, force=False):
    """
    Remove a box from vagrant.
    opts argument is in format: 'box-name'
    method call is i.e like: _remove_box(args, 'virtuabox', force')
    """
    cmd = ['box', 'remove']
    if provider is not False:
        cmd.append('--provider ' + str(provider))
    if not force:
        cmd.append('--force')
    
    cmd.append(opts)

    return _vagrant_call_command(cmd)

def _init_env(boxname, path, *args):
    """
    Run vagrant init with minimal -m and force -f opts
    the boxname arg is for set the 'config.vm.box=boxname' option
    see: http://www.vagrantup.com/docs
    """
    cmd = ['init', '-mf']
    cmd.append(str(boxname))
    if path:
        print("-" * 20 + " VAGRANT INIT " + "-" * 20)
        os.chdir(path)
        # cmd.append('--output ' + str(path) + '/Vagrantfile')
        return _vagrant_call_command(cmd)

def _box_up(path, *args):
    """
    Run vagrant up
    """
    cmd = ['up']
    if not os.path.isdir(path):
        print("Path does not exist, please give a valid directory path")
    else:
        if os.path.isfile(os.path.join(path, 'Vagrantfile')):
            print("-" * 20 + " VAGRANT UP " + "-" * 20)
            return _vagrant_call_command(cmd)

def _box_destroy(path, *args):
    """
    Run vagrant destroy
    """
    cmd = ['destroy', '-f']
    if not os.path.isdir(path):
        print("Path does not exist, please give a valid directory path")
    else:
        print("-" * 20 + " VAGRANT DESTROY " + "-" * 20)
        return _vagrant_call_command(cmd)


def _deps_versions():
    deps_vers = {}
    vagrant_ver = subprocess.check_output('vagrant --version', shell=True, universal_newlines=True)
    vagrant_ver = vagrant_ver.strip('\n')
    vagrant_ver = vagrant_ver.split(' ')

    virtualbox_ver = subprocess.check_output("virtualbox --help |head -n1 |cut -d ' ' -f 5 |cut -d '_' -f 1", shell=True, universal_newlines=True)
    virtualbox_ver = virtualbox_ver.strip('\n')

    deps_vers["vagrant_version"] = vagrant_ver[1]
    deps_vers["virtualbox_version"] = virtualbox_ver

    return deps_vers
