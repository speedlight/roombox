import subprocess
import collections

'''
Module to get information (output) of Vagrant,
and haveit in a usable structure (yaml¿?) for later use
i.e for django views/templates

_box_list.- 'vagrant box list --machine-readable' output
_global_status.- 'vagrant global-status
'''

def run(*args):
    '''
    run attribute for runscript (python-extensions)
    '''
    if 'vagrant_boxes' in args:
        print(vagrant_boxes_list())
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

    return print(boxes)

def _global_status():
    cmd = ['global-status', '--machine-readable']
    output = _vagrant_command(cmd)
    parsed_lines = [line.split(',', 4) for line in output.splitlines() if line.strip()]
    del parsed_lines[-2:]
    del parsed_lines[:7]
    parsed_lines = list(filter(lambda x: x[4] !='', parsed_lines))

    vagrant_status = []
    Vagrant_Status = collections.namedtuple('Environment', ['uid', 'name', 'provider', 'state', 'path'])

    uid = name = provider = state = path = None
    for timestamp, extra, ui, info, data in parsed_lines:
        if data is not None:
            vagrant_status.append(Vagrant_Status(uid=uid, name=name, provider=provider, state=state, path=path))
            print(data)


    print(vagrant_status)
