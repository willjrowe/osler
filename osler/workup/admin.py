from __future__ import unicode_literals
from django.contrib import admin
from django.urls import reverse

from osler.utils import admin as admin_utils
from . import models


@admin.register(models.ClinicDate)
class ClinicDateAdmin(admin.ModelAdmin):
    date_hierarchy = 'clinic_date'
    list_display = ('__str__', 'clinic_date', 'clinic_type', 'number_of_notes')


@admin.register(models.Workup)
class WorkupAdmin(admin_utils.NoteAdmin):
    date_hierarchy = 'written_datetime'

    list_display = ('chief_complaint', 'written_datetime', 'patient',
                    'author', 'clinic_day', 'attending', 'signed', 'is_pending')

    readonly_fields = admin_utils.NoteAdmin.readonly_fields + (
        'author', 'signed_date', 'signer')
    list_filter = ('clinic_day', 'diagnosis_categories')
    search_fields = ('patient__first_name', 'patient__last_name',
                     'attending__first_name', 'attending__last_name',
                     'author__first_name', 'author__last_name',
                     'clinic_day__clinic_type__name',
                     'chief_complaint')

    def view_on_site(self, obj):
        url = reverse('workup', kwargs={'pk': obj.pk})
        return url


@admin.register(models.AttestableBasicNote)
class AttestableBasicNoteAdmin(admin_utils.NoteAdmin):

    def view_on_site(self, obj):
        url = reverse('attestable-basic-note-detail', kwargs={'pk': obj.pk})
        return url


@admin.register(models.BasicNote)
class BasicNoteAdmin(admin_utils.NoteAdmin):

    def view_on_site(self, obj):
        url = reverse('basic-note-detail', kwargs={'pk': obj.pk})
        return url

@admin.register(models.Addendum)
class AddendumAdmin(admin_utils.NoteAdmin):
    pass


for model in [models.ClinicType, models.DiagnosisType]:
    admin_utils.simplehistory_aware_register(model)
