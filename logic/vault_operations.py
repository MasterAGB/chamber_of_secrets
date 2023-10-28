import json
import secrets
import string

from PyQt6.QtWidgets import QFileDialog, QMessageBox

from logic.class_registry import ClassRegistry

registry = ClassRegistry()


# for hints


class VaultOperations():

    def generate_secure_key(self, length=32):
        """
        Generate a random key with the given length.
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        key = ''.join(secrets.choice(alphabet) for _ in range(length))
        return key

    # This will be part of the class where create_new_vault is defined
    def create_new_vault(self):

        login = registry.get_main_window().new_login_input.text().strip()
        password = registry.get_main_window().new_password_input.text().strip()

        # Validate input
        if not login or not password:
            QMessageBox.critical(None, 'Error', 'Login and password fields must not be empty.')
            return

        # Check for existing vault
        existing_data = registry.get_immu_db().get_user_data_from_database(login)
        if existing_data and existing_data.get('revisions', []):
            QMessageBox.critical(None, 'Error', 'A vault with this login already exists.')
            return

        key = self.generate_secure_key()

        response_json = registry.get_immu_db().save_new_vault(login, password, key)

        # Handle the response
        if 'documentId' not in response_json:
            QMessageBox.critical(None, 'Error', 'Failed to create a new vault.')
            return

        newu_ser_id = response_json.get('documentId', 'Unknown')
        print("newu_ser_id=" + newu_ser_id)
        registry.set_userid(newu_ser_id)

        # Save the key to a file
        default_file_name = f"{login}_key.txt"
        file_name, _ = QFileDialog.getSaveFileName(None, "Save Key File", default_file_name,
                                                   "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(key)


        #response_text = json.dumps(response_json, indent=4)
        #QMessageBox.information(None, 'Success', f'Successfully created the vault. Your ID is: {registry.get_userid()}. Server Response:\n{response_text}')
        self.display_user_table()

    def display_login_screen(self):

        registry.get_user_password_table().hide()
        registry.get_main_window().show()

    def display_user_table(self):
        # Hide the main window
        registry.get_main_window().hide()

        registry.get_immu_db().load_table_from_database()  # Populate the table after showing it
        registry.get_user_password_table().show()

    def access_user_vault(self, key_from_file):
        try:
            login = registry.get_main_window().existing_login_input.text()
            password = registry.get_main_window().existing_password_input.text()

            print(f"Debug login {login}")

            key = key_from_file

            stored_data = registry.get_immu_db().get_user_data_from_database(login)
            print("Stored Data:", stored_data)  # Debug print

            revisions = stored_data.get('revisions', [])

            if len(revisions) == 0:
                QMessageBox.critical(None, 'Failure', 'No such vault exists.')
                return

            first_revision = revisions[0]
            document = first_revision.get('document', {})

            login_from_db = document.get('login')
            password_from_db = document.get('password')
            key_from_db = document.get('key')

            #response_text = json.dumps(stored_data, indent=4)
            #QMessageBox.information(None, 'Checking response',f'Successfully checked the vault. Server Response:\n{response_text}')

            if login_from_db == login and password_from_db == password and key_from_db == key:
                registry.set_userid(document.get('_id', 'Unknown'))
                print("User id from data:" + registry.get_userid())
                print(stored_data)
                #response_text = json.dumps(stored_data, indent=4)
                #QMessageBox.information(None, 'Success',f'Successfully accessed the vault. ID is: {registry.get_userid()}. Response:\n{response_text}')
                self.display_user_table()
            else:
                QMessageBox.critical(None, 'Failure', 'Failed to access the vault. Invalid credentials or key.')
        except Exception as e:
            print(f"An exception occurred: {e}")
            QMessageBox.critical(None, 'Error', f'An error occurred: {e}')

    def read_key_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Load Key File", "", "Text Files (*.txt);;All Files (*)")
        if file_name:
            with open(file_name, 'r') as f:
                key_from_file = f.read()
            self.access_user_vault(key_from_file)
