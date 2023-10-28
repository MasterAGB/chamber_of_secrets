
# Chamber of Secrets: A Secure Vault Manager 🔒

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Modules](#modules)
6. [Task Requirements](#task-requirements)

## Introduction

Chamber of Secrets is a Python application built with PyQt6 for managing sensitive data like passwords securely. It utilizes the immudb database to keep your data safe and encrypted.

## Requirements 📋

- Python 3.10
- PyQt6
- immudb API key

For a complete list of dependencies, see `requirements.txt`.

```plaintext
PyQt6==6.5.3
requests==2.31.0
```

## Installation

1. Clone the repository.
```bash
git clone https://github.com/MasterAGB/chamber_of_secrets.git
```
2. Run `pip install -r requirements.txt` to install the dependencies.

## Usage

Run the main script to launch the application.

```python
python main.py
```

You'll be greeted with a GUI window that allows you to either create a new vault or access an existing one.

## Modules

- `api/`: Contains the immudb API interface.
- `logic/`: Contains business logic.
- `ui/`: Contains the PyQt6 UI components.

## Task Requirements

1. **Virtual Environment**: A `requirements.txt` is provided for defining the virtual environment.
    ```plaintext
    pip install -r requirements.txt
    ```

2. **Python Modules and Packages**: The code is organized into modules and packages, and makes use of `__init__.py` for package initialization.

3. **Data Types**: Strings, dictionaries, and JSON data types are extensively used.
    ```python
   data = {
       "login": login,
       "password": password,
       "key": key,
   }
    ```
4. **Functions and Classes**: The project uses both standalone functions and classes, including inheritance.
    ```python
   class VaultOperations():
       def generate_secure_key(self, length=32):
   
   ...
   
   class MainWindowWidget(QWidget):
       def __init__(self):
           super().__init__()
           self.setWindowTitle('Chamber of Secrets')
    ```
5. **File System Operations**: The project reads and writes key files.
    ```python
    with open(file_name, "w") as f:
        f.write(key)
    ```

6. **Network Operations**: It uses the immudb API for data storage and retrieval.
    ```python
    requests.post(url, headers=self.HEADERS, json=data)
    ```

---
