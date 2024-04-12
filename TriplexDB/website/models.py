# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class DNA(models.Model):
#     promoterid = models.CharField(db_column='PromoterID', primary_key=True, blank=False, null=False, max_length=150)  # Field name made lowercase. This field type is a guess.
#     promotertranscriptids = models.CharField(db_column='PromoterTranscriptIDs', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
#     promotergeneids = models.CharField(db_column='PromoterGeneIDs', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
#     promotersymbols = models.CharField(db_column='PromoterSymbols', blank=True, null=True, max_length=150, verbose_name='Promoter Symbol(s)')  # Field name made lowercase. This field type is a guess.
#     promoterchr = models.CharField(db_column='PromoterChr', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
#     promoterstart = models.IntegerField(db_column='PromoterStart', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
#     promoterend = models.IntegerField(db_column='PromoterEnd', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
#     promoterlength = models.IntegerField(db_column='PromoterLength', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

#     def __str__(self):
#         return self.promotersymbols + ' : ' + self.promotertranscriptids 

#     class Meta:
#         managed = False
#         db_table = 'DNA'


class rem(models.Model):
    remid = models.CharField(db_column='REMID', blank=False, primary_key=True, null=False, max_length=150)  # Field name made lowercase. This field type is a guess.
    remgeneids = models.CharField(db_column='REMGeneIDs', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
    remsymbols = models.CharField(db_column='REMSymbols', blank=True, max_length=150, verbose_name='REM Symbol(s)')  # Field name made lowercase. This field type is a guess.
    remchr = models.CharField(db_column='REMChr', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
    remstart = models.IntegerField(db_column='REMStart', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    remend = models.IntegerField(db_column='REMEnd', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    remlength = models.IntegerField(db_column='REMLength', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    def __str__(self):
        return self.remid + ' : ' + self.remsymbols 

    class Meta:
        managed = False
        db_table = 'rem'


class rna(models.Model):
    transcriptid = models.CharField(db_column='TranscriptID', primary_key=True, blank=False, null=False, max_length=150)  # Field name made lowercase. This field type is a guess.
    transcriptgeneid = models.CharField(db_column='TranscriptGeneID', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
    transcriptgenesymbol = models.CharField(db_column='TranscriptGeneSymbol', blank=True, null=True, max_length=150, verbose_name='RNA Symbol')  # Field name made lowercase. This field type is a guess.
    transcriptchr = models.CharField(db_column='TranscriptChr', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.
    transcriptstart = models.IntegerField(db_column='TranscriptStart', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    transcriptend = models.IntegerField(db_column='TranscriptEnd', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    transcriptlength = models.IntegerField(db_column='TranscriptLength', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    transcriptbiotype = models.CharField(db_column='TranscriptBiotype', blank=True, null=True, max_length=150)  # Field name made lowercase. This field type is a guess.

    def __str__(self):
        return self.transcriptgenesymbol + ' : ' + self.transcriptid 


    class Meta:
        managed = False
        db_table = 'rna'

# class Triplexaligner(models.Model):
#     triplexid = models.CharField(db_column='TriplexID', primary_key=True, blank=False, null=False, max_length=150)
#     rna = models.ForeignKey(RNA, blank=False, null=True, on_delete=models.SET_NULL, db_column='TranscriptID')  # Field name made lowercase.
#     promoter = models.ForeignKey(DNA, blank=False, null=True, on_delete=models.SET_NULL, db_column='PromoterID')  # Field name made lowercase.
#     transcripttriplexstart = models.IntegerField(db_column='TranscriptTriplexStart', blank=True, null=True)  # Field name made lowercase.
#     transcripttriplexend = models.IntegerField(db_column='TranscriptTriplexEnd', blank=True, null=True)  # Field name made lowercase.
#     promotertriplexstart = models.IntegerField(db_column='PromoterTriplexStart', blank=True, null=True)  # Field name made lowercase.
#     promotertriplexend = models.IntegerField(db_column='PromoterTriplexEnd', blank=True, null=True)  # Field name made lowercase.
#     transcriptlength = models.IntegerField(db_column='TranscriptLength', blank=True, null=True)  # Field name made lowercase.
#     promoterlength = models.IntegerField(db_column='PromoterLength', blank=True, null=True)  # Field name made lowercase.
#     triplexalignerscore = models.FloatField(db_column='TriplexAlignerScore', blank=True, null=True, max_length=150, verbose_name='TriplexAligner Score')  # Field name made lowercase.
#     lambda_field = models.FloatField(db_column='Lambda', blank=True, null=True, max_length=150)  # Field name made lowercase. Field renamed because it was a Python reserved word.
#     k = models.FloatField(db_column='K', blank=True, null=True, max_length=150)  # Field name made lowercase.
#     triplexalignerbitscore = models.FloatField(db_column='TriplexAlignerBitScore', blank=True, null=True, max_length=150)  # Field name made lowercase.
#     triplexalignere = models.FloatField(db_column='TriplexAlignerE', blank=True, null=True, max_length=150, verbose_name='TriplexAligner E')  # Field name made lowercase.
#     triplexalignercode = models.CharField(db_column='Code', blank=True, null=True, max_length=10, verbose_name='Code')

#     class Meta:
#         managed = False
#         db_table = 'TriplexAligner'


class triplexaligner(models.Model):
    triplexid = models.CharField(db_column='TriplexID', primary_key=True, blank=False, null=False, max_length=150)
    rna = models.ForeignKey(rna, blank=False, null=True, on_delete=models.SET_NULL, db_column='TranscriptID',\
     related_name = 'rna_triplexid')  # Field name made lowercase.
    rem = models.ForeignKey(rem, blank=False, null=True, on_delete=models.SET_NULL, db_column='REMID',\
     related_name = 'rem_triplexid')  # Field name made lowercase.
    transcripttriplexstart = models.IntegerField(db_column='TranscriptTriplexStart', blank=True, null=True)  # Field name made lowercase.
    transcripttriplexend = models.IntegerField(db_column='TranscriptTriplexEnd', blank=True, null=True)  # Field name made lowercase.
    remtriplexstart = models.IntegerField(db_column='REMTriplexStart', blank=True, null=True)  # Field name made lowercase.
    remtriplexend = models.IntegerField(db_column='REMTriplexEnd', blank=True, null=True)  # Field name made lowercase.
    transcriptlength = models.IntegerField(db_column='TranscriptLength', blank=True, null=True)  # Field name made lowercase.
    remlength = models.IntegerField(db_column='REMLength', blank=True, null=True)  # Field name made lowercase.
    triplexalignerscore = models.FloatField(db_column='TriplexAlignerScore', blank=True, null=True, max_length=150, verbose_name='TriplexAligner Score')  # Field name made lowercase.
    lambda_field = models.FloatField(db_column='Lambda', blank=True, null=True, max_length=150)  # Field name made lowercase. Field renamed because it was a Python reserved word.
    k = models.FloatField(db_column='K', blank=True, null=True, max_length=150)  # Field name made lowercase.
    triplexalignerbitscore = models.FloatField(db_column='TriplexAlignerBitScore', blank=True, null=True, max_length=150)  # Field name made lowercase.
    triplexalignere = models.FloatField(db_column='TriplexAlignerE', blank=True, null=True, max_length=150, verbose_name='TriplexAligner E')  # Field name made lowercase.
    triplexalignercode = models.CharField(db_column='Code', blank=True, null=True, max_length=10, verbose_name='Code')

    def __str__(self):
        return self.triplexid 

    class Meta:
        managed = False
        db_table = 'triplexaligner'


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


class PollsChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()
    question = models.ForeignKey('PollsQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polls_choice'


class PollsQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'polls_question'
