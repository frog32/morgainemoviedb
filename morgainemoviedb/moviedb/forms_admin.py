from django import forms

class FileImportForm(forms.Form):
    import_field = forms.FileField()
    
class CompareForm(FileImportForm):
    mode = forms.ChoiceField(choices=(('tmdb_id','Difference by TMDB ID'),('file_hash','Difference by File Hash')))