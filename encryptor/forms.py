from django import forms

class FileUploadForm(forms.Form):
    csv_file = forms.FileField(label='CSV File')
    aes_key_file = forms.FileField(label='AES Key File')
