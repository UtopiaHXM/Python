# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TMalware(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    date_update = models.DateTimeField(db_column='Date_update', blank=True, null=True)  # Field name made lowercase.
    domain = models.TextField(db_column='Domain', blank=True)  # Field name made lowercase.
    ip = models.TextField(db_column='IP', blank=True)  # Field name made lowercase.
    reverse_lookup = models.TextField(db_column='Reverse_Lookup', blank=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True)  # Field name made lowercase.
    registrant = models.TextField(db_column='Registrant', blank=True)  # Field name made lowercase.
    asn = models.TextField(db_column='ASN', blank=True)  # Field name made lowercase.
    country = models.TextField(db_column='Country', blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 't_malware'


class TPhish(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    phish_id = models.CharField(max_length=20, blank=True)
    url = models.TextField(blank=True)
    phish_detail_url = models.TextField(blank=True)
    submission_time = models.DateTimeField()
    verified = models.TextField(blank=True)
    verification_time = models.DateTimeField()
    online = models.TextField(blank=True)
    target = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 't_phish'


class TSafebrowsing(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    url = models.TextField(blank=True)
    type = models.CharField(max_length=20, blank=True)

    class Meta:
        managed = False
        db_table = 't_safebrowsing'


class TVirusapi(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    scan_id = models.CharField(max_length=100, blank=True)
    response_code = models.IntegerField(blank=True, null=True)
    scan_date = models.DateTimeField(blank=True, null=True)
    url = models.TextField(blank=True)
    positives = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)
    scans = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 't_virusapi'


class TWhois(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    domain_name = models.TextField(db_column='Domain Name', blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrar = models.CharField(db_column='Registrar', max_length=100, blank=True)  # Field name made lowercase.
    registrar_whois_server = models.CharField(db_column='Registrar WHOIS Server', max_length=100, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_field = models.DateTimeField(db_column='\u66f4\u65b0\u65f6\u95f4', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    registrar_registration_field = models.DateTimeField(db_column='Registrar Registration \u8fc7\u671f\u65f6\u95f4', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    registrant_city = models.CharField(db_column='Registrant City', max_length=40, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_name = models.CharField(db_column='Registrant Name', max_length=40, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_organization = models.CharField(db_column='Registrant Organization', max_length=100, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_state_province = models.CharField(db_column='Registrant State/Province', max_length=40, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_postal_code = models.CharField(db_column='Registrant Postal Code', max_length=20, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_country = models.CharField(db_column='Registrant Country', max_length=40, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_phone = models.CharField(db_column='Registrant Phone', max_length=20, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    registrant_email = models.CharField(db_column='Registrant Email', max_length=40, blank=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 't_whois'


class TZeustracker(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    info_type = models.TextField(blank=True)
    bad_content = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        managed = False
        db_table = 't_zeustracker'
