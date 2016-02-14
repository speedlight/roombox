from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader
from django.views import generic

from .scripts.vagrant_boxes import _box_list, _global_status, _deps_versions

class IndexView(generic.ListView):
    template_name = 'manager/index.html'

    def get(self, request):
        versions = _deps_versions()
        vboxes = _box_list()
        venvs = _global_status()
    
        return render(request, self.template_name, {'all_boxes': vboxes, 'all_envs': venvs, 'versions': versions, })

