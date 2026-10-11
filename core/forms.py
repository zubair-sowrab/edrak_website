from django import forms
from django.forms import inlineformset_factory
from .models import Project, Lease, ProjectImage, ProjectFeature, LeaseImage, LeaseFeature

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = '__all__'

# Formsets for Dynamic Rows
ProjectImageFormSet = inlineformset_factory(Project, ProjectImage, fields=('image',), extra=1, max_num=4, can_delete=True)
ProjectFeatureFormSet = inlineformset_factory(Project, ProjectFeature, fields=('feature',), extra=1, can_delete=True)

LeaseImageFormSet = inlineformset_factory(Lease, LeaseImage, fields=('image',), extra=1, max_num=4, can_delete=True)
LeaseFeatureFormSet = inlineformset_factory(Lease, LeaseFeature, fields=('feature',), extra=1, can_delete=True)