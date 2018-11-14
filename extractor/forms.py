from django import forms


class FileUrlForm(forms.Form):
    selected_file = forms.CharField(label='Selected file')
