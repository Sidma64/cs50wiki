from django.http import Http404
from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entry_md = util.get_entry(entry)
    if entry_md == None:
        return Http404('<h1>Page not found</h1>')
    entry_html = markdown2.markdown(entry_md)
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_html": entry_html
    })

