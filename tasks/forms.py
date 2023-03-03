from django import forms
from .models import Tasks

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['titulo','descripcion','importante']
        widgets ={
            'titulo': forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','placeholder':'Describe la tarea'}),
            'importante': forms.CheckboxInput(attrs={'class':'form-check-imput'}),
        }