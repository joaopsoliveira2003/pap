from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from website.models import *
from website.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from PIL import Image


def year():
    if datetime.now().year > 2020:
        return f'2020 - {datetime.now().year}'
    else:
        return '2020'


def index(request, *args, **kwargs):
    error = -1
    if request.method == 'POST':
        form = Contactform(request.POST)
        if form.is_valid():
            error = 1
            contactmodel(name=request.POST["name"], email=request.POST["email"], subject=request.POST["subject"],
                         message=request.POST["message"]).save()
            try:
                send_mail("Nucleus - Pedido de Contacto Enviado",
                          f"Olá {request.POST['name']}, o seu pedido de contacto "
                          f"foi enviado com sucesso!\n\nAssim que um técnico "
                          f"responder, receberá um email com a "
                          f"resposta!\n\nObrigado, a equipa Nucleus.",
                          "noreply@nucleus.pt",
                          [form.cleaned_data["email"]], fail_silently=True)
            except:
                pass
        else:
            error = 2
    else:
        form = Contactform()
    return render(request, 'index.html', {
        'year': year(),
        'form': form,
        'error': error
    })


@login_required
def dashboard(request):
    active_contacts = contactmodel.objects.filter(status='unread').count()
    closed_contacts = contactmodel.objects.filter(status='read').count()
    if request.user.groups.filter(name="user"):
        active_tickets = ticketmodel.objects.filter(status='open', user=request.user).count()
        closed_tickets = ticketmodel.objects.filter(status='closed', user=request.user).count()
        tickets = ticketmodel.objects.filter(user=request.user)
        data = [ticketmodel.objects.filter(status='open', user=request.user).count(),
                ticketmodel.objects.filter(status='closed', user=request.user).count()]
        permission = False
    else:
        active_tickets = ticketmodel.objects.filter(status='open').count()
        closed_tickets = ticketmodel.objects.filter(status='closed').count()
        tickets = ticketmodel.objects.all()
        data = [ticketmodel.objects.filter(status='open').count(),
                ticketmodel.objects.filter(status='closed').count()]
        permission = True
    return render(request, 'dashboard.html', {
        'title': 'Painel Principal',
        'active_tickets': active_tickets,
        'closed_tickets': closed_tickets,
        'active_contacts': active_contacts,
        'closed_contacts': closed_contacts,
        'tickets': tickets,
        'label': 'Tickets',
        'labels': ["Por Atender", "Atendidos"],
        'data': data,
        'permission': permission
    })


def ticket(request):
    if request.method == 'POST':
        if "id" in request.POST:
            if request.POST["id"] != "":
                temp = ticketmodel.objects.get(id=request.POST["id"])
                temp.technician = request.user
                if temp.status != request.POST["status"]:
                    temp.status = request.POST["status"]
                if temp.response != request.POST["response"]:
                    temp.response = request.POST["response"]
                    try:
                        send_mail("Nucleus - Pedido de Assistência Respondido",
                                  f"Olá {temp.user.username}, o seu pedido de assistência foi respondido!\n\nVerifique o "
                                  f"estado do mesmo através da nossa página!\n\nObrigado, a equipa Nucleus.",
                                  "noreply@nucleus.pt",
                                  [temp.user.email], fail_silently=True)
                    except:
                        pass
                temp.save()
        else:
            form = Ticketform(request.POST)
            if form.is_valid():
                ticketmodel(subject=request.POST["subject"], gravity=request.POST["gravity"],
                            message=request.POST["message"], user=request.user).save()


@login_required
def ticketlist(request):
    ticket(request)
    if request.user.groups.filter(name="user"):
        tickets = ticketmodel.objects.filter(user=request.user, status='open')
        data = [ticketmodel.objects.filter(status='open', user=request.user).count(),
                ticketmodel.objects.filter(status='closed', user=request.user).count()]
        permission = False
    else:
        tickets = ticketmodel.objects.filter(status='open')
        data = [ticketmodel.objects.filter(status='open').count(),
                ticketmodel.objects.filter(status='closed').count()]
        permission = True
    return render(request, 'ticket.html', {
        'title': 'Pedidos de Assistência',
        'breadcrumb_title': 'Pedidos de Assistência',
        'tickets': Paginator(tickets, 10, 3).get_page(request.GET.get('page')),
        'count': tickets.count(),
        'label': 'Tickets',
        'labels': ["Por Atender", "Atendidos"],
        'data': data,
        'permission': permission

    })


@login_required
def ticketarchive(request):
    ticket(request)
    if request.user.groups.filter(name="user"):
        tickets = ticketmodel.objects.filter(user=request.user, status='closed')
        data = [ticketmodel.objects.filter(status='open', user=request.user).count(),
                ticketmodel.objects.filter(status='closed', user=request.user).count()]
        permission = False
    else:
        tickets = ticketmodel.objects.filter(status='closed')
        data = [ticketmodel.objects.filter(status='open').count(),
                ticketmodel.objects.filter(status='closed').count()]
        permission = True
    return render(request, 'ticket.html', {
        'title': 'Arquivo de Pedidos de Assistência',
        'breadcrumb_title': 'Arquivo de Pedidos de Assistência',
        'tickets': Paginator(tickets.order_by('-id'), 10, 3).get_page(request.GET.get('page')),
        'count': tickets.count(),
        'label': 'Tickets',
        'labels': ["Por Atender", "Atendidos"],
        'data': data,
        'permission': permission
    })


@login_required
def extension(request):
    errors = -1
    if request.method == "POST":
        form = Ticketform(request.POST)
        if form.is_valid():
            ticketmodel(subject=request.POST["subject"], gravity=request.POST["gravity"],
                        message=request.POST["message"], user=request.user).save()
            errors = 0
        else:
            errors = 1
    return render(request, "extension.html", {'errors': errors})


def contact(request):
    if request.method == 'POST':
        if "id" in request.POST:
            if request.POST["id"] != "":
                temp = contactmodel.objects.get(id=request.POST["id"])
                temp.technician = request.user
                if temp.status != request.POST["status"]:
                    temp.status = request.POST["status"]
                if temp.response != request.POST["response"]:
                    temp.response = request.POST["response"]
                    try:
                        send_mail("Nucleus - Pedido de Contacto Respondido",
                                  f"Olá {temp.name}, o seu pedido de contacto foi respondido!\n\nResposta: {request.POST['response']}\n\nObrigado, a equipa Nucleus.",
                                  "noreply@nucleus.pt",
                                  [temp.email], fail_silently=True)
                    except:
                        pass
                temp.save()


@login_required
def contactlist(request):
    contact(request)
    contacts = contactmodel.objects.filter(status='unread')
    data = [contactmodel.objects.filter(status='unread').count(),
            contactmodel.objects.filter(status='read').count()]
    return render(request, 'contact.html', {
        'title': 'Pedidos de Contacto',
        'breadcrumb_title': 'Pedidos de Contacto',
        'contacts': Paginator(contacts, 10, 3).get_page(request.GET.get('page')),
        'count': contactmodel.objects.filter(status='unread').count(),
        'data': data,
        'label': 'Contactos',
        'labels': ["Por Ler", "Lidos"],
        'permission': True
    })


@login_required
def contactarchive(request):
    contact(request)
    contacts = contactmodel.objects.filter(status='read')
    data = [contactmodel.objects.filter(status='unread').count(),
            contactmodel.objects.filter(status='read').count()]
    return render(request, 'contact.html', {
        'title': 'Arquivo de Contactos',
        'breadcrumb_title': 'Arquivo de Contactos',
        'contacts': Paginator(contacts.order_by('-id'), 10, 3).get_page(request.GET.get('page')),
        'count': contactmodel.objects.filter(status='read').count(),
        'data': data,
        'label': 'Contactos',
        'labels': ["Por Ler", "Lidos"],
        'permission': True
    })


@login_required
def files(request):
    if request.method == "POST":
        if "id" in request.POST:
            filemodel.objects.get(id=request.POST["id"]).delete()
        else:
            form = Fileform(request.POST, request.FILES)
            if form.is_valid():
                temp = filemodel(name=request.POST["name"], description=request.POST["description"])
                temp.file = request.FILES["file"]
                temp.save()
    if request.user.groups.filter(name="user"):
        tickets = ticketmodel.objects.filter(user=request.user, status='closed')
        data = [ticketmodel.objects.filter(status='open', user=request.user).count(),
                ticketmodel.objects.filter(status='closed', user=request.user).count()]
        permission = False
    else:
        tickets = ticketmodel.objects.filter(status='closed')
        data = [ticketmodel.objects.filter(status='open').count(),
                ticketmodel.objects.filter(status='closed').count()]
        permission = True
    return render(request, 'files.html', {
        'title': 'Ficheiros',
        'breadcrumb_title': 'Ficheiros',
        'files': filemodel.objects.all(),
        'tickets': tickets,
        'data': data,
        'label': 'Tickets',
        'labels': ["Por Atender", "Atendidos"],
        'permission': permission
    })


@login_required
def profile(request, username):
    if request.method == "POST":
        if request.POST['first_name'] != "" and request.POST['last_name'] != "" and request.POST['email'] != "" and \
                request.POST['bio'] != "":
            temp = request.user
            if "image" in request.FILES != "":
                try:
                    Image.open(request.FILES["image"])
                    temp.profile.image = request.FILES["image"]
                except:
                    pass
            temp.first_name = request.POST['first_name']
            temp.last_name = request.POST['last_name']
            temp.email = request.POST['email']
            temp.profile.bio = request.POST['bio']
            temp.save()
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('dashboard')
    if request.user.username == username:
        usertype = True
    else:
        usertype = False
    if User.objects.get(username=username).groups.filter(name="user").exists():
        tickets = ticketmodel.objects.filter(user=request.user)
    else:
        tickets = ticketmodel.objects.filter(technician=request.user)
    if request.user.groups.filter(name="user"):
        permission = False
    else:
        permission = True
    return render(request, 'profile.html', {
        'title': 'Perfil',
        'breadcrumb_title': 'Perfil',
        'tickets': tickets,
        'permission': permission,
        'usertype': usertype,
        'user': user
    })


@login_required
def register(request):
    if request.user.groups.filter(name="admin"):
        form = UserCreationForm()
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
        return render(request, "registration/register.html", {
            "form": form
        })
    else:
        return redirect('dashboard')


@login_required
def admin(request):
    if request.method == "POST":
        if "username" in request.POST and "group" in request.POST:
            try:
                temp = User.objects.get(username=request.POST["username"])
                temp.groups.clear()
                temp.groups.add(Group.objects.get(name=request.POST["group"]))
                temp.save()
            except:
                pass
    return redirect("dashboard")
