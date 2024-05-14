from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FileUploadForm
import tenseal as ts
import pandas as pd
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import io


def load_aes_key(key_path):
    try:
        with open(key_path, 'rb') as key_file:
            key = key_file.read()
        return key
    except IOError as e:
        print(f"Failed to read AES key: {e}")
        return None


def aes_decrypt(encrypted_data, key):
    try:
        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data
    except Exception as e:
        print(f"Decryption failed: {e}")
        return None


def load_context(path, aes_key):
    encrypted_context = open(path, 'rb').read()
    context_data = aes_decrypt(encrypted_context, aes_key)
    return ts.context_from(context_data)


def load_encrypted_data(path, aes_key):
    encrypted_data = open(path, 'rb').read()
    data_bytes = aes_decrypt(encrypted_data, aes_key)
    return pd.read_pickle(io.BytesIO(data_bytes))


def decrypt_vector(context, encrypted_vector):
    return ts.ckks_vector_from(context, encrypted_vector).decrypt()


def encrypted_sum(context, encrypted_column):
    return sum(ts.ckks_vector_from(context, serial_vector) for serial_vector in encrypted_column)


def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if handle_uploaded_files(request.FILES):
                return redirect('analysis:visualization_page')
            else:
                messages.error(request, "Failed to handle files correctly.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = FileUploadForm()
    return render(request, 'analysis/upload.html', {'form': form})


def handle_uploaded_files(files):
    upload_dir = 'uploads'
    try:
        os.makedirs(upload_dir, exist_ok=True)

        standard_names = {
            'aes_key': 'aes_key.bin',
            'encrypted_data': 'encrypted_data.pkl.aes',
            'context_file': 'tenseal_context.tenseal.aes'
        }

        file_paths = {}
        for file_type, file in files.items():
            standard_file_name = standard_names.get(file_type)
            if standard_file_name:
                file_path = os.path.join(upload_dir, standard_file_name)
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                file_paths[file_type] = file_path
            else:
                print(f"No standard file name defined for type {file_type}")

        return file_paths
    except Exception as e:
        print(f"Error handling files: {e}")
        return {}


def delete_files(file_paths):
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"Successfully deleted {file_path}")
        except OSError as e:
            print(f"Error: {file_path} : {e.strerror}")


def data_visualization(request):
    aes_key_path = 'uploads/aes_key.bin'
    encrypted_data_path = 'uploads/encrypted_data.pkl.aes'
    context_path = 'uploads/tenseal_context.tenseal.aes'

    aes_key = load_aes_key(aes_key_path)
    if aes_key is None:
        return JsonResponse({"error": "Failed to load AES key"}, status=400)

    context = load_context(context_path, aes_key)
    if context is None:
        return JsonResponse({"error": "Failed to load context"}, status=400)

    encrypted_df = load_encrypted_data(encrypted_data_path, aes_key)
    if encrypted_df is None:
        return JsonResponse({"error": "Failed to load encrypted data"}, status=400)

    monthly_metrics = ['Income', 'Expenses', 'Savings', 'Payments', 'Investments', 'Loans']
    decrypted_data = {metric: [] for metric in monthly_metrics}
    averages = {metric: [] for metric in monthly_metrics}

    for month in range(1, 13):
        for metric in monthly_metrics:
            monthly_data = encrypted_df[encrypted_df['Month'] == month][metric]
            decrypted_total = sum([decrypt_vector(context, vector)[0] for vector in monthly_data])
            decrypted_data[metric].append(decrypted_total)
            if len(monthly_data) > 0:
                averages[metric].append(decrypted_total / len(monthly_data))
            else:
                averages[metric].append(0)

    cumulative_sums = {metric: np.cumsum(decrypted_data[metric]).tolist() for metric in
                       ['Income', 'Expenses', 'Savings']}

    savings_rate = [s / i if i else 0 for s, i in zip(decrypted_data['Savings'], decrypted_data['Income'])]

    formatted_data = {metric: [float(value) for value in values] for metric, values in decrypted_data.items()}
    formatted_averages = {metric: [float(value) for value in values] for metric, values in averages.items()}
    formatted_savings_rate = [float(rate) for rate in savings_rate]

    all_scores = [decrypt_vector(context, score)[0] for score in encrypted_df['Credit_Score']]
    hist, bin_edges = np.histogram(all_scores, bins=range(300, 850, 50))
    histogram_data = [{"bin_start": int(bin_edges[i]), "count": int(hist[i])} for i in range(len(hist))]

    data_for_d3 = {
        "months": list(range(1, 13)),
        "totals": formatted_data,
        "cumulative": cumulative_sums,
        "savingsRate": formatted_savings_rate,
        "averages": formatted_averages,
        "creditScoreHistogram": histogram_data,
    }

    delete_files([aes_key_path, encrypted_data_path, context_path])

    return JsonResponse(data_for_d3)


def visualization_page(request):
    return render(request, 'analysis/visualization.html')
