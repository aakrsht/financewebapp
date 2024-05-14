from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib import messages
from .forms import FileUploadForm
import pandas as pd
import tenseal as ts
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import io
import zipfile
import os
import mimetypes


def load_aes_key_from_content(key_content):
    return key_content


def aes_encrypt(data, key):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data


def encryptor_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                csv_file = request.FILES['csv_file'].read().decode('utf-8')
                aes_key_content = request.FILES['aes_key_file'].read()

                aes_key = load_aes_key_from_content(aes_key_content)
                df = pd.read_csv(io.StringIO(csv_file))

                context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192,
                                     coeff_mod_bit_sizes=[60, 40, 40, 60])
                context.global_scale = 2 ** 40
                context.generate_galois_keys()

                encrypted_columns = {}
                for column in df.columns:
                    if column != 'Month':
                        encrypted_columns[column] = [ts.ckks_vector(context, [value]).serialize() for value in
                                                     df[column]]
                    else:
                        encrypted_columns[column] = df[column].tolist()

                buffer = io.BytesIO()
                pd.DataFrame(encrypted_columns).to_pickle(buffer)
                encrypted_df_bytes = buffer.getvalue()
                encrypted_df_data = aes_encrypt(encrypted_df_bytes, aes_key)

                context_buffer = io.BytesIO()
                context_buffer.write(context.serialize(save_secret_key=True))
                encrypted_context_data = aes_encrypt(context_buffer.getvalue(), aes_key)

            except Exception as e:
                messages.error(request,
                               'An error occurred during encryption. Please make sure correct files are uploaded.')
                return render(request, 'encryptor/upload_form.html', {'form': form})

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr('encrypted_data.pkl.aes', encrypted_df_data)
                zip_file.writestr('tenseal_context.tenseal.aes', encrypted_context_data)
            zip_buffer.seek(0)

            zip_name = 'encrypted_files.zip'
            path = default_storage.save(zip_name, ContentFile(zip_buffer.read()))

            download_url = redirect('encryptor:download', path=path)
            return download_url
    else:
        form = FileUploadForm()

    return render(request, 'encryptor/upload_form.html', {'form': form})


def download_file(request, path):
    if not default_storage.exists(path):
        return HttpResponse("File not found.", status=404)

    actual_download_url = reverse('encryptor:actual_download', kwargs={'path': path})

    return render(request, 'encryptor/download_page.html', {'download_url': actual_download_url})


def actual_download(request, path):
    if not default_storage.exists(path):
        return HttpResponse("File not found.", status=404)

    file = default_storage.open(path, 'rb')
    mime_type, _ = mimetypes.guess_type(path)
    response = HttpResponse(file, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(path)}"'

    default_storage.delete(path)
    return response
