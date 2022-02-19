from django.shortcuts import render, redirect, HttpResponse
from . import util
import markdown
from django import forms
from django.http import JsonResponse

# model for getting the input when adding a new entry to the wiki 
class NewEntryForm(forms.Form):
    title = forms.CharField(label="title")
    md = forms.CharField(label="md")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def loadPage(request, filename):
    entry = util.get_entry(filename) # get the md file using get_entry method 
    if(entry == None): # if an exception is thrown "None": no result found
        response = render(request, "encyclopedia/wiki_not_found.html", {
            "title": filename
        })
        response.status_code = 404
        return response
    converted_result = markdown.markdown(entry)
    return render(request, "encyclopedia/show_page.html", {
        "title": filename, 
        "html": converted_result
    })

def createEntry(request):
    if request.method == "POST": 
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["md"]
            if util.get_entry(entry_title) == None:
                util.save_entry(entry_title, entry_md)
            else:
                return render(request, "encyclopedia/create_entry.html", {
                    "textarea": entry_md,
                    "titleField": entry_title, 
                    "duplicate_title_found": True
                })
        return redirect('loadpage', filename=entry_title)
    return render(request, "encyclopedia/create_entry.html", {
        "textarea": "",
        "titleField": "", 
        "duplicate_title_found": False
    })

def editEntry(request, filename):
    current_title = filename
    requested_entry = util.get_entry(filename)
    if requested_entry == None: 
        response = render(request, "encyclopedia/wiki_not_found.html", {
            "title": filename
        })
        response.status_code = 404
        return response
    if request.method == "POST": 
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            entry_md = form.cleaned_data["md"]
            if util.get_entry(entry_title) == None and entry_title != current_title:
                util.save_entry(entry_title, entry_md)
                util.remove_entry(current_title)
            else:
                return render(request, "encyclopedia/edit_entry.html", {
                    "textarea": entry_md,
                    "titleField": entry_title, 
                    "duplicate_title_found": True
                })
        return redirect('loadpage', filename=entry_title)
    return render(request, "encyclopedia/edit_entry.html", {
        "textarea": requested_entry,
        "titleField": filename, 
        "duplicate_title_found": False
    })

# handles search queries 
def search(request):
    q = str(request.GET["q"]).lower() 
    all_entries = util.list_entries() 
    results_available = [filename for filename in all_entries if q in filename.lower()]
    if len(results_available) == 0: # if no result found  
        return render(request, "encyclopedia/no_search_result_found.html", {
            "query": q
        })
    elif len(results_available) == 1: # if there's only one search result for the search redirect them to that page
        return loadPage(request, results_available[0])
    else: # if there's multiple search results
        return render(request, "encyclopedia/results.html", {
            "query": q, 
            "results": results_available
        })

# deletes an entry: only accepts POST requests
def api_deleteEntry(request):
    if request.method == "POST":
        filename = request.POST["filename"]
        print("deleting.. ( " + filename + " )" )
        util.remove_entry(filename)
        response_data = {
            "status":"deleted", 
            "filename": filename
        }
        return redirect('index')   
    else:
        return HttpResponse("Method not allowed")

