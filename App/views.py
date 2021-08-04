#from typing_extensions import Required
from App.forms import LoginForm, ReservationForm, CreateUserForm
from django.db.models.fields import DateTimeField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from App.models import Guest, Reservation, Table
from datetime import date, datetime
import random
from django.template import loader
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction

# Create your views here.
def index(request):
    user_login = request.session.get('login_user', None)
    print(user_login)
    user_name = None if user_login is None else Guest.objects.filter(login=user_login).get().name
    template = loader.get_template('index.html')
    f = ReservationForm(guest=user_name)

    return render(request, 'index.html',{'user': user_login, 'login_form':LoginForm() ,'my_form': f})

def do_login(request):
    f = LoginForm(request.POST)
    try:
        if not f.is_valid():
            raise RuntimeError("Error: " + str(f.errors))

        g = Guest.objects.filter(login=f.cleaned_data['login'])
        if len(g) == 0 or not check_password(f.cleaned_data['password'], g[0].password):
            raise RuntimeError("Wrong user name or passsword.")

        request.session['login_user'] = g[0].login
    except RuntimeError as e:
        return HttpResponse(str(e) + "<p><a href=index>Go back</a>.")

    return redirect('index')

    
def do_logout(request):
    request.session['login_user'] = None
    return redirect('index')

def create_guest(request):
    return render(request, 'create.html', {'create_form': CreateUserForm()})

def do_create(request):
    f = CreateUserForm(request.POST)
    try:
        if not f.is_valid():
            raise RuntimeError("Error: " + str(f.errors))

        values = f.cleaned_data

        if len(Guest.objects.filter(login=values['login'])) > 0:
            raise RuntimeError("A Guest with the login '{}' already exists.".format(values['login']))

        if values['password'] != values['passagain']:
            raise RuntimeError("Passwords do not match.")

        Guest.objects.create(name=values['name'], login=values['login'], password=make_password(values['password']))

    except RuntimeError as e:
        return HttpResponse(str(e) + "<p><a href=create>Go back</a>.")

    return redirect('index')


def create_reservation(request):
    dt = datetime(2021,7,1,12,0,0)

    # Create new guest
    g = Guest.objects.all()
    if(g.__len__()==0):
        return redirect('index')

    g = g[random.randint(0,g.__len__()-1)]    
    g.save()

    # Search available table(sheet)
    tbls = Table.objects.filter(max_sheet__gte=g.number)
    t=None
    if(tbls.__len__()>0):
        t=tbls[0]

        # Search available table(not reserved)
        resvs = Reservation.objects.filter(timeslot=dt).filter(table=t)
        if(resvs.__len__()>0):
            t=None
    
    if(t==None):
        return redirect('index')
        
    r = Reservation(guest=g, table=t, timeslot=dt)
    r.save()
    return redirect('index')

def do_reserve(request):
    f = ReservationForm(request.POST, guest=None) #doctors=doctor_names, patient=None)
    user_login = request.session.get('authorized_user_login', None)

    MAX_DAILY_RESERVATIONS=10

    try:
        if not f.is_valid():
            raise RuntimeError("Error: " + str(f.errors))

        with transaction.atomic():
            g = (Guest.objects.create(name=f.cleaned_data['name'], login='', password='') if user_login is None 
                else Guest.objects.filter(login=user_login).get())
            r = Reservation.objects.filter(timeslot=f.cleaned_data['timeslot'])

            t = Table.objects.filter(max_sheet__gte=f.cleaned_data['num']).exclude(id__in=r.values('table')).order_by('max_sheet')
            
            if len(t)==0:
                raise RuntimeError("This date has full reservations...")
            
            if len(r) > MAX_DAILY_RESERVATIONS:
                raise RuntimeError("This date has full reservations...")

            Reservation.objects.create(timeslot=f.cleaned_data['timeslot'], guest=g, number=f.cleaned_data['num'], table=t[0])
    
    except RuntimeError as e:
        return HttpResponse(str(e) + "<p><a href=index>Go back</a>.")

    return render(request, 'reservation_ok.html', {'guest_name': f.cleaned_data['name'], 'num': f.cleaned_data['num'], 'datetime': f.cleaned_data['timeslot']})

def list_reservation(request):
    user_login = request.session.get('login_user', None)
    user = None if user_login is None else Guest.objects.filter(login=user_login).get()
    resvs = Reservation.objects.all()
    #i=0
    #for r in resvs:
    #    print(str(i)+': '+r.__str__())
    #    i += 1
    return render(request, 'reserve_list.html',{'user': user, 'reserves':resvs})