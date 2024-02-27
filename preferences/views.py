from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreferences
from django.contrib import messages

def index(request):

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})
    context = {'currencies': currency_data}

    exists = UserPreferences.objects.filter(user=request.user).exists()

    currency = request.POST.get('currency')
    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)
        user_preferences.currency = currency
        user_preferences.save()
        messages.success(request, 'Changes Saved')
        context.update({'user_preferences': user_preferences})

    else:
        user_preferences = UserPreferences.objects.create(user=request.user, currency=currency)
        user_preferences.save()
        messages.success(request, 'Changes Saved')

    context.update({'user_preferences': user_preferences})
    return render(request, 'preferences/index.html', context)
