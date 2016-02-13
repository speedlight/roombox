from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import subprocess
from .scripts.vagrant_boxes import _box_list, _global_status

def index(request):
    sysinfo = systeminfo()
    vboxes = _box_list()
    venvs = _global_status()

    return render(request, 'manager/index.html', {'all_boxes': vboxes, 'all_envs': venvs, 'sysinfo': sysinfo, })

def systeminfo():
    sysinfo = {}
    vagrant_ver = subprocess.check_output('vagrant --version', shell=True, universal_newlines=True)
    vagrant_ver = vagrant_ver.strip('\n')
    vagrant_ver = vagrant_ver.split(' ')
    
    virtualbox_ver = subprocess.check_output("virtualbox --help |head -n1 |cut -d ' ' -f 5 |cut -d '_' -f 1", shell=True, universal_newlines=True)
    virtualbox_ver = virtualbox_ver.strip('\n')

    sysinfo["vagrant_version"] = vagrant_ver[1]
    sysinfo["virtualbox_version"] = virtualbox_ver

    return sysinfo
