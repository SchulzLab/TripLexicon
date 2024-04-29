# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
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


class Dna(models.Model):
    dnaid = models.TextField(db_column='DNAID', primary_key=True, blank=True, null=False)   
    featureid = models.TextField(db_column='FeatureID', blank=True, null=True)   
    type = models.TextField(db_column='Type', blank=True, null=True)   
    geneid = models.TextField(db_column='GeneID', blank=True, null=True)   
    genesymbol = models.TextField(db_column='GeneSymbol', blank=True, null=True)   
    chr = models.TextField(db_column='Chr', blank=True, null=True)   
    start = models.TextField(db_column='Start', blank=True, null=True)   
    end = models.TextField(db_column='End', blank=True, null=True)   
    length = models.TextField(db_column='Length', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'dna'


class Rna(models.Model):
    rnaid = models.TextField(db_column='RNAID', primary_key=True, blank=True, null=False)   
    transcriptid = models.TextField(db_column='TranscriptID', blank=True, null=True)   
    transcriptgeneid = models.TextField(db_column='TranscriptGeneID', blank=True, null=True)   
    transcriptgenesymbol = models.TextField(db_column='TranscriptGeneSymbol', blank=True, null=True)   
    transcriptchr = models.TextField(db_column='TranscriptChr', blank=True, null=True)   
    transcriptstart = models.IntegerField(db_column='TranscriptStart', blank=True, null=True)   
    transcriptend = models.IntegerField(db_column='TranscriptEnd', blank=True, null=True)   
    transcriptlength = models.IntegerField(db_column='TranscriptLength', blank=True, null=True)   
    transcriptbiotype = models.TextField(db_column='TranscriptBiotype', blank=True, null=True)   
    transcripttriplexcount = models.IntegerField(db_column='TranscriptTriplexCount', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'rna'

class Triplexaligner(models.Model):
    rnaid = models.ForeignKey(Rna, on_delete=models.SET_NULL, db_column='RNAID', blank=True, null=True,\
     related_name = 'triplex_rnaid') 
    dnaid = models.ForeignKey(Dna, on_delete=models.SET_NULL, db_column='DNAID', blank=True, null=True,\
     related_name = 'triplex_dnaid') 
    rnatriplexstart = models.FloatField(db_column='RNATriplexStart', blank=True, null=True)  
    rnatriplexend = models.FloatField(db_column='RNATriplexEnd', blank=True, null=True)  
    dnatriplexstart = models.FloatField(db_column='DNATriplexStart', blank=True, null=True)  
    dnatriplexend = models.FloatField(db_column='DNATriplexEnd', blank=True, null=True) 
    rnalength = models.IntegerField(db_column='RNALength', blank=True, null=True)  
    dnalength = models.IntegerField(db_column='DNALength', blank=True, null=True)  
    triplexalignerscore = models.FloatField(db_column='TriplexAlignerScore', blank=True, null=True)  
    code = models.TextField(db_column='Code', blank=True, null=True)  
    lambda_field = models.FloatField(db_column='Lambda', blank=True, null=True) 
    k = models.FloatField(db_column='K', blank=True, null=True)  
    triplexalignerbitscore = models.FloatField(db_column='TriplexAlignerBitScore', blank=True, null=True)  
    triplexalignere = models.FloatField(db_column='TriplexAlignerE', blank=True, null=True)  
    triplexid = models.TextField(db_column='TriplexID', blank=True, null=True)  
    genometriplexchr = models.TextField(db_column='GenomeTriplexChr', blank=True, null=True)  
    genomednastart = models.IntegerField(db_column='GenomeDNAStart', blank=True, null=True)  
    genometriplexstart = models.FloatField(db_column='GenomeTriplexStart', blank=True, null=True)  
    genometriplexend = models.FloatField(db_column='GenomeTriplexEnd', blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'triplexaligner'












########## SILK MODELS #########################################################################################################


class SilkProfile(models.Model):
    name = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    file_path = models.CharField(max_length=300)
    line_num = models.IntegerField(blank=True, null=True)
    end_line_num = models.IntegerField(blank=True, null=True)
    func_name = models.CharField(max_length=300)
    exception_raised = models.BooleanField()
    dynamic = models.BooleanField()
    request = models.ForeignKey('SilkRequest', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'silk_profile'


class SilkProfileQueries(models.Model):
    profile = models.ForeignKey(SilkProfile, models.DO_NOTHING)
    sqlquery = models.ForeignKey('SilkSqlquery', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'silk_profile_queries'
        unique_together = (('profile', 'sqlquery'),)


class SilkRequest(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    path = models.CharField(max_length=190)
    query_params = models.TextField()
    raw_body = models.TextField()
    body = models.TextField()
    method = models.CharField(max_length=10)
    start_time = models.DateTimeField()
    view_name = models.CharField(max_length=190, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    encoded_headers = models.TextField()
    meta_time = models.FloatField(blank=True, null=True)
    meta_num_queries = models.IntegerField(blank=True, null=True)
    meta_time_spent_queries = models.FloatField(blank=True, null=True)
    pyprofile = models.TextField()
    num_sql_queries = models.IntegerField()
    prof_file = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = 'silk_request'


class SilkResponse(models.Model):
    status_code = models.IntegerField()
    raw_body = models.TextField()
    body = models.TextField()
    encoded_headers = models.TextField()
    request = models.OneToOneField(SilkRequest, models.DO_NOTHING)
    id = models.CharField(primary_key=True, max_length=36)

    class Meta:
        managed = False
        db_table = 'silk_response'


class SilkSqlquery(models.Model):
    query = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    time_taken = models.FloatField(blank=True, null=True)
    traceback = models.TextField()
    request = models.ForeignKey(SilkRequest, models.DO_NOTHING, blank=True, null=True)
    identifier = models.IntegerField()
    analysis = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'silk_sqlquery'



