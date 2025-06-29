from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.http import JsonResponse
from .models import Appointment
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

def home(request):
    skills = Skill.objects.all()
    return render(request, 'home.html', {'skills': skills})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



@csrf_protect
def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('dashboard')  # ✅ redirect to dashboard after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user_skills = Skill.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'skills': user_skills})





def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})

def exchange_request(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            exch = form.save(commit=False)
            exch.from_user = request.user
            exch.to_user = exch.skill.user
            exch.save()
            return redirect('dashboard')
    else:
        form = ExchangeForm()
    return render(request, 'exchange.html', {'form': form})

def chat(request):
    messages = Message.objects.filter(receiver=request.user) | Message.objects.filter(sender=request.user)
    form = MessageForm()
    return render(request, 'chat.html', {'messages': messages, 'form': form})

def calendar_view(request):
    return render(request, 'calendar.html')

def get_events(request):
    appointments = Appointment.objects.all()
    events = [{
        "title": f"{a.user.username} ↔ {a.with_user.username}",
        "start": a.start_time.isoformat(),
        "end": a.end_time.isoformat(),
    } for a in appointments]
    return JsonResponse(events, safe=False)

@csrf_exempt
def add_event(request):
    if request.method == "POST":
        data = json.loads(request.body)
        skill_id = data.get('skill')
        with_user_id = data.get('with_user')
        start = parse_datetime(data.get('start'))
        end = parse_datetime(data.get('end'))

        Appointment.objects.create(
            user=request.user,
            skill_id=skill_id,
            with_user_id=with_user_id,
            start_time=start,
            end_time=end
        )
        return JsonResponse({"status": "success"})


def chat_room(request, room_name):
    return render(request, 'chat.html', {
        'room_name': room_name
        })
        




@csrf_protect
def test(request):
    if request.method == 'POST':
        return HttpResponse("Success")
    return render(request, 'test.html')



