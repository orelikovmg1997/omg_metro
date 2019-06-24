import sqlite3
from contextlib import closing

from django.shortcuts import render_to_response, redirect

from mach.services import ServiceLayer
from machinist.settings import SQLITE


def login_required(func):
    def wrapped(request, *args, **kwargs):
        if request.session.get('user_id') is None:
            return redirect('login')

        return func(request, *args, **kwargs)

    return wrapped


def database_connection(func):
    def wrapped(request, *args, **kwargs):
        with closing(sqlite3.connect(SQLITE)) as connection:
            with closing(connection.cursor()) as cur:
                return func(request, *args, cur=cur, **kwargs)

    return wrapped


@database_connection
def login_view(request, *args, cur=None, **kwargs):
    user_id = request.session.get('user_id')
    if user_id is not None:
        return redirect('index')

    context = {
        'username': '',
        'password': '',
    }

    if request.method == "POST":
        context['username'] = request.POST.get('username')
        context['password'] = request.POST.get('password')
        user = ServiceLayer.get_by_username(context['username'], cur)
        if user.password == context['password']:
            request.session['user_id'] = user.id
            return redirect('index')

    return render_to_response('html/login.html', context)


@database_connection
def logout_view(request, *args, **kwargs):
    request.session.pop('user_id')
    return redirect('login')


@login_required
@database_connection
def schedule_view(request, cur=None):
    schedules = ServiceLayer.get_all_schedules(connection=cur)
    context = {
        'schedules': list(schedules)
    }

    return render_to_response('html/base.html', context)


@login_required
@database_connection
def message_view(request, cur=None):
    messages = list(ServiceLayer.get_all_messages(connection=cur))
    context = {
        'messages': messages
    }
    return render_to_response('html/message.html', context)


@login_required
@database_connection
def change_list_view(request, cur=None):

    options = [
        'Плохое самочувствие',
        'Травма',
        'Нервный срыв',
        'Накопилось',
        'Проголоcовать за Путина',
        'Ой, все!',
    ]

    points = list(ServiceLayer.get_all_places(connection=cur))

    if request.method == 'GET':
        return render_to_response('html/change.html', {'options': options, 'places': points})

    other = request.POST.get('other')
    text = other or request.POST.get('text')
    sender = request.POST.get('user')
    place = request.POST.get('place')
    ServiceLayer.create_new_message(sender, text, place, connection=cur)

    return redirect('messages')


@login_required
@database_connection
def emergency_list_view(request, cur=None):
    options = [
        'Состав вышел из строя',
        'Падение напряжения',
        'Состав сошел с рельсов',
        'Человек на рельсах',
        'Закрытый',
        'Террористическая атака',
        'Несанкционированный митинг Алексея Навэльного'
    ]

    points = list(ServiceLayer.get_all_places(connection=cur))

    if request.method == 'GET':
        return render_to_response('html/emergency.html',
                                  {'options': options, 'places': points})

    other = request.POST.get('other')
    text = other or request.POST.get('text')
    sender = request.POST.get('user')
    place = request.POST.get('place')
    ServiceLayer.create_new_message(sender, text, place, connection=cur)
    return redirect('messages')
