import string
import requests
import logging
import datetime
import tweepy
import json
import itertools

from functools import wraps

from django.db.models import Q
from django.db.models import Min, Max
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect
from django.utils import simplejson
from django.template import RequestContext

from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from django.shortcuts import render as django_render

from urlparse import urlparse
from django.conf import settings

from flik.app.forms import *
from flik.app.models import User, Company

logger = logging.getLogger(__name__)

def render_to(template):
    def k(fun):
        @wraps(fun)
        def wrapper(request, *args, **kwargs):
            context = fun(request, *args, **kwargs)
            if type(context) == dict:
                return django_render(request, template, context)
            else:
                return context
        return wrapper
    return k

@render_to("home.html")
def login_view(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect(reverse("dashboard"))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                next = request.session.get("next")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse('scribbles'))
    else:
        form = LoginForm()
    return {'form': form}

@render_to("signup.html")
def signup(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect(reverse("dashboard"))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            company = request.POST.get("company_name")
            company = Company.objects.create(name=company, json={})
            user = User.objects.create(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    company=company)

            first_name = request.POST.get("first_name", "James")
            last_name = request.POST.get("last_name", "Johnson")
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = RegistrationForm()
    return {'form': form}

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def dashboard(request):
    return django_render(request, 'dashboard.html', context_instance=RequestContext(request))

def dashboard_fingerprints(request):
    company = request.user.company
    fingerprints = company.json.get("fingerprints", [])
    return django_render(request, 'dashboard/fingerprints.html', context_instance=RequestContext(request))

def dashboard_offers(request):
    company = request.user.company
    offers = company.json.get("offers", [])
    return django_render(request, 'dashboard/offers.html', context_instance=RequestContext(request))

def dashboard_fingerprints_create(request):
    company = request.user.company
    if request.method == 'POST':
        fingerprints = company.json.get("fingerprints", [])
        fingerprints.append(dict(request.POST))
        company.json['fingerprints'] = fingerprints
        company.save()
        return HttpResponseRedirect(reverse("dashboard-fingerprints-create"))
    return django_render(request, 'dashboard/fingerprints/create.html', context_instance=RequestContext(request))

def dashboard_offers_create(request):
    company = request.user.company
    if request.method == 'POST':
        offers = company.json.get("offers", [])
        offers.append(dict(request.POST))
        company.json['offers'] = offers
        company.save()
        return HttpResponseRedirect(reverse("dashboard-offers-create"))
    return django_render(request, 'dashboard/offers/create.html', context_instance=RequestContext(request))

def dashboard_campaigns_create(request):
    company = request.user.company
    if request.method == 'POST':
        campaigns = company.json.get("campaigns", [])
        campaigns.append(dict(request.POST))
        company.json['campaigns'] = campaigns
        company.save()
        return HttpResponseRedirect(reverse("dashboard-campaigns-create"))
    return django_render(request, 'dashboard/campaigns/create.html', context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("dashboard"))
