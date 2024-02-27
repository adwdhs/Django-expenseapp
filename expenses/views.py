from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense

from django.contrib import messages
from django.core.paginator import Paginator
import datetime
import json
from django.http import JsonResponse




@login_required(login_url='/authentication/login')
def index(request):

    categories = Category.objects.all()
    expenses = Expense.objects.filter(user=request.user)
    paginagor = Paginator(expenses, 5)
    page_num = request.GET.get('p')
    page_obj = paginagor.get_page(page_num)
    context = {
        'categories': categories,
        'expenses': expenses,
        'page_obj': page_obj,


    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
        'values': request.POST
    }


    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.error(request, 'Amount is Required')

            return render(request, 'expenses/add_expenses.html', context)

        description = request.POST.get('description')

        expense_date = request.POST.get('expense_date')
        category = request.POST.get('category')


        Expense.objects.create(amount=float(amount),
                               description=description,
                               date=expense_date,
                               category=category,
                               user=request.user)
        messages.success(request, 'Expense Saved Successfully')
        return redirect('expenses')
    return render(request, 'expenses/add_expenses.html', context)


def editExpense(request, pk):
    expense = Expense.objects.get(pk=pk)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }
    if request.method == 'GET':

        return render(request, 'expenses/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if not amount:
            messages.error(request, 'Amount is Required')

            return render(request, 'expenses/add_expenses.html', context)

        description = request.POST.get('description')



        expense_date = request.POST.get('expense_date')
        category = request.POST.get('category')

        expense.amount = amount
        expense.description = description
        expense.date = expense_date
        expense.category = category
        expense.user = request.user
        expense.save()

        messages.success(request, 'Expense Saved Successfully')
        return redirect('expenses')

def deleteExpense(request, pk):
    expense = Expense.objects.get(pk=pk)
    expense.delete()
    messages.info(request, 'Expense Removed')
    return redirect('expenses')

def categorySummary(request):
    today = datetime.date.today()
    six_m_ago = today - datetime.timedelta(days=180)
    expenses = Expense.objects.filter(date__gte=six_m_ago, date__lte=today, user=request.user)


    def get_category(expense):
        return expense.category

    categories_list = set(map(get_category, expenses))
    def categories_sum(categories_list):
        result = {}
        amount = 0
        for i in categories_list:
            filtered = Expense.objects.filter(category=i)
            for j in filtered:
                amount += j.amount
            result.update({i: amount})
            amount = 0

        return result
    results = categories_sum(categories_list)
    return JsonResponse({'expenses_sum_data': results}, safe=False)

def statsView(request):
    return render(request, 'expenses/statistics.html')










