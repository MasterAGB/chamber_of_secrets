import json
import requests
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox

from logic.class_registry import ClassRegistry

registry = ClassRegistry()


class ImmuDB():

    def __init__(self, api_key, ledger, collection):
        self.API_KEY = api_key
        self.LEDGER = ledger
        self.COLLECTION = collection
        self.HEADERS = {
            'accept': 'application/json',
            'X-API-Key': self.API_KEY,
            'Content-Type': 'application/json',
        }

    def create_unique_field_index(self, field):
        data = {
            'fields': [field],
            'isUnique': True
        }

        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/indexes'
        response = requests.post(url, headers=self.HEADERS, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def check_for_existing_records(self):
        data = {
            'page': 1,
            'perPage': 1,  # We just need to know if at least one record exists
        }

        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/documents/search'
        response = requests.post(url, headers=self.HEADERS, json=data)

        if response.status_code == 200:
            revisions = response.json().get('revisions', [])
            return len(revisions) > 0  # True if at least one record exists, else False

        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")
            return True  # Assume records exist to be safe

    # Inside ImmuDB class
    def save_new_vault(self, login, password, key):
        print("save_new_vault")
        data = {
            "login": login,
            "password": password,
            "key": key,
            "table_data": [
                {
                    'username': login + "1",
                    'password': 'examplePassword1',
                    'website': 'www.example1.com'
                },
                {
                    'username': login + "2",
                    'password': 'examplePassword2',
                    'website': 'www.example2.com'
                },
                {
                    'username': login + "3",
                    'password': 'examplePassword3',
                    'website': 'www.example3.com'
                }
            ]
        }
        return self.save_data_to_database(data)

    def create_new_vault(self, key):

        login = registry.get_main_window().new_login_input.text().strip()  # Remove any leading/trailing whitespace
        password = registry.get_main_window().new_password_input.text().strip()  # Remove any leading/trailing whitespace

        # Check for empty login or password
        if not login or not password:
            QMessageBox.critical(None, 'Error', 'Login and password fields must not be empty.')
            return

        # Check if a vault with this login already exists
        existing_data = self.get_user_data_from_database(login)
        if existing_data and existing_data.get('revisions', []):
            QMessageBox.critical(None, 'Error', 'A vault with this login already exists.')
            return

        key = registry.get_vault_operations().generate_secure_key()
        print(f"Generated random key: {key}")

        # Prepare data for the new vault

        # Store the login, password, and key in immudb
        data = {
            "login": login,
            "password": password,
            "key": key,
            "table_data": [
                {
                    'username': login + "1",
                    'password': 'examplePassword1',
                    'website': 'www.example1.com'
                },
                {
                    'username': login + "2",
                    'password': 'examplePassword2',
                    'website': 'www.example2.com'
                },
                {
                    'username': login + "3",
                    'password': 'examplePassword3',
                    'website': 'www.example3.com'
                }
            ]
        }
        # print("sending data:");
        # print(data);
        response_json = self.save_data_to_database(data)

        # print("Got response:");
        # print(response_json);

        if 'documentId' not in response_json:
            QMessageBox.critical(None, 'Error', 'Failed to create a new vault.')
            return

        registry.set_userid(response_json.get('documentId', 'Unknown'))

        # print(f"Created user_id: {registry.get_userid()}")

        # Now that the vault is successfully created, save the key to a file
        options = QFileDialog.Options()
        default_file_name = f"{login}_key.txt"
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Key File", default_file_name,
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, "w") as f:
                f.write(key)

        response_text = json.dumps(response_json, indent=4)
        QMessageBox.information(None, 'Success',
                                f'Successfully created the vault. Your ID is: {registry.get_userid()}. Server Response:\n{response_text}')
        print(f'Successfully created the vault. Your ID is: {registry.get_userid()}. Server Response:\n{response_text}')
        registry.get_vault_operations().display_user_table()

    # Fetch data by _id from database
    def get_data_by_user_id(self, _id):
        data = {
            'page': 1,
            'perPage': 100,
            'query': {
                'expressions': [
                    {
                        'fieldComparisons': [
                            {
                                'field': '_id',
                                'operator': 'EQ',
                                'value': _id
                            }
                        ]
                    }
                ]
            }
        }

        response = requests.post(
            f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/documents/search',
            headers=self.HEADERS,
            json=data
        )

        if response.status_code == 200:
            revisions = response.json().get('revisions', [])
            if revisions:  # if revisions exist
                return revisions[0]  # Assuming the latest revision is what you want
        return None

    def modify_collection_schema(self):
        data = {
            'fields': [
                {
                    'name': 'login',
                    'type': 'STRING'
                }
            ],
            'indexes': [
                {
                    'fields': ['login'],
                    'isUnique': True  # Assuming 'login' should be unique
                }
            ]
        }

        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}'
        response = requests.put(url, headers=self.HEADERS, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")
            return None

    def save_data_to_database(self, data):
        print("save_data_to_database")
        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/document'
        response = requests.put(url, headers=self.HEADERS, data=json.dumps(data))
        return response.json()

    def fetch_collection_metadata(self):
        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}'
        response = requests.get(url, headers=self.HEADERS)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")
            return None

    def get_user_data_from_database(self, login):
        collection_info = self.fetch_collection_metadata()
        if collection_info:
            print("Got to retrieve collection info.")
            print(json.dumps(collection_info, indent=4))
        else:
            print("Failed to retrieve collection info.")

        data = {
            'page': 1,
            'perPage': 100,
            'query': {
                'expressions': [
                    {
                        'fieldComparisons': [
                            {
                                'field': 'login',
                                'operator': 'EQ',
                                'value': login
                            }
                        ]
                    }
                ]
            }
        }

        url = f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/documents/search'
        response = requests.post(url, headers=self.HEADERS, json=data)

        if response.status_code == 200:
            print(f"Yey! {response.status_code}")
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")
            return None

    def load_table_from_database(self):

        data = {
            'page': 1,
            'perPage': 100,
            'query': {
                'expressions': [
                    {
                        'fieldComparisons': [
                            {
                                'field': '_id',
                                'operator': 'EQ',
                                'value': registry.get_userid()
                            }
                        ]
                    }
                ]
            }
        }
        print(f"Searching for data: {registry.get_userid()}")

        response = requests.post(
            f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/documents/search',
            headers=self.HEADERS,
            json=data
        )

        if response.status_code == 200:
            revisions = response.json().get('revisions', [])
            if revisions:  # if revisions exist
                document = revisions[0].get('document', {})
                table_data = document.get('table_data', [])
                table = registry.get_user_password_table().table_widget;
                table.setRowCount(0)  # Clear the table first

                registry.get_user_password_table().last_fetched_data = table_data  # Update last_fetched_data

                for row_data in table_data:
                    row_position = table.rowCount()
                    table.insertRow(row_position)
                    table.setItem(row_position, 0, QTableWidgetItem(row_data.get('username', '')))
                    table.setItem(row_position, 1, QTableWidgetItem(row_data.get('password', '')))
                    table.setItem(row_position, 2, QTableWidgetItem(row_data.get('website', '')))
            else:
                print(f"Error: Failed to populate table. Revisions empty. Status code: {response.status_code}")
        else:
            print(f"Error: Failed to populate table. Status code: {response.status_code}")
            print(data)

    def CheckStartup(self):
        # Only execute if no records exist in the DB
        if not self.check_for_existing_records():
            # Your existing code
            update_result = self.modify_collection_schema()
            #print(json.dumps(update_result, indent=4))
            if not update_result:
                print("Failed to update collection fields.")


            index_result = self.create_unique_field_index('login')
            # print(json.dumps(index_result, indent=4))
            if not index_result:
                print("Failed to create unique index.")


    def replace_records(self, existing_data, user_id):
        # Step 3: Update the document with the merged data
        update_body = {
            'document': existing_data['document'],
            'query': {
                'expressions': [{
                    'fieldComparisons': [{
                        'field': '_id',
                        'operator': 'EQ',
                        'value': user_id
                    }]
                }]
            }
        }

        response = requests.post(
            f'https://vault.immudb.io/ics/api/v1/ledger/{self.LEDGER}/collection/{self.COLLECTION}/document',
            headers=self.HEADERS,
            json=update_body
        )
        return response;

    @classmethod
    def merge_records(self, existing_data, all_rows):
        existing_data['document']['table_data'] = all_rows  # Replace only table_data part
        return existing_data
