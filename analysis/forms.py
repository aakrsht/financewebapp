from django import forms
class FileUploadForm(forms.Form):
    aes_key = forms.FileField(label='Upload AES Key')
    encrypted_data = forms.FileField(label='Upload Encrypted Data')
    context_file = forms.FileField(label='Upload TenSEAL Context')
