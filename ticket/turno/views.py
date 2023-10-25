from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Municipio, Nivel, Asunto, Turno, Estatus, User, Qr

import http.client
import json

from django.template.loader import get_template
from xhtml2pdf import pisa

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "turno/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "turno/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def registrar(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "turno/registrar.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "turno/registrar.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "turno/registrar.html")


@login_required
def index(request):
    municipios = Municipio.objects.all()
    context = {
        'municipios': municipios
    }
    return render(request, 'turno/index.html', context)


@login_required
def crear(request, id_muni, message=''):
    if request.method == 'POST':
        try:
            print('entro trycatch')
            curp = request.POST["curp"]
            nombres = request.POST["nombres"]
            paterno = request.POST["paterno"]
            materno = request.POST["materno"]
            telefono = request.POST["telefono"]
            celular = request.POST["celular"]
            correo = request.POST["correo"]
            nivel_form = request.POST["nivel"]
            asunto_form = request.POST["asunto"]

            print('obtuvo todos los post CREAR')

            nivel = Nivel.objects.get(nivel=nivel_form)
            asunto = Asunto.objects.get(asunto=asunto_form)
            municipio = Municipio.objects.get(id=id_muni)
            status = Estatus.objects.get(estatus='Pendiente')

            # retorna la ultima instancia de turno del municipio especificado en el forms
            try:
                ultimo_turno = Turno.objects.filter(
                    municipio_id=municipio.id).latest('turno')
                print(ultimo_turno)
                if ultimo_turno.turno < 1:
                    turno = 1
                else:
                    turno = ultimo_turno.turno + 1
            except:
                turno = 1

            Turno.objects.create(curp=curp, nombres=nombres, paterno=paterno,
                                 materno=materno, telefono=telefono, celular=celular,
                                 correo=correo, nivel=nivel, asunto=asunto,
                                 municipio=municipio, status=status, turno=turno)

            mensaje = "Turno creado correctamente"
            return HttpResponseRedirect(reverse("crear", args=(id_muni, mensaje, )))
        except:
            print('excepcion')
            mensaje = "Revisa todos los campos con cuidado"
            return HttpResponseRedirect(reverse("crear", args=(id_muni, mensaje,)))

    else:
        if message == '':
            mensaje = None

        # print(mensaje)
        niveles = Nivel.objects.all()
        asuntos = Asunto.objects.all()
        municipio = Municipio.objects.get(id=id_muni)
        context = {
            "niveles": niveles,
            "asuntos": asuntos,
            "municipio": municipio,
            "id_muni": id_muni
        }
        # print(municipio)
        return render(request, 'turno/crear.html', context)


@login_required
def turnos(request, id_muni):
    turnos = Turno.objects.filter(municipio_id=id_muni)
    municipio = Municipio.objects.get(id=id_muni)
    return render(request, 'turno/turnos.html', {'turnos': turnos, 'municipio': municipio})


@login_required
def detalles(request, id_turno):
    turno = Turno.objects.get(id=id_turno)
    return render(request, 'turno/detalles.html', {'turno': turno})


@login_required
def editar(request, id_turno):
    turno_edit = Turno.objects.get(id=id_turno)

    if request.method == 'POST':
        curp = request.POST["curp"]
        nombres = request.POST["nombres"]
        paterno = request.POST["paterno"]
        materno = request.POST["materno"]
        telefono = request.POST["telefono"]
        celular = request.POST["celular"]
        correo = request.POST["correo"]
        nivel_form = request.POST["nivel"]
        asunto_form = request.POST["asunto"]
        municipio_form = request.POST["municipio"]

        print('obtuvo todos los post EDITAR')

        nivel = Nivel.objects.get(nivel=nivel_form)
        asunto = Asunto.objects.get(asunto=asunto_form)
        municipio = Municipio.objects.get(municipio=municipio_form)
        status = Estatus.objects.get(estatus='Pendiente')

        # retorna la ultima instancia de turno del municipio especificado en el forms
        try:
            ultimo_turno = Turno.objects.filter(
                municipio_id=municipio.id).latest('turno')
            print(ultimo_turno)
            if ultimo_turno.turno < 1:
                turno_turno = 1
            else:
                turno_turno = ultimo_turno.turno + 1
        except:
            turno_turno = 1

        print(turno_edit)
        turno_edit.curp = curp
        turno_edit.nombres = nombres
        turno_edit.paterno = paterno
        turno_edit.materno = materno
        turno_edit.telefono = telefono
        turno_edit.celular = celular
        turno_edit.correo = correo
        turno_edit.nivel = nivel
        turno_edit.asunto = asunto
        turno_edit.municipio = municipio
        turno_edit.status = status
        turno_edit.turno = turno_turno
        turno_edit.save()
        return HttpResponseRedirect(reverse('detalles', args=(id_turno, )))

    else:
        niveles = Nivel.objects.all()
        asuntos = Asunto.objects.all()
        municipios = Municipio.objects.all()
        status = Estatus.objects.all()

        context = {
            'turno': turno_edit,
            'niveles': niveles,
            'asuntos': asuntos,
            'municipios': municipios,
            'status': status
        }
        return render(request, 'turno/editar.html', context)

@login_required
def dashboard(request, id_muni=''):

    if id_muni == '':
        r_id = Estatus.objects.get(estatus='Resuelto')
        p_id = Estatus.objects.get(estatus='Pendiente')

        resueltos = Turno.objects.filter(status=r_id)
        pendientes = Turno.objects.filter(status=p_id)
        context = {
            'resueltos': resueltos,
            'pendientes': pendientes
        }
        return render(request, 'turno/dashboard.html', context)
    else:
        r_id = Estatus.objects.get(estatus='Resuelto')
        p_id = Estatus.objects.get(estatus='Pendiente')
        muni = Municipio.objects.get(id=id_muni)

        resueltos = Turno.objects.filter(municipio=muni, status=r_id)
        pendientes = Turno.objects.filter(municipio=muni, status=p_id)
        context = {
            'resueltos': resueltos,
            'pendientes': pendientes,
            'municipio': muni
        }
        return render(request, 'turno/dashboard.html', context)


@login_required
def pronostico(request, id_muni):
    conn = http.client.HTTPSConnection("smn.conagua.gob.mx")
    payload = ''
    headers = {
        'Cookie': 'HttpOnly; incap_ses_1060_2707069=kOFKauFEU3qSlTQ/cOC1DqEgNmUAAAAArXKuqPKRQJDs01ofUMV4DA==; nlbi_2707069=gK6GQOB4dgY7atBBByjSLwAAAAAAIy2r/apYUL53pOAfn05a; visid_incap_2707069=95pIspjARQe43oXdaxxxc6EgNmUAAAAAQUIPAAAAAAD2inUfrrApu2EKd/HFtn2u'
    }
    url = f"https://smn.conagua.gob.mx/tools/PHP/pronostico_municipios_grafico/controlador/getDataJson2String.php?edo=5&mun={id_muni}"
    conn.request(f"GET", url, payload, headers)
    res = conn.getresponse()
    data = res.read()

    data = json.loads(data)
    # for item in data[1]:
    #     print(item)

    nes = data[1]['nes']
    nmun = data[1]['nmun']
    tmax = data[1]['tmax']
    tmin = data[1]['tmin']
    desciel = data[1]['desciel']
    probprec = data[1]['probprec']


    municipio = Municipio.objects.get(id=id_muni)
    context = {
        'nes': nes,
        'nmun': nmun,
        'tmax': tmax,
        'tmin': tmin,
        'desciel': desciel,
        'probprec': probprec,
        'municipio': municipio
    }
    return render(request, 'turno/clima.html', context)

@login_required
def renderpdf(request, turno_id):
    template_path = 'turno/pdf.html'

    qr = Qr.objects.get(id=1)
    turno = Turno.objects.get(id=turno_id)
    context = {'turno': turno, 'qr':qr}

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attatchment; filename="turno.pdf"'
    response['Content-Disposition'] = 'filename="turno.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Tuvimos algunos problemas <pre>' + html + '</pre>')
    return response