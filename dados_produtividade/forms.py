from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': 'Ex.: Revisar indicadores semanais'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Descreva a tarefa em detalhes'})

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Selecione o arquivo CSV de Atividades', help_text='O arquivo deve conter as colunas: "Start Time", "End Time", "Description"')
