from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from xhtml2pdf import pisa 
from .models import student_caipa, repre_caipa, admin_caipa, teacher_caipa, direc_caipa, user_type, user_loggin
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from io import BytesIO
import smtplib
import getpass
import time
from datetime import datetime
# Create your views here.

def index(request):
    return render(request, 'caipa/index.html')

def agender(request):
    return render(request, 'caipa/agender_cite.html')

def register_stu(request):
    return render(request, 'caipa/register_stu.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'caipa/index.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['email_repre'],
                    password=request.POST['password1'])
                login(request, user)

                loggin = user_loggin(
                    ced=request.POST['id_repre'],
                    email=request.POST['email_repre'],
                    password=request.POST['password1'],
                    status= 'Activo'
                    )

                loggin.save()

                student = student_caipa(
                    ced_stu=request.POST['id_stu'],
                    name_stu=request.POST['name_stu'],
                    lastna_stu=request.POST['last_stu'],
                    age_stu=request.POST['age_stu'],
                    natio_stu=request.POST['natio_stu']
                )

                student.save()

                student2 = student_caipa.objects.get(pk=student.id)
                print(student)

                repre = repre_caipa(
                    ced_repre=request.POST['id_repre'],
                    name_repre=request.POST['name_repre'],
                    lastna_repre=request.POST['lastna_repre'],
                    phone_repre=request.POST['number_phone'],
                    direcc_repre=request.POST['direc'],
                    email_repre=request.POST['email_repre'],
                    id_estu = student2)

                repre.save()

                message = "Registro exitoso. ¡Bienvenido(a)!"
                notification_type = "success"

            except IntegrityError as e:
                message = f"Error al registrarse: {e}"
                notification_type = "error"

            return redirect('/complete')

        else:
            message = "Las contraseñas no coinciden."
            notification_type = "error"
            return redirect('caipa/index.html', {
                'message': message,
                'notification_type': notification_type,
            })


def create_estudiante2(request):
    estu = student_caipa(
        ced_stu=request.POST['id'],
        name_stu=request.POST['nombre'],
        lastna_stu=request.POST['apellido'],
        age_stu=request.POST['edad'],
        phone_stu=request.POST['tel'])

    estu.save()
    return redirect('/profile')

def sigin(request):
    print("metodo sigin")
    if request.method == 'GET':
        print('metodo get')
        return render(request, 'caipa/index.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST
                            ['password'])
        if user == None:
            return render(request, 'caipa/index.html', {
                'error': 'Username or password is incorrect'
            })
            print("error al iniciar")
        else:
            login(request, user)
            print("inicio correcto", user)
            return redirect('/profile') 


def profile(request):
    if request.user is None:
        print('none user')
        return render(request, 'caipa/index.html')

    else:
        print('user type complete', request.user)
        user_type_obj = user_type.objects.get(email=request.user) 

        if user_type_obj.rol == 'Docente':
            data_user = teacher_caipa.objects.get(email_tea = request.user)
            router = 'caipa/profile_teacher.html'

        elif user_type_obj.rol == 'Administrativo':
            data_user = admin_caipa.objects.get(email_admin = request.user)
            router = 'caipa/profile_admin.html'  

        elif user_type_obj.rol == 'Directivo':
            data_user = direc_caipa.objects.get(email_direc = request.user)
            router = 'caipa/profile_direct.html'  

        elif user_type_obj.rol == 'Representante':
            data_user = repre_caipa.objects.get(email_repre = request.user)
            stu = data_user.id_estu_id
            student = student_caipa.objects.get(id = stu)
            router = 'caipa/profile_repre.html' 
            return render(request, router, {"data": data_user, "user": user_type_obj, "estudiante": student})

        return render(request, router, {"data": data_user, "user": user_type_obj})


def delete(request, ced_id):
    estu = student_caipa.objects.get(ced_stu=ced_id)
    estu.delete()
    return redirect('/profile')


def create(request):
    return render(request, 'caipa/create.html')


def search(request):
    user_repre = repre_caipa.objects.get(email_repre=request.user) 
    id_student = user_repre.id_estu.id
    print(id_student)
    data_student = student_caipa.objects.get(id=id_student)     
    return render(request, 'caipa/complete.html', {"data": data_student, "repre": user_repre})

def search_pdf(request):
    user_repre = repre_caipa.objects.get(email_repre=request.user) 
    id_student = user_repre.id_estu.id
    print(id_student)
    data_student = student_caipa.objects.get(id=id_student)   
    return render(request, 'caipa/pdf_stu.html', {"data": data_student, "repre": user_repre})


def update(request):

    ced_id = request.POST['ced_stu']
    estu = student_caipa.objects.get(ced_stu=ced_id)
    estu.name_stu = request.POST['name_stu']
    estu.lastna_stu = request.POST['lastna_stu']
    estu.age_stu = request.POST['age_stu']
    estu.direcc_stu = request.POST['direcc_stu']
    fecha_nacimiento = datetime.strptime(request.POST['fech_nac'], '%Y-%m-%d')
    print(fecha_nacimiento)
    estu.fech_nac = fecha_nacimiento
    estu.cami_stu = request.POST['cami_stu']
    estu.pan_stu = request.POST['pan_stu']
    estu.zapa_stu = request.POST['zapa_stu']
    estu.birth_stu = request.POST['birth_stu']
    estu.state_stu = request.POST['state_stu']
    estu.zapa_stu = request.POST['zapa_stu']
    estu.pes_stu = request.POST['pes_stu']
    estu.email_stu = request.POST['email_stu']
    estu.gender = request.POST['gender']
    estu.grp_sng_stu = request.POST['grp_sng_stu']


    estu.save()

    ced_id = request.POST['ced_repre']
    repre = repre_caipa.objects.get(ced_repre=ced_id)
    repre.name_repre=request.POST['name_repre']
    repre.lastna_repre=request.POST['lastna_repre']
    repre.number_repre=request.POST['number_repre']
    repre.phone_repre=request.POST['phone_repre']
    repre.direcc_repre=request.POST['direcc_repre']
    repre.email_repre=request.POST['email_repre']
    repre.age_repre=request.POST['age_repre']


    repre.save()

    user = user_type(
        ced = ced_id,
        email = request.POST['email_repre'],
        rol = "Representante"
    )

    user.save()

    return redirect('/pdf_stu')



def validate(request):

    try:
        request.method != 'GET'
    except request.POST['password1'] != request.POST['password2']:
        message = "Las contraseñas no coinciden."
        notification_type = "error"
        return render(request, 'caipa/index.html', {
            'message': message,
            'notification_type': notification_type,
        })

    try:
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password1']
        )
        login(request, user)  # Autentifica después de la creación exitosa
        
        user_typ = user_type(
            ced = request.POST['ced_id'],
            email = request.POST['username'],
            rol = request.POST['type_user']

        )

        user_typ.save()

        ced_ide = request.POST.get('ced_id')

        user_type_obj = user_type.objects.get(ced=ced_ide)

        # Crea una instancia de perfil de usuario según el tipo_usuario
        if user_type_obj.rol == 'Docente':
            profile_obj = teacher_caipa.objects.create(
                ced_tea=request.POST['ced_id'],
                name_tea=request.POST['name'],
                lastna_tea=request.POST['lastname'],
                email_tea=request.POST['username']
            )
        elif user_type_obj.rol == 'Administrativo':
            profile_obj = admin_caipa.objects.create(
                ced_admin=request.POST['ced_id'],
                name_admin=request.POST['name'],
                lastna_admin=request.POST['lastname'],
                email_admin=request.POST['username']
            )
        elif user_type_obj.rol == 'Directivo':
            profile_obj = direc_caipa.objects.create(
                ced_direc=request.POST['ced_id'],
                name_direc=request.POST['name'],
                lastna_direc=request.POST['lastname'],
                email_direc=request.POST['username']
            )

        message = "¡Registro exitoso!"
        notification_type = "success"
        house = 'caipa/profile.html'
        context = {'tipo_usuario': user_type_obj.rol, 'message': message, 'notification_type': notification_type}
        return render(request, house, context)

    except IntegrityError as e:
        message = f"Error al registrarse: {e}"
        notification_type = "error"
        return render(request, 'caipa/index.html', {
            'message': message,
            'notification_type': notification_type,
        })

from django.http import HttpResponse
from django.template.loader import get_template
import io
from xhtml2pdf import pisa  # Instalar xhtml2pdf: pip install xhtml2pdf

def render_to_pdf(request):
    
    # Recuperar información del representante y estudiante
    user_repre = repre_caipa.objects.get(email_repre=request.user)
    id_student = user_repre.id_estu.id
    data_student = student_caipa.objects.get(id=id_student)

    # Preparar el contexto para la plantilla
    data = {
        "data": data_student,
        "repre": user_repre
    }

    # Renderizar la plantilla HTML
    template = get_template('caipa/planilla_new.html')
    html = template.render(data)
    result = io.BytesIO()

    # Opciones para xhtml2pdf (intentar reconocer estilos Bootstrap)
    options = {
        'encoding': "ISO-8859-1",
        'media': "screen",  # Cambiar a "screen" para aplicar estilos de pantalla
        'smart_quotes': True,
        'x_html': True,
        'print_friendly': True,
        'no_breaks': True,
    }

    # Generar el PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, options=options)

    # Comprobar errores y devolver el PDF
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return None

