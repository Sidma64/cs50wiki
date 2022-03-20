from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entryTitle):
    entry_md = util.get_entry(entryTitle)
    if entry_md == None:
        return Http404('<h1>Page not found</h1>')
    entry_html = markdown2.markdown(entry_md)
    
    return render(request, "encyclopedia/entry.html", {
        "entry": entryTitle,
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
        if title.lower() in (entryTitle.lower() for entryTitle in util.list_entries()):
            return HttpResponse(f'The entry for "{title}" already exists.')

        content = request.POST['content']
        util.save_entry(title, content)
        return redirect(entry, title)
    
    return render(request, "encyclopedia/addEntry.html")

def editEntry(request, entryTitle):
    if request.method == "POST":
        content = request.POST['content']
        util.save_entry(entryTitle, content)
        return redirect(entry, entryTitle)
    return render(request, "encyclopedia/editEntry.html", {
        "content": util.get_entry(entryTitle),
        "entry": entryTitle
    })
        
    

