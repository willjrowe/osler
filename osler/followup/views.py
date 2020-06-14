from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponseRedirect

from osler.core.models import Patient, ActionItem
from osler.core.views import (NoteUpdate, NoteFormView,
                                 get_current_provider_type)

from osler.followup import forms
from osler.followup import models
from django.utils.translation import gettext_lazy as _


def followup_choice(request, pt_id):
    '''Prompt the user to choose a follow up type.'''
    pt = get_object_or_404(Patient, pk=pt_id)
    return render(request, 'core/followup-choice.html', {'patient': pt})


class FollowupUpdate(NoteUpdate):
    template_name = "core/form-update.html"

    def get_success_url(self):
        pt = self.object.patient
        return reverse("core:patient-detail", args=(pt.id, ))


class ActionItemFollowupUpdate(FollowupUpdate):
    model = models.ActionItemFollowup
    form_class = forms.ActionItemFollowup
    note_type = _("Action Item Followup")


class LabFollowupUpdate(FollowupUpdate):
    model = models.LabFollowup
    form_class = forms.LabFollowup
    note_type = _("Lab Followup")


class VaccineFollowupUpdate(FollowupUpdate):
    model = models.VaccineFollowup
    form_class = forms.VaccineFollowup
    note_type = _("Vaccine Followup")


class FollowupCreate(NoteFormView):
    '''A view for creating a new Followup'''
    template_name = 'core/form_submission.html'
    note_type = _("Followup")

    def get_form_class(self, **kwargs):

        ftype = self.kwargs['ftype']

        futypes = {'labs': forms.LabFollowup,
                   'vaccine': forms.VaccineFollowup}

        return futypes[ftype]

    def get_followup_model(self):
        '''Get the subtype of Followup model used by the FollowupForm used by
        this FollowupCreate view.'''
        # I have no idea if this is the right way to do this. It seems a bit
        # dirty.
        return self.get_form_class().Meta.model

    def form_valid(self, form):

        pt = get_object_or_404(Patient, pk=self.kwargs['pt_id'])
        fu = form.save(commit=False)
        fu.patient = pt
        fu.author = self.request.user.provider
        fu.author_type = get_current_provider_type(self.request)

        fu.save()

        form.save_m2m()

        if 'followup_create' in self.request.POST:
            return HttpResponseRedirect(reverse('core:new-action-item',
                                                args=(pt.id,)))
        else:
            return HttpResponseRedirect(reverse("core:patient-detail",
                                                args=(pt.id,)))


class ActionItemFollowupCreate(FollowupCreate):
    '''A view for creating a new ActionItemFollowup'''
    form_class = forms.ActionItemFollowup

    def get_form_class(self,**kwargs):
        return self.form_class

    def form_valid(self, form):
        pt = get_object_or_404(Patient, pk=self.kwargs['pt_id'])
        ai = get_object_or_404(ActionItem, pk=self.kwargs['ai_id'])

        ai_fu = form.save(commit=False)
        ai_fu.author = self.request.user.provider
        ai_fu.author_type = get_current_provider_type(self.request)
        ai_fu.action_item = ai
        ai_fu.patient = pt
        ai_fu.save()
        form.save_m2m()

        if 'followup_create' in self.request.POST:
            return HttpResponseRedirect(reverse('core:new-action-item',
                                                args=(pt.id,)))
        else:
            return HttpResponseRedirect(reverse("core:patient-detail",
                                                args=(pt.id,)))