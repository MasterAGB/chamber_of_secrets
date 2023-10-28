from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from logic.class_registry import ClassRegistry

registry = ClassRegistry()


class MainWindowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chamber of Secrets')

        layout = QVBoxLayout()

        # Logo (text-based)
        self.logo_label = QLabel("✨✨✨🪄 Chamber of Secrets 🪄✨✨✨")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)

        # Option 1: Create a new vault
        self.new_vault_label = QLabel("Create a new vault:")
        layout.addWidget(self.new_vault_label)

        self.new_login_input = QLineEdit()
        layout.addWidget(self.new_login_input)

        self.new_password_input = QLineEdit()
        layout.addWidget(self.new_password_input)

        self.create_vault_button = QPushButton("Create Vault 🔒")
        self.create_vault_button.clicked.connect(registry.get_vault_operations().create_new_vault)
        layout.addWidget(self.create_vault_button)

        # Option 2: Access an existing vault
        self.access_vault_label = QLabel("Access an existing vault:")
        layout.addWidget(self.access_vault_label)

        self.existing_login_input = QLineEdit()
        layout.addWidget(self.existing_login_input)

        self.existing_password_input = QLineEdit()
        layout.addWidget(self.existing_password_input)

        self.key_file_button = QPushButton("Load Key & Access Vault 🔑")
        self.key_file_button.clicked.connect(registry.get_vault_operations().read_key_from_file)
        layout.addWidget(self.key_file_button)

        # self.developer_button = QPushButton("Developer: open table")
        # self.developer_button.clicked.connect(registry.get_vault_operations().display_user_table)
        # layout.addWidget(self.developer_button)

        self.setLayout(layout)
