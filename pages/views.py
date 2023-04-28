from asyncio.windows_events import NULL
from django.shortcuts import render
from . import models
# Create your views here.
from datetime import date,timedelta,datetime
from django.db.models import Max
from django.shortcuts import redirect
# ..\Scripts\activate
# python manage.py startapp
# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver
friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
last_friday = friday - timedelta(days=7)
# print(last_friday)
print(friday)
# .order_by('date','id')
def money_box(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    all_money_box = models.money_box.objects.all().order_by('id')
    for item in all_money_box.filter(date__gt = friday):
        bf_money_box = models.money_box.objects.filter(entry_date__lt = item.entry_date)
        bf_mn = sum([mnitem.income_id.price for mnitem in bf_money_box])
        bf_ep = sum([epitem.expenses_id.price for epitem in bf_money_box])

        mn = item.income_id.price
        ep = item.expenses_id.price
        item.box  = bf_mn + mn - ep - bf_ep
        if mn:
            item.date = item.income_id.date
        else:
            item.date = item.expenses_id.date
        item.save()
    x = {
        'title':'الحركات المالية',

        'all_money_box':all_money_box,
    }
    return render(request ,'pages/money_box.html',x)

def money_box_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    if request.method == "GET":
        data = request.GET
        if data:
            all_money_box = models.money_box.objects.filter(date__range =[data['fdate'],data['tdate']]).order_by('date','id')
        else:
            all_money_box = models.money_box.objects.all().order_by('date','id')
    else:
        all_money_box = models.money_box.objects.all().order_by('date','id')
    # for item in all_money_box:
    #     bf_money_box = models.money_box.objects.filter(entry_date__lt = item.entry_date)
    #     bf_mn = sum([mnitem.income_id.price for mnitem in bf_money_box])
    #     bf_ep = sum([epitem.expenses_id.price for epitem in bf_money_box])

    #     mn = item.income_id.price
    #     ep = item.expenses_id.price
    #     item.box  = bf_mn + mn - ep - bf_ep
    #     item.save()
    x = {
        'title':'الحركات المالية',
        'all_money_box':all_money_box,
    }
    return render(request ,'pages/money_box_print.html',x)

def index(request):
    # redirect('index')

    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    # week_iron_purchases = iron_purchases.objects.all()

    week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('-date','-id')
    today_iron_purchases = models.iron_purchases.objects.filter(date = date.today()).order_by('-date','-id')
    yes_iron_purchases = models.iron_purchases.objects.filter(date = (date.today()  - timedelta(days=1))).order_by('-date','-id')
    if week_iron_purchases:
        last =  week_iron_purchases.order_by('-id')[0]
    else:
        last = 0
    today_pistons = models.pistons.objects.filter(date = date.today()).order_by('-date','-id')
    yes_pistons = models.pistons.objects.filter(date = (date.today()  - timedelta(days=1))).order_by('-date','-id')
    week_pistons = models.pistons.objects.filter(date__gt = friday).order_by('-date','-id')

    fuel_incom = models.fuel_incom.objects.all().order_by('-date','-id')
    fuel = models.fuel.objects.all().order_by('-date','-id')
    still = (sum([item.quantity for item in fuel_incom]) - sum([item.quantity for item in fuel])  )
    if(still == NULL or still == " "):
        still = 0
    
    income = models.income.objects.all().order_by('-date','-id')
    expenses = models.expenses.objects.all().order_by('-date','-id')
    money_still = (sum([item.price for item in income]) - sum([item.price for item in expenses])  )
    if(money_still == NULL or money_still == " "):
        money_still = 0
    x = {
        'title':'الصفخة الرئيسية',

        'week_iron_purchases' : sum([item.quantity for item in week_iron_purchases]),
        'today_iron_purchases' : sum([item.quantity for item in today_iron_purchases]),
        'yes_iron_purchases' : sum([item.quantity for item in yes_iron_purchases]),

        'last':last,
        'today_pistons':sum([item.piston1 for item in today_pistons]) + sum([item.piston2 for item in today_pistons]) + sum([item.piston3 for item in today_pistons]),
        'yes_pistons':sum([item.piston1 for item in yes_pistons]) + sum([item.piston2 for item in yes_pistons]) + sum([item.piston3 for item in yes_pistons]),
        'week_pistons':sum([item.piston1 for item in week_pistons]) + sum([item.piston2 for item in week_pistons]) + sum([item.piston3 for item in week_pistons]),
        'fuel':still,
        'money_still':money_still,
        'today':date.today(),
    }
    return render(request ,'pages/index.html',x)

def week_sum(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)

    week_income_last_week = models.income.objects.filter(account_id = 1,date__gt = friday)

    week_income_all = models.income.objects.filter(date__gt = friday).order_by('-date','-id')
    week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday).order_by('-date','-id')
    week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday).order_by('-date','-id')
    week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday).order_by('-date','-id')

    week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('-date','-id')
    week_expenses_not_iron = models.expenses.objects.filter(date__gt = friday).exclude(account_id = 3).order_by('-date','-id')
    week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__gt = friday).order_by('-date','-id')

    week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('-date','-id')
    week_iron_sales = models.iron_sales.objects.filter(date__gt = friday).order_by('-date','-id')



    x = {
        'title':'البيان الاسبوعي',

        'week_income_last_week':sum([item.price for item in week_income_last_week]),
        'week_income_company':sum([item.price for item in week_income_company]),
        'week_income_company_week': sum([item.price for item in week_income_company]) + sum([item.price for item in week_income_last_week]),

        'week_income_weight_gain':sum([item.price for item in week_income_weight_gain]),
        'week_income_company_weekt_gain': sum([item.price for item in week_income_company]) + sum([item.price for item in week_income_last_week]) + sum([item.price for item in week_income_weight_gain]),

        'week_income_iron':sum([item.price for item in week_income_iron]),
        'week_income_company_weekt_gain_iron': sum([item.price for item in week_income_company]) + sum([item.price for item in week_income_last_week]) + sum([item.price for item in week_income_weight_gain]) + sum([item.price for item in week_income_iron]),

        'week_expenses_iron':sum([item.price for item in week_expenses_iron]),

        'week_income_company_weekt_gain_iron_expenses_iron': sum([item.price for item in week_income_company]) + sum([item.price for item in week_income_last_week]) + sum([item.price for item in week_income_weight_gain]) + sum([item.price for item in week_income_iron]) - sum([item.price for item in week_expenses_iron]),

        'week_expenses_not_iron':sum([item.price for item in week_expenses_not_iron]),
        'week_income_company_weekt_gain_iron_expenses_iron_not_iron': sum([item.price for item in week_income_company]) + sum([item.price for item in week_income_last_week]) + sum([item.price for item in week_income_weight_gain]) + sum([item.price for item in week_income_iron]) - sum([item.price for item in week_expenses_iron]) - sum([item.price for item in week_expenses_not_iron]),

        'week_income_all':sum([item.price for item in week_income_all]),
        'week_expenses_all':sum([item.price for item in week_expenses_all]),

        'week_iron_purchases_quantity' : sum([item.quantity for item in week_iron_purchases]),
        'week_iron_sales_quantity' : sum([item.quantity for item in week_iron_sales]),
        'today':date.today(),


    }
    return render(request ,'pages/week_sum.html',x)
    
def week_pyn(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)

    week_income_all = models.income.objects.filter(date__gt = friday).order_by('-date','-id')
    week_income_last_week = models.income.objects.filter(account_id = 1,date__gt = friday)
    week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday).order_by('-date','-id')
    week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday).order_by('-date','-id')
    week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday).order_by('-date','-id')

    week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('-date','-id')

    week_iron_purchases_st = models.iron_purchases.objects.filter(date = friday + timedelta(days=1)).order_by('-date','-id')
    week_iron_purchases_sn = models.iron_purchases.objects.filter(date = friday + timedelta(days=2)).order_by('-date','-id')
    week_iron_purchases_mn = models.iron_purchases.objects.filter(date = friday + timedelta(days=3)).order_by('-date','-id')
    week_iron_purchases_ty = models.iron_purchases.objects.filter(date = friday + timedelta(days=4)).order_by('-date','-id')
    week_iron_purchases_wn = models.iron_purchases.objects.filter(date = friday + timedelta(days=5)).order_by('-date','-id')
    week_iron_purchases_te = models.iron_purchases.objects.filter(date = friday + timedelta(days=6)).order_by('-date','-id')

    export = models.export.objects.filter(date__gt = friday).order_by('-date','-id')

    export_st = models.export.objects.filter(date = friday + timedelta(days=1)).order_by('-date','-id')
    export_sn = models.export.objects.filter(date = friday + timedelta(days=2)).order_by('-date','-id')
    export_mn = models.export.objects.filter(date = friday + timedelta(days=3)).order_by('-date','-id')
    export_ty = models.export.objects.filter(date = friday + timedelta(days=4)).order_by('-date','-id')
    export_wn = models.export.objects.filter(date = friday + timedelta(days=5)).order_by('-date','-id')
    export_te = models.export.objects.filter(date = friday + timedelta(days=6)).order_by('-date','-id')

    week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('-date','-id')
    week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__gt = friday).order_by('-date','-id')
    week_expenses_prpair_make = models.expenses.objects.filter(account_id__in = [5,10],date__gt = friday).order_by('-date','-id')
    week_expenses_food = models.expenses.objects.filter(account_id = 2,date__gt = friday).order_by('-date','-id')
    week_expenses_else = models.expenses.objects.filter(date__gt = friday).exclude(account_id__in = [3,5,10]).order_by('-date','-id')
    
    pistons_week = models.pistons.objects.filter(date__gt = friday).order_by('-date','-id')
    pistons_last_week = models.pistons.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')

    pistons = models.pistons.objects.filter(date__gt = friday).order_by('-date','-id')
    pistons_st = models.pistons.objects.filter(date = friday + timedelta(days=1)).order_by('-date','-id')
    pistons_sn = models.pistons.objects.filter(date = friday + timedelta(days=2)).order_by('-date','-id')
    pistons_mn = models.pistons.objects.filter(date = friday + timedelta(days=3)).order_by('-date','-id')
    pistons_ty = models.pistons.objects.filter(date = friday + timedelta(days=4)).order_by('-date','-id')
    pistons_wn = models.pistons.objects.filter(date = friday + timedelta(days=5)).order_by('-date','-id')
    pistons_te = models.pistons.objects.filter(date = friday + timedelta(days=6)).order_by('-date','-id')

    x ={
        'title':'البيان الاسبوعي البياني',

        'week_income_last_week':sum([item.price for item in week_income_last_week]),
        'week_income_company':sum([item.price for item in week_income_company]),
        'week_income_weight_gain':sum([item.price for item in week_income_weight_gain]),
        'week_income_iron':sum([item.price for item in week_income_iron]),
        'iron_wight': sum([item.price for item in week_income_weight_gain]) + sum([item.price for item in week_income_iron]),
        'week_income_all':sum([item.price for item in week_income_all]),
        'friday':friday,
        'today':date.today(),

        'week_iron_purchases_quantity':sum([item.quantity for item in week_iron_purchases]),
        'week_iron_purchases_st_quantity':sum([item.quantity for item in week_iron_purchases_st]),
        'week_iron_purchases_sn_quantity':sum([item.quantity for item in week_iron_purchases_sn]),
        'week_iron_purchases_mn_quantity':sum([item.quantity for item in week_iron_purchases_mn]),
        'week_iron_purchases_ty_quantity':sum([item.quantity for item in week_iron_purchases_ty]),
        'week_iron_purchases_wn_quantity':sum([item.quantity for item in week_iron_purchases_wn]),
        'week_iron_purchases_te_quantity':sum([item.quantity for item in week_iron_purchases_te]),

        'week_iron_purchases_price':sum([item.price for item in week_iron_purchases]),
        'week_iron_purchases_st_price':sum([item.price for item in week_iron_purchases_st]),
        'week_iron_purchases_sn_price':sum([item.price for item in week_iron_purchases_sn]),
        'week_iron_purchases_mn_price':sum([item.price for item in week_iron_purchases_mn]),
        'week_iron_purchases_ty_price':sum([item.price for item in week_iron_purchases_ty]),
        'week_iron_purchases_wn_price':sum([item.price for item in week_iron_purchases_wn]),
        'week_iron_purchases_te_price':sum([item.price for item in week_iron_purchases_te]),


        'export_output':sum([item.output for item in export]),
        'export_st_output':sum([item.output for item in export_st]),
        'export_sn_output':sum([item.output for item in export_sn]),
        'export_mn_output':sum([item.output for item in export_mn]),
        'export_ty_output':sum([item.output for item in export_ty]),
        'export_wn_output':sum([item.output for item in export_wn]),
        'export_te_output':sum([item.output for item in export_te]),

        'export_output_type2':sum([item.output_type2 for item in export]),
        'export_st_output_type2':sum([item.output_type2 for item in export_st]),
        'export_sn_output_type2':sum([item.output_type2 for item in export_sn]),
        'export_mn_output_type2':sum([item.output_type2 for item in export_mn]),
        'export_ty_output_type2':sum([item.output_type2 for item in export_ty]),
        'export_wn_output_type2':sum([item.output_type2 for item in export_wn]),
        'export_te_output_type2':sum([item.output_type2 for item in export_te]),

        'week_expenses_all':sum([item.price for item in week_expenses_all]),
        'week_expenses_iron':sum([item.price for item in week_expenses_iron]),
        'week_expenses_prpair_make':sum([item.price for item in week_expenses_prpair_make]),
        'week_expenses_food':sum([item.price for item in week_expenses_food]),
        'week_expenses_else':sum([item.price for item in week_expenses_else]),

        'pistons_week':sum([item.piston1 for item in pistons_week]) + sum([item.piston2 for item in pistons_week]) + sum([item.piston3 for item in pistons_week]),
        'pistons_last_week':sum([item.piston1 for item in pistons_last_week]) + sum([item.piston2 for item in pistons_last_week]) + sum([item.piston3 for item in pistons_last_week]),

        'pistons1':sum([item.piston1 for item in pistons]),
        'pistons1_st':sum([item.piston1 for item in pistons_st]),
        'pistons1_sn':sum([item.piston1 for item in pistons_sn]),
        'pistons1_mn':sum([item.piston1 for item in pistons_mn]),
        'pistons1_ty':sum([item.piston1 for item in pistons_ty]),
        'pistons1_wn':sum([item.piston1 for item in pistons_wn]),
        'pistons1_te':sum([item.piston1 for item in pistons_te]),

        'pistons2':sum([item.piston2 for item in pistons]),
        'pistons2_st':sum([item.piston2 for item in pistons_st]),
        'pistons2_sn':sum([item.piston2 for item in pistons_sn]),
        'pistons2_mn':sum([item.piston2 for item in pistons_mn]),
        'pistons2_ty':sum([item.piston2 for item in pistons_ty]),
        'pistons2_wn':sum([item.piston2 for item in pistons_wn]),
        'pistons2_te':sum([item.piston2 for item in pistons_te]),

        'pistons3':sum([item.piston3 for item in pistons]),
        'pistons3_st':sum([item.piston3 for item in pistons_st]),
        'pistons3_sn':sum([item.piston3 for item in pistons_sn]),
        'pistons3_mn':sum([item.piston3 for item in pistons_mn]),
        'pistons3_ty':sum([item.piston3 for item in pistons_ty]),
        'pistons3_wn':sum([item.piston3 for item in pistons_wn]),
        'pistons3_te':sum([item.piston3 for item in pistons_te]),
    }
    return render(request ,'pages/sum.html',x)

def iron_purchases(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        ac = models.accounts.objects.get(id = 3)
        iron = models.iron_purchases.objects.create(quantity=data['quantity'],pricing=data['pricing'],price=data['price'],date=data['date'],notes=data['notes'] )
        
        expenses_ma = models.expenses.objects.create(price=data['price'],operation_id=iron.id,date=data['date'],account=ac,notes=data['notes'] )
        models.money_box.objects.create(expenses_id=expenses_ma,type="expenses",date=data['date'])
    
    if request.method == "GET":
        data = request.GET
        day_iron_purchases = models.iron_purchases.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')
        day_iron_purchases_quantity = sum([item.quantity for item in day_iron_purchases])
        day_iron_purchases_price = sum([item.price for item in day_iron_purchases])
    else:
        day_iron_purchases = 0
        day_iron_purchases_quantity = 0
        day_iron_purchases_price = 0
        data_as = 0
        
    week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('-date','-id')
    last_week_iron_purchases = models.iron_purchases.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')
    all_last_week_iron_purchases = models.iron_purchases.objects.filter(date__lt = last_friday).order_by('-date','-id')

    try:
        day_iron_sales_purchases = day_iron_purchases_price / day_iron_purchases_quantity
    except ZeroDivisionError:
        day_iron_sales_purchases = 0
    try:
        week_iron_sales_purchases = sum([item.price for item in week_iron_purchases]) / sum([item.quantity for item in week_iron_purchases])
    except ZeroDivisionError:
        week_iron_sales_purchases = 0
    try:
        last_week_iron_sales_purchases = sum([item.price for item in last_week_iron_purchases]) / sum([item.quantity for item in last_week_iron_purchases])
    except ZeroDivisionError:
        last_week_iron_sales_purchases = 0
    try:
        all_last_week_iron_sales_purchases = sum([item.price for item in all_last_week_iron_purchases]) / sum([item.quantity for item in all_last_week_iron_purchases])
    except ZeroDivisionError:
        all_last_week_iron_sales_purchases = 0
    x = {
        'title':'مشتريات الحديد',

        'last_week_iron_purchases':last_week_iron_purchases,
        'last_week_iron_purchases_quantity' : sum([item.quantity for item in last_week_iron_purchases]),
        'last_week_iron_purchases_price' : sum([item.price for item in last_week_iron_purchases]),
        'last_pricing':last_week_iron_sales_purchases,

        'all_last_week_iron_purchases':all_last_week_iron_purchases,
        'all_last_week_iron_purchases_quantity' : sum([item.quantity for item in all_last_week_iron_purchases]),
        'all_last_week_iron_purchases_price' : sum([item.price for item in all_last_week_iron_purchases]),
        'all_last_pricing':all_last_week_iron_sales_purchases,

        'week_iron_purchases_quantity' : sum([item.quantity for item in week_iron_purchases]),
        'week_iron_purchases_price' : sum([item.price for item in week_iron_purchases]),
        'week_iron_purchases' :week_iron_purchases,
        'pricing':week_iron_sales_purchases,
        'today':date.today(),

        'day_iron_purchases':day_iron_purchases,
        'day_iron_purchases_quantity' : day_iron_purchases_quantity,
        'day_iron_purchases_price' : day_iron_purchases_price,
        'day_pricing':day_iron_sales_purchases,
        'data_as':data_as,
    }
    return render(request ,'pages/iron_purchases.html',x)

def iron_purchases_child(request,id):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    week_iron_purchases_child = models.iron_purchases.objects.get(id = id )
    x = {
    'title':f'عمليات شراء الحديد | {week_iron_purchases_child.id}',

    'week_iron_purchases_child':week_iron_purchases_child,
        'today':date.today(),
    }
    return render(request ,'pages/iron_purchases_child.html',x)
def iron_purchases_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    today = date.today()

    if request.method == "GET":
        data = request.GET
        if data:
            week_iron_purchases = models.iron_purchases.objects.filter(date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            fdate = data['fdate']
            tdate = data['tdate']
        else:
            week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('date','id')
            fdate = friday
            tdate = today
    else:
        week_iron_purchases = models.iron_purchases.objects.filter(date__gt = friday).order_by('date','id')
        fdate = friday
        tdate = today
    try:
        week_iron_sales_purchases = sum([item.price for item in week_iron_purchases]) / sum([item.quantity for item in week_iron_purchases])
    except ZeroDivisionError:
        week_iron_sales_purchases = 0
    print(fdate)
    x = {
        'title':'مشتريات الحديد',
        'week_iron_purchases_quantity' : sum([item.quantity for item in week_iron_purchases]),
        'week_iron_purchases_price' : sum([item.price for item in week_iron_purchases]),
        'week_iron_purchases' :week_iron_purchases,
        'pricing':week_iron_sales_purchases,
        'fdate':fdate,
        'tdate':tdate,
    }
    return render(request ,'pages/iron_purchases_print.html',x)

    
def iron_sales(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        ac = models.accounts.objects.get(id = 4)
        iron = models.iron_sales.objects.create(quantity=data['quantity'],pricing=data['pricing'],price=data['price'],date=data['date'],notes=data['notes'] )

        income_ma = models.income.objects.create(price=data['price'],operation_id=iron.id,date=data['date'],account=ac,notes=data['notes'] )

        models.money_box.objects.create(income_id=income_ma,type="income",date=data['date'])

    if request.method == "GET":
        data = request.GET
        day_iron_sales = models.iron_sales.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')
        day_iron_sales_quantity = sum([item.quantity for item in day_iron_sales])
        day_iron_sales_price = sum([item.price for item in day_iron_sales])
    else:
        day_iron_sales = 0
        data_as = 0
        day_iron_sales_quantity = 0
        day_iron_sales_price = 0
    week_iron_sales = models.iron_sales.objects.filter(date__gt = friday).order_by('-date','-id')
    last_week_iron_sales = models.iron_sales.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')
    all_week_iron_sales = models.iron_sales.objects.filter(date__lt = last_friday).order_by('-date','-id')

    try:
        day_iron_sales_pricing = day_iron_sales_price / day_iron_sales_quantity
    except ZeroDivisionError:
        day_iron_sales_pricing = 0
    try:
        week_iron_sales_pricing = sum([item.price for item in week_iron_sales]) / sum([item.quantity for item in week_iron_sales])
    except ZeroDivisionError:
        week_iron_sales_pricing = 0
    try:
        last_week_iron_sales_pricing = sum([item.price for item in last_week_iron_sales]) / sum([item.quantity for item in last_week_iron_sales])
    except ZeroDivisionError:
        last_week_iron_sales_pricing = 0
    try:
        all_week_iron_sales_pricing = sum([item.price for item in all_week_iron_sales]) / sum([item.quantity for item in all_week_iron_sales])
    except ZeroDivisionError:
        all_week_iron_sales_pricing = 0
    x = {
        'title':'مبيعات الحديد',

        'week_iron_sales_quantity' : sum([item.quantity for item in week_iron_sales]),
        'week_iron_sales_price' : sum([item.price for item in week_iron_sales]),
        'week_iron_sales' :week_iron_sales,
        'pricing':week_iron_sales_pricing,

        'last_week_iron_sales_quantity' : sum([item.quantity for item in last_week_iron_sales]),
        'last_week_iron_sales_price' : sum([item.price for item in last_week_iron_sales]),
        'last_week_iron_sales' :last_week_iron_sales,
        'last_pricing':last_week_iron_sales_pricing,

        'all_week_iron_sales_quantity' : sum([item.quantity for item in all_week_iron_sales]),
        'all_week_iron_sales_price' : sum([item.price for item in all_week_iron_sales]),
        'all_week_iron_sales' :all_week_iron_sales,
        'all_pricing':all_week_iron_sales_pricing,
        'today':date.today(),

        'day_iron_sales':day_iron_sales,
        'day_iron_sales_quantity' : day_iron_sales_quantity,
        'day_iron_sales_price' : day_iron_sales_price,
        'day_pricing':day_iron_sales_pricing,
        'data_as':data_as,
    }
    return render(request ,'pages/iron_sales.html',x)

def iron_sales_child(request,id):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    iron_sales_child = models.iron_purchases.objects.get(id = id )
    x = {
    'title':f'عمليات بيع الحديد | {iron_sales_child.id}',

    'iron_sales_child':iron_sales_child,
    'today':date.today(),
    }
    return render(request ,'pages/iron_sales_child.html',x)

def income(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST

        ac = models.accounts.objects.get(id = data['account'])
        # models.income.objects.create(price=data['price'],date=data['date'],account=ac,notes=data['notes'] )
        income_ma = models.income.objects.create(price=data['price'],date=data['date'],account=ac,notes=data['notes'] )

        models.money_box.objects.create(income_id=income_ma,type="income",date=data['date'])
    
    if request.method == "GET":
        data = request.GET
        day_income = models.income.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        day_income_company = models.income.objects.filter(account_id = 6,date = data.get('data_as')).order_by('-date','-id')
        day_income_iron = models.income.objects.filter(account_id = 4,date = data.get('data_as')).order_by('-date','-id')
        day_income_weight_gain = models.income.objects.filter(account_id = 7,date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')

        day_income_all = day_income
        day_income_company= sum([item.price for item in day_income_company])
        day_income_iron= sum([item.price for item in day_income_iron])
        day_income_weight_gain= sum([item.price for item in day_income_weight_gain])
        day_income_all_price = sum([item.price for item in day_income])

    else:
        day_income_all = 0
        day_income_company= 0
        day_income_iron= 0
        day_income_weight_gain= 0
        day_income_all_price = 0
        data_as = 0

    week_income_all = models.income.objects.filter(date__gt = friday).order_by('-date','-id')
    week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday).order_by('-date','-id')
    week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday).order_by('-date','-id')
    week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday).order_by('-date','-id')
    week_income_last_week = models.income.objects.filter(account_id = 1,date__gt = friday)
    week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('-date','-id')

    last_week_income_all = models.income.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_income_company = models.income.objects.filter(account_id = 6,date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_income_iron = models.income.objects.filter(account_id = 4,date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_income_weight_gain = models.income.objects.filter(account_id = 7,date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_income_last_week = models.income.objects.filter(account_id = 1,date__range =[last_friday,friday])
    last_week_expenses_all = models.expenses.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')

    all_week_income_all = models.income.objects.filter(date__lt = last_friday).order_by('-date','-id')
    all_week_income_company = models.income.objects.filter(account_id = 6,date__lt = last_friday).order_by('-date','-id')
    all_week_income_iron = models.income.objects.filter(account_id = 4,date__lt = last_friday).order_by('-date','-id')
    all_week_income_weight_gain = models.income.objects.filter(account_id = 7,date__lt = last_friday).order_by('-date','-id')
    all_week_expenses_all = models.expenses.objects.filter(date__lt = last_friday).order_by('-date','-id')

    income_accounts = models.accounts.objects.filter(use__id = 1).order_by('-entry_date')

    x = {
        'title':'المدخولات المالية',

        'week_income_price' : sum([item.price for item in week_income_all]),
        'week_income_all' :week_income_all,
        'week_income_company':sum([item.price for item in week_income_company]),
        'week_income_iron':sum([item.price for item in week_income_iron]),
        'week_income_last_week':sum([item.price for item in week_income_last_week]),
        'week_income_weight_gain':sum([item.price for item in week_income_weight_gain]),
        'week_income_all_price' :sum([item.price for item in week_income_all]),
        'week_expenses_all_price' :sum([item.price for item in week_expenses_all]),
        'bc':sum([item.price for item in week_income_all]) - sum([item.price for item in week_expenses_all]),

        'all_week_income_price' : sum([item.price for item in all_week_income_all]),
        'all_week_income_all' :all_week_income_all,
        'all_week_income_company':sum([item.price for item in all_week_income_company]),
        'all_week_income_iron':sum([item.price for item in all_week_income_iron]),
        'all_week_income_weight_gain':sum([item.price for item in all_week_income_weight_gain]),
        'all_week_income_all_price' :sum([item.price for item in all_week_income_all]),
        'all_week_expenses_all_price' :sum([item.price for item in all_week_expenses_all]),
        'all_bc':sum([item.price for item in all_week_income_all]) - sum([item.price for item in all_week_expenses_all]),


        'last_week_income_price' : sum([item.price for item in last_week_income_all]),
        'last_week_income_all' :last_week_income_all,
        'last_week_income_company':sum([item.price for item in last_week_income_company]),
        'last_week_income_iron':sum([item.price for item in last_week_income_iron]),
        'last_week_income_last_week':sum([item.price for item in last_week_income_last_week]),
        'last_week_income_weight_gain':sum([item.price for item in last_week_income_weight_gain]),
        'last_week_income_all_price' :sum([item.price for item in last_week_income_all]),
        'last_week_expenses_all_price' :sum([item.price for item in last_week_expenses_all]),
        'last_bc':sum([item.price for item in last_week_income_all]) - sum([item.price for item in last_week_expenses_all]),

        'income_accounts':income_accounts,
        'today':date.today(),

        'day_income_all' :day_income_all,
        'day_income_company':day_income_company,
        'day_income_iron':day_income_iron,
        'day_income_weight_gain':day_income_weight_gain,
        'day_income_all_price' :day_income_all_price,
        'data_as':data_as,

    }
    return render(request ,'pages/income.html',x)

def income_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    today = date.today()
    if request.method == "GET":
        data = request.GET
        if data:
            week_expenses_all = models.expenses.objects.filter(date__range =[data['fdate'],data['tdate']]).exclude(account_id = 1).order_by('date','id')
            week_income_all = models.income.objects.filter(date__gt = friday,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            week_expenses_all = models.expenses.objects.filter(date__gt = friday,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
            fdate = data['fdate']
            tdate = data['tdate']
        else:
            week_income_all = models.income.objects.filter(date__gt = friday).order_by('date','id')
            week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday).order_by('date','id')
            week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday).order_by('date','id')
            week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday).order_by('date','id')
            week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('date','id')
            fdate = friday
            tdate = today
    else:
        week_income_all = models.income.objects.filter(date__gt = friday).order_by('date','id')
        week_income_company = models.income.objects.filter(account_id = 6,date__gt = friday).order_by('date','id')
        week_income_iron = models.income.objects.filter(account_id = 4,date__gt = friday).order_by('date','id')
        week_income_weight_gain = models.income.objects.filter(account_id = 7,date__gt = friday).order_by('date','id')
        week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('date','id')
        fdate = friday
        tdate = today


    income_accounts = models.accounts.objects.filter(use__id = 1).order_by('entry_date')
    x = {
        'title':'المدخولات المالية',

        'week_income_price' : sum([item.price for item in week_income_all]),
        'week_income_all' :week_income_all,
        'week_income_company':sum([item.price for item in week_income_company]),
        'week_income_iron':sum([item.price for item in week_income_iron]),
        'week_income_weight_gain':sum([item.price for item in week_income_weight_gain]),
        'week_income_all_price' :sum([item.price for item in week_income_all]),
        'week_expenses_all_price' :sum([item.price for item in week_expenses_all]),
        'bc':sum([item.price for item in week_income_all]) - sum([item.price for item in week_expenses_all]),
        'income_accounts':income_accounts,
        'today':date.today(),
        'friday':friday,
        'fdate':fdate,
        'tdate':tdate,
    }
    return render(request ,'pages/income_print.html',x)

def expenses(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    if request.method == "POST":
        data = request.POST
        ac = models.accounts.objects.get(id = data['account'])
        expenses_ma = models.expenses.objects.create(price=data['price'],bio=data['bio'],date=data['date'],account=ac,notes=data['notes'] )

        models.money_box.objects.create(expenses_id=expenses_ma,type="expenses",date=data['date'])

    if request.method == "GET":
        data = request.GET
        day_expenses_all = models.expenses.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        day_expenses_not_iron = models.expenses.objects.filter(date = data.get('data_as')).exclude(account_id = 3).order_by('-date','-id')
        day_expenses_iron = models.expenses.objects.filter(account_id = 3,date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')

        day_expenses_price =  sum([item.price for item in day_expenses_all])
        day_expenses_not_iron = sum([item.price for item in day_expenses_not_iron])
        day_expenses_iron = sum([item.price for item in day_expenses_iron])
        day_expenses_all_price = sum([item.price for item in day_expenses_all])
    else:
        day_expenses_all = 0
        day_expenses_not_iron = 0
        day_expenses_iron = 0
        data_as = 0

        day_expenses_price =  0
        day_expenses_not_iron= 0
        day_expenses_iron= 0
        day_expenses_all_price = 0


        
    week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('-date','-id')
    week_expenses_not_iron = models.expenses.objects.filter(date__gt = friday).exclude(account_id = 3).order_by('-date','-id')
    week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__gt = friday).order_by('-date','-id')
    week_income_all = models.income.objects.filter(date__gt = friday).order_by('-date','-id')
    expenses_accounts = models.accounts.objects.filter(use__id = 2).order_by('-entry_date')

    last_week_expenses_all = models.expenses.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_expenses_not_iron = models.expenses.objects.filter(date__range =[last_friday,friday]).exclude(account_id__in = [1,3]).order_by('-date','-id')
    last_week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_expenses_transfer = models.expenses.objects.filter(account_id = 1,date__range =[last_friday,friday]).order_by('-date','-id')
    last_week_income_all = models.income.objects.filter(date__range =[last_friday,friday]).order_by('-date','-id')



    all_week_expenses_all = models.expenses.objects.filter(date__lt = last_friday).order_by('-date','-id')
    all_week_expenses_not_iron = models.expenses.objects.filter(date__lt = last_friday).exclude(account_id = 3).order_by('-date','-id')
    all_week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__lt = last_friday).order_by('-date','-id')
    all_week_income_all = models.income.objects.filter(date__lt = last_friday).order_by('-date','-id')

    x = {
        'title':'المصروفات المالية',

        'week_expenses_price' : sum([item.price for item in week_expenses_all]),
        'week_expenses_all' :week_expenses_all,
        'week_expenses_not_iron':sum([item.price for item in week_expenses_not_iron]),
        'week_expenses_iron':sum([item.price for item in week_expenses_iron]),
        'week_expenses_all_price' :sum([item.price for item in week_expenses_all]),
        'week_income_all_price' :sum([item.price for item in week_income_all]),
        'bc':sum([item.price for item in week_income_all]) - sum([item.price for item in week_expenses_all]),

        'last_week_expenses_price' : sum([item.price for item in last_week_expenses_all]),
        'last_week_expenses_all' :last_week_expenses_all,
        'last_week_expenses_not_iron':sum([item.price for item in last_week_expenses_not_iron]),
        'last_week_expenses_iron':sum([item.price for item in last_week_expenses_iron]),
        'last_week_expenses_transfer':sum([item.price for item in last_week_expenses_transfer]),
        'last_week_expenses_all_price' :sum([item.price for item in last_week_expenses_all]),
        'last_week_income_all_price' :sum([item.price for item in last_week_income_all]),
        'last_bc':sum([item.price for item in last_week_income_all]) - sum([item.price for item in last_week_expenses_all]),

        'all_week_expenses_price' : sum([item.price for item in all_week_expenses_all]),
        'all_week_expenses_all' :all_week_expenses_all,
        'all_week_expenses_not_iron':sum([item.price for item in all_week_expenses_not_iron]),
        'all_week_expenses_iron':sum([item.price for item in all_week_expenses_iron]),
        'all_week_expenses_all_price' :sum([item.price for item in all_week_expenses_all]),
        'all_week_income_all_price' :sum([item.price for item in all_week_income_all]),
        'all_bc':sum([item.price for item in all_week_income_all]) - sum([item.price for item in all_week_expenses_all]),

        'expenses_accounts':expenses_accounts,
        'today':date.today(),

        'day_expenses_price' : day_expenses_price,
        'day_expenses_all' :day_expenses_all,
        'day_expenses_not_iron':day_expenses_not_iron,
        'day_expenses_iron':day_expenses_iron,
        'day_expenses_all_price' :day_expenses_all_price,
        'data_as':data_as,
    }
    return render(request ,'pages/expenses.html',x)

def expenses_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    today = date.today()
    if request.method == "GET":
        data = request.GET
        if data:
            print(data['wtprint'])
            if data['wtprint'] == "2":
               return redirect(f'/expenses/print_noiron?fdate={data["fdate"]}&tdate={data["tdate"]}')
            else:
                week_expenses_all = models.expenses.objects.filter(date__range =[data['fdate'],data['tdate']]).exclude(account_id = 1).order_by('date','id')
                week_expenses_not_iron = models.expenses.objects.filter(date__range =[data['fdate'],data['tdate']]).exclude(account_id__in = [1,3]).order_by('date','id')
                week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__range =[data['fdate'],data['tdate']]).order_by('date','id')
                fdate = data['fdate']
                tdate = data['tdate']
        else:
            week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('date','id')
            week_expenses_not_iron = models.expenses.objects.filter(date__gt = friday).exclude(account_id__in = [1,3]).order_by('date','id')
            week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__gt = friday).order_by('date','id')
            fdate = friday
            tdate = today
    else:
        week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('date','id')
        week_expenses_not_iron = models.expenses.objects.filter(date__gt = friday).exclude(account_id__in = [1,3]).order_by('date','id')
        week_expenses_iron = models.expenses.objects.filter(account_id = 3,date__gt = friday).order_by('date','id')

    
    x = {
        'title':'المصروفات المالية',
        
        'week_expenses_price' : sum([item.price for item in week_expenses_all]),
        'week_expenses_all' :week_expenses_all,
        'week_expenses_not_iron':sum([item.price for item in week_expenses_not_iron]),
        'week_expenses_iron':sum([item.price for item in week_expenses_iron]),
        'week_expenses_all_price' :sum([item.price for item in week_expenses_all]),
        'fdate':fdate,
        'tdate':tdate,

    }
    return render(request ,'pages/expenses_print.html',x)

def expenses_print_noiron(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    week_expenses_all = models.expenses.objects.filter(date__gt = friday).order_by('date','id')
    week_expenses_not_iron = models.expenses.objects.filter(date__gt = friday).exclude(account_id = 3).order_by('date','id')
    week_income_all = models.income.objects.filter(date__gt = friday).order_by('date','id')
    expenses_accounts = models.accounts.objects.filter(use__id = 2).order_by('entry_date')
    x = {
        'title':'المصروفات المالية غير شاملة مشتريات الحديد',

        'week_expenses_price' : sum([item.price for item in week_expenses_all]),
        'week_expenses_all' :week_expenses_all,
        'week_expenses_not_iron' :week_expenses_not_iron,
        'week_expenses_not_iron_pr':sum([item.price for item in week_expenses_not_iron]),
        'week_expenses_all_price' :sum([item.price for item in week_expenses_all]),
        'week_income_all_price' :sum([item.price for item in week_income_all]),
        'bc':sum([item.price for item in week_income_all]) - sum([item.price for item in week_expenses_all]),
        'expenses_accounts':expenses_accounts,
        'today':date.today(),
        'friday':friday
    }
    return render(request ,'pages/expenses_print_noiron.html',x)

def pistons(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        models.pistons.objects.create(date=data['date'],piston1=data['piston1'],piston2=data['piston2'],piston3=data['piston3'],notes=data['notes'] )

    if request.method == "GET":
        data = request.GET
        day_pistons = models.pistons.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')
    else:
        day_pistons = 0
        data_as = 0
        
    all_pistons = models.pistons.objects.filter().order_by('-date','-id')

    x = {
        'title':'انتاج المكابس',

        'all_pistons':all_pistons,
        'today':date.today(),

        'day_pistons':day_pistons,
        'data_as':data_as,
    }
    return render(request ,'pages/pistons.html',x)

def pistons_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    today = date.today()

    if request.method == "GET":
        data = request.GET
        if data:
            all_pistons = models.pistons.objects.filter(date__range =[data['fdate'],data['tdate']]).order_by('-date','-id')
            fdate = data['fdate']
            tdate = data['tdate']
        else:
            all_pistons = models.pistons.objects.filter().order_by('-date','-id')
            fdate = friday
            tdate = today
        


    x = {
        'title':'انتاج المكابس',

        'all_pistons':all_pistons,
        'today':date.today(),
        'fdate':fdate,
        'tdate':tdate,

    }
    return render(request ,'pages/pistons_print.html',x)

def fuel_box(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    all_fuel_box = models.fuel_box.objects.all().order_by('id')
    for item in all_fuel_box:
        bf_fuel_box = models.fuel_box.objects.filter(entry_date__lt = item.entry_date)

        bf_fuel = sum([mnitem.fuel_id.quantity for mnitem in bf_fuel_box])
        bf_fuel_incom = sum([epitem.fuel_incom_id.quantity for epitem in bf_fuel_box])

        print(bf_fuel)
        print(bf_fuel_incom)
        mn = item.fuel_incom_id.quantity
        ep = item.fuel_id.quantity
        print(mn)
        print(ep)
        item.box  = bf_fuel_incom + mn - ep - bf_fuel
        item.save()
    x = {
        'title':'حركات مخزن الوقود',

        'all_fuel_box':all_fuel_box,
    }
    return render(request ,'pages/fuel_box.html',x)

def fuel_box_print(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    all_fuel_box = models.fuel_box.objects.all().order_by('id')
    for item in all_fuel_box:
        bf_fuel_box = models.fuel_box.objects.filter(entry_date__lt = item.entry_date)

        bf_fuel = sum([mnitem.fuel_id.quantity for mnitem in bf_fuel_box])
        bf_fuel_incom = sum([epitem.fuel_incom_id.quantity for epitem in bf_fuel_box])

        print(bf_fuel)
        print(bf_fuel_incom)
        mn = item.fuel_incom_id.quantity
        ep = item.fuel_id.quantity
        print(mn)
        print(ep)
        item.box  = bf_fuel_incom + mn - ep - bf_fuel
        item.save()
    x = {
        'title':'حركات مخزن الوقود',

        'all_fuel_box':all_fuel_box,
    }
    return render(request ,'pages/fuel_box_print.html',x)


def fuel(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        ac = models.accounts.objects.get(id = data['account'])
        fuel_ma = models.fuel.objects.create(quantity=data['quantity'],date=data['date'],account=ac,notes=data['notes'] )

        models.fuel_box.objects.create(fuel_id=fuel_ma,type="fuel",date=data['date'])

    if request.method == "GET":
        data = request.GET
        day_fuel = models.fuel.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')
    else:
        day_fuel = 0
        data_as = 0
    fuel = models.fuel.objects.all().order_by('-date','-id')
    fuel_incom = models.fuel_incom.objects.all().order_by('-date','-id')
    fuel_still = sum([item.quantity for item in fuel_incom]) - sum([item.quantity for item in fuel])
    fuel_accounts = models.accounts.objects.filter(use__id = 3).order_by('-entry_date')

    x = {
        'title':'اخرجات الوقود',

        'fuel':fuel,
        'all_fuel':sum([item.quantity for item in fuel]),
        'fuel_incom':fuel_incom,
        'all_fuel_incom':sum([item.quantity for item in fuel_incom]),
        'fuel_still':fuel_still,
        'fuel_accounts':fuel_accounts,
        'today':date.today(),

        'day_fuel':day_fuel,
        'data_as':data_as,
    }
    return render(request ,'pages/fuel.html',x)

def fuel_incom(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        fuel_incom_ma = models.fuel_incom.objects.create(quantity=data['quantity'],date=data['date'],notes=data['notes'] )

        models.fuel_box.objects.create(fuel_incom_id=fuel_incom_ma,type="fuel_incom",date=data['date'])

    if request.method == "GET":
        data = request.GET
        day_fuel_incom = models.fuel_incom.objects.filter(date = data.get('data_as')).order_by('-date','-id')
        data_as = data.get('data_as')
    else:
        day_fuel_incom = 0
        data_as = 0

    fuel = models.fuel.objects.all().order_by('-date','-id')
    fuel_incom = models.fuel_incom.objects.all().order_by('-date','-id')
    fuel_still = sum([item.quantity for item in fuel_incom]) - sum([item.quantity for item in fuel])
    x = {
        'title':'ادخالات الوقود',

        'fuel':fuel,
        'all_fuel':sum([item.quantity for item in fuel]),
        'fuel_incom':fuel_incom,
        'all_fuel_incom':sum([item.quantity for item in fuel_incom]),
        'fuel_still':fuel_still,
        'today':date.today(),

        'day_fuel_incom':day_fuel_incom,
        'data_as':data_as,
    }
    return render(request ,'pages/fuel_incom.html',x)

def weight_gain(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        ac = models.accounts.objects.get(id = 7)
        weight_gain = models.weight_gain.objects.create(price=data['price'],date=data['date'] ,notes=data['notes'])
        income_ma = models.income.objects.create(price=data['price'],operation_id=weight_gain.id,date=data['date'], account=ac,notes=data['notes'])
        
        models.money_box.objects.create(income_id=income_ma,type="income",date=data['date'])
        
    weight_gain = models.weight_gain.objects.all().order_by('-date','-id')
    x = {
        'title':'ادخلات خدمات التوزين',

        'weight_gain':weight_gain,
        'week_weight_gain':sum([item.price for item in weight_gain]),
        'today':date.today(),
    }
    return render(request ,'pages/weight_gain.html',x)

def export(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    if request.method == "POST":
        data = request.POST
        models.export.objects.create(output=data['output'],output_type2 = data['output_type2'],weight=data['weight'],iron_floors=data['iron_floors'],date=data['date'],notes=data['notes'])

    export = models.export.objects.all().order_by('-date','-id')
    week_export = models.export.objects.filter(date__gt = friday).order_by('-date','-id')
    x = {
    'title':'عمليات التصدير',

    'export':export,
    'all_export':sum([item.output for item in export]),
    'all_week_export':sum([item.output for item in week_export]),
    'all_week_export_type2':sum([item.output_type2 for item in week_export]),
    'today':date.today(),
    }
    return render(request ,'pages/export.html',x)

def accounts(request):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    accounts = models.accounts.objects.all()
    x = {
        'title':'الحسابات',

        'accounts':accounts,
        'today':date.today(),
    }
    return render(request ,'pages/accounts.html',x)

def accounts_child(request,id):
    friday = date.today() - timedelta(days=((date.today().weekday() - 4) % 7))
    last_friday = friday - timedelta(days=7)
    
    accounts = models.accounts.objects.get(id = id)
    income = models.income.objects.filter(account__id = id).order_by('-date','-id')
    fuel = models.fuel.objects.filter(account__id = id).order_by('-date','-id')
    expenses = models.expenses.objects.filter(account__id = id).order_by('-date','-id')

    x = {
    'title':f'الحسابات | {accounts.name}',

        'accounts':accounts,
        'income':income,
        'fuel':fuel,
        'expenses':expenses,
        'today':date.today(),


    }
    return render(request ,'pages/accounts_child.html',x)