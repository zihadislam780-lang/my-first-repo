from django import forms
from .models import *
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'role', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institute', 'degree', 'year']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'link', 'image']