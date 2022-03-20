from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
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

def search(request):
    # Check if there is a q variable inside the URL and make a variable for it.
    if query := request.GET['q']:
        # Get all the saved entries
        savedEntries = util.list_entries()

        # If search exactly matches an entry name, redirect to it.
        if query in savedEntries:
            return redirect(entry, query)
        # Casefold the query to make it case insensitive.
        else:
            
            casefoldQuery = query.casefold()
            # Variable for matched entries
            matches = []
            for savedEntry in savedEntries:
                if casefoldQuery in savedEntry.casefold():
                    matches.append(savedEntry)
            return render(request, "encyclopedia/index.html", {
                "entries": matches
            })            
    else:
        # If there is not q variable found return 400.
        return HttpResponseBadRequest()

def addEntry(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        redirect(entry, title)
    
    return render(request, "encyclopedia/addEntry.html")
        
    

