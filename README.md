

# Enhancing Financial Data Analysis Using Homomorphic Cryptography

This project aims to enhance the security of financial data analysis by integrating homomorphic encryption within a Django-based web application. By leveraging the TenSEAL library, this project allows secure computations on encrypted financial data, ensuring data privacy throughout the analysis process.

## Key Features

- **Homomorphic Encryption**: Perform arithmetic operations on encrypted data without needing to decrypt it.
- **Dual-Layer Security**: Combines homomorphic encryption with AES for added security.
- **User-Friendly Interface**: An intuitive web interface for secure data upload and analysis.
- **Real-World Applicability**: Tested with simulated financial datasets to ensure practical use.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Django
- TenSEAL
- NumPy
- Pandas

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/aakrsht/financewebapp.git
    cd financewebapp
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the Django secret key:
    - Generate a new secret key. You can use the following Python script to generate one:
     ```python
     import secrets
     print(secrets.token_urlsafe(50))
     ```
   - Copy the generated key and add it to the `settings.py` file:
     ```python
     SECRET_KEY = 'your-generated-secret-key'
     ```

4. Generate an AES key:
    Use the following Python script to generate an AES key and save it to a file:
    ```python
    import os

    def generate_aes_key(key_size=256):
        if key_size not in [128, 192, 256]:
            raise ValueError("AES key must be either 128, 192, or 256 bits.")
        return os.urandom(key_size // 8)

    def save_aes_key_to_file(key, file_path):
        with open(file_path, 'wb') as key_file:
            key_file.write(key)
        print(f"AES-{key_size} key generated and saved to {file_path}")

    if __name__ == "__main__":
        key_size = 256  # Example: 256 for AES-256
        key_file_path = 'aes_key.bin'  # Update this to your preferred path

        aes_key = generate_aes_key(key_size)
        save_aes_key_to_file(aes_key, key_file_path)
    ```

### Usage

1. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

2. Access the application through your web browser at `http://127.0.0.1:8000`.

### Data Requirements

The Django application currently works only with CSV files created using the following Python program. This program generates random financial data for a specified number of persons:
```python
import pandas as pd
import numpy as np

def generate_random_person_data(num_persons):
    data = []
    for person_id in range(1, num_persons + 1):
        for month in range(1, 13):  # Assuming data for 12 months per person
            income = np.random.uniform(4000, 6000)
            expenses = np.random.uniform(3000, income)  # Expenses should not exceed income
            investments = np.random.uniform(10000, 50000)
            loans = np.random.uniform(5000, 20000)
            payments = np.random.uniform(400, 1000)
            credit_score = np.random.randint(300, 850)  # Typical credit score range
            savings = income - expenses - payments  # Simplistic calculation for savings

            row = {
                'Person_ID': person_id,
                'Month': month,
                'Income': income,
                'Expenses': expenses,
                'Investments': investments,
                'Loans': loans,
                'Payments': payments,
                'Credit_Score': credit_score,
                'Savings': savings
            }
            data.append(row)

    df = pd.DataFrame(data)
    return df

# User interaction part
num_persons = int(input("Enter the number of persons you want to generate data for: "))
csv_filename = input("Enter the name of the CSV file to save the data (include .csv extension): ")
df_generated = generate_random_person_data(num_persons)
df_generated.to_csv(csv_filename, index=False)  # Save the data to the specified CSV file
print(f"Data has been generated and saved to '{csv_filename}'.")
```

### Future Enhancements

- **Advanced Encryption Features**: Implementing newer and more robust encryption algorithms as they become available.
- **Real-Time Data Processing**: Enhancing the system to handle real-time data encryption and analysis.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.
