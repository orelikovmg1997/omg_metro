import sqlite3

from django.shortcuts import render_to_response, redirect

from mach.services import ServiceLayer
from machinist.settings import SQLITE


def schedule_view(request):
    connection = sqlite3.connect(SQLITE)
    context = {}
    cur = connection.cursor()
    schedules = ServiceLayer.get_all_schedules(connection=cur)
    context['schedules'] = list(schedules)
    cur.close()
    connection.close()
    return render_to_response('html/base.html', context)


def message_view(request):
    context = {}
    connection = sqlite3.connect(SQLITE)
    cur = connection.cursor()

    messages = list(ServiceLayer.get_all_messages(connection=cur))
    context['messages'] = messages

    cur.close()
    connection.close()
    return render_to_response('html/message.html', context)


def change_list_view(request):
    connection = sqlite3.connect(SQLITE, isolation_level=None)
    cur = connection.cursor()

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
        cur.close()
        connection.close()
        return render_to_response('html/change.html', {'options': options, 'places': points})

    other = request.POST.get('other')
    text = other or request.POST.get('text')
    sender = request.POST.get('user')
    place = request.POST.get('place')
    ServiceLayer.create_new_message(sender, text, place, connection=cur)

    cur.close()
    connection.close()
    return redirect('messages')


def emergency_list_view(request):
    connection = sqlite3.connect(SQLITE, isolation_level=None)
    cur = connection.cursor()

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
        cur.close()
        connection.close()
        return render_to_response('html/emergency.html',
                                  {'options': options, 'places': points})

    other = request.POST.get('other')
    text = other or request.POST.get('text')
    sender = request.POST.get('user')
    place = request.POST.get('place')
    ServiceLayer.create_new_message(sender, text, place, connection=cur)

    cur.close()
    connection.close()
    return redirect('messages')
