from django.http import HttpResponse  # TWT ?

# not in use
# from django.shortcuts import render

# Nombre placeholder ?


def index(response, id):
    return HttpResponse("<h1>%s</h1>" % id)
