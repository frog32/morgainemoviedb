from django import forms

class FileImportForm(forms.Form):
    import_field = forms.FileField()
