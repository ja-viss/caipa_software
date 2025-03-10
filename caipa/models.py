from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class areas(models.Model):
    name_area = models.TextField()
    informe_area = models.TextField()

class student_caipa(models.Model):
    ced_stu = models.TextField()
    name_stu = models.TextField()
    lastna_stu = models.TextField()
    age_stu = models.TextField()
    direcc_stu = models.TextField()
    fech_nac = models.DateTimeField(null = True, blank = True)
    cami_stu = models.TextField(blank = True)
    pan_stu = models.TextField(blank = True)
    zapa_stu = models.TextField(blank = True)
    birth_stu = models.TextField(blank = True)
    state_stu = models.TextField(blank = True)
    natio_stu = models.TextField(blank = True)
    country_stu = models.TextField(blank = True)
    gender = models.TextField(blank = True)
    pes_stu = models.TextField(blank = True)
    grp_sng_stu = models.TextField(blank = True)
    email_stu = models.TextField(blank = True)
    area = models.ManyToManyField(areas, through='areaestudiante')
    
class repre_caipa(models.Model):
    ced_repre = models.TextField()
    name_repre = models.TextField()
    lastna_repre = models.TextField()
    age_repre = models.TextField(blank = True)
    number_repre = models.TextField(blank = True)
    phone_repre = models.TextField()
    email_repre = models.TextField()
    direcc_repre = models.TextField()
    id_estu = models.ForeignKey(student_caipa, on_delete=models.CASCADE)


class teacher_caipa(models.Model):
    ced_tea = models.TextField()
    name_tea = models.TextField()
    lastna_tea = models.TextField()
    age_tea = models.TextField(blank = True)
    phone_tea = models.TextField()
    email_tea = models.TextField()
    direcc_tea = models.TextField()
    id_estu = models.ForeignKey(student_caipa, on_delete=models.CASCADE, null=True)
    area = models.ManyToManyField(areas, through='areaestudiante')

class admin_caipa(models.Model):
    ced_admin = models.TextField()
    name_admin = models.TextField()
    lastna_admin = models.TextField()
    age_admin = models.TextField(blank = True)
    phone_admin = models.TextField()
    email_admin = models.TextField()
    direcc_admin = models.TextField()

class direc_caipa(models.Model):
    ced_direc = models.TextField()
    name_direc = models.TextField()
    lastna_direc = models.TextField()
    phone_direc = models.TextField()
    email_direc = models.TextField()
    direcc_direc = models.TextField()

class user_type(models.Model):
    ced = models.TextField()
    email = models.TextField()
    rol = models.TextField()

class user_loggin(models.Model):
    ced = models.TextField()
    email = models.TextField()
    password = models.TextField()
    status = models.TextField()


class areaestudiante(models.Model):
    area = models.ForeignKey(areas, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(teacher_caipa, on_delete=models.CASCADE)
    docente = models.ForeignKey(student_caipa, on_delete=models.CASCADE)



