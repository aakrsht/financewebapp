
```markdown
# Enhancing Financial Data Analysis Using Homomorphic Cryptography

## Overview

This project aims to enhance the security and efficiency of financial data analysis by implementing homomorphic encryption. The system is built using the Django framework and leverages the TenSEAL library to perform computations on encrypted data, ensuring data privacy and security throughout the process.

## Features

- **Homomorphic Encryption**: Uses the CKKS scheme to perform arithmetic operations on encrypted financial data.
- **Dual-Layer Encryption**: Adds an extra layer of security with AES encryption.
- **User-Friendly Interface**: Provides a simple and intuitive web interface for uploading and analyzing encrypted data.
- **Performance Testing**: Includes tools to evaluate the time efficiency and memory utilization of the encryption and analysis processes.
- **Real-World Testing**: Tested with simulated financial datasets to assess practical applicability.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/aakrsht/financewebapp.git
   cd financewebapp
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set the Django Secret Key:
   - Generate a new secret key. You can use the following Python script to generate one:
     ```python
     import secrets
     print(secrets.token_urlsafe(50))
     ```
   - Copy the generated key and add it to the `financewebapp/settings.py` file:
     ```python
     SECRET_KEY = 'your-generated-secret-key'
     ```

## Usage

1. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the Application**:
   Open your web browser and go to `http://127.0.0.1:8000` to access the home page.

3. **Encrypt Data**:
   - Navigate to the Encryptor App.
   - Upload your CSV file and click the 'Encrypt' button.
   - Download the encrypted file.

4. **Analyze Encrypted Data**:
   - Navigate to the Analysis App.
   - Upload the encrypted file and necessary keys.
   - Perform the analysis and view the results.

## Repository Structure

- `encryptor/`: Contains the Encryptor App for encrypting financial data.
- `analysis/`: Contains the Analysis App for performing computations on encrypted data.
- `templates/`: HTML templates for the web interface.
- `static/`: Static files (CSS, JavaScript) used in the web interface.
- `requirements.txt`: List of dependencies required to run the project.
- `README.md`: Project overview and setup instructions.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the existing style and passes all tests.


---

[GitHub Repository](https://github.com/aakrsht/financewebapp)
