from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QPushButton, QVBoxLayout, QTableWidget, QHBoxLayout
from logic.class_registry import ClassRegistry

registry = ClassRegistry()


class UserPasswordTableWidget(QWidget):
    def __init__(self):
        super().__init__()

        print("hidden window10")
        # ... existing code ...
        self.last_fetched_data = None  # Initialize to None

        self.setWindowTitle('Vault Manager')

        print("hidden window9")
        self.setGeometry(100, 100, 600, 400)  # Increased the width

        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Username', 'Decrypted Password', 'Website URL'])

        print("hidden window8")
        # Connect the itemChanged signal to TableSync
        self.table_widget.itemChanged.connect(self.mark_table_for_sync)

        # Populate table from database on initialization
        # (Note: Replace this comment with your DB fetching logic and populate the table)

        print("hidden window7")
        self.addButton = QPushButton('Add Entry', self)
        self.addButton.clicked.connect(self.add_table_row)

        self.removeButton = QPushButton('Remove Entry', self)
        self.removeButton.clicked.connect(self.remove_table_row)

        self.syncButton = QPushButton('Sync Data', self)
        self.syncButton.clicked.connect(self.synchronize_table_with_database)

        print("hidden window6")
        self.resetButton = QPushButton('Reset Data', self)
        self.resetButton.clicked.connect(self.reset_table_data)
        self.resetButton.hide()  # Initially hidden

        self.logoutButton = QPushButton('Sign Out', self)
        self.logoutButton.clicked.connect(self.logout)

        print("hidden window5")
        self.addButton.setToolTip('Add a new row to the table.')
        self.removeButton.setToolTip('Remove the selected row from the table.')
        self.syncButton.setToolTip('Synchronize the table data with the server to save changes.')
        self.resetButton.setToolTip('Revert table data to the last saved state.')
        self.logoutButton.setToolTip('Sign out and return to the main window.')

        print("hidden window4")
        box_layout = QVBoxLayout()
        sync_reset_layout = QHBoxLayout()  # Horizontal layout for Sync and Reset buttons

        print("hidden window3")
        box_layout.addWidget(self.table_widget)
        box_layout.addWidget(self.addButton)
        box_layout.addWidget(self.removeButton)

        print("hidden window2")
        sync_reset_layout.addWidget(self.syncButton)
        sync_reset_layout.addWidget(self.resetButton)
        box_layout.addLayout(sync_reset_layout)  # Add the horizontal layout to the vertical layout

        box_layout.addWidget(self.logoutButton)

        print("hidden window1")
        self.setLayout(box_layout)

    def add_table_row(self):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.mark_table_for_sync()

    def remove_table_row(self):
        selected_row = self.table_widget.currentRow()
        if selected_row != -1:
            self.table_widget.removeRow(selected_row)
            self.mark_table_for_sync()

    def logout(self):
        registry.get_vault_operations().display_login_screen()

    def synchronize_table_with_database(self):
        # Step 1: Fetch existing data from the database
        existing_data = registry.get_immu_db().get_data_by_user_id(registry.get_userid())
        if existing_data is None:
            print("Error: Failed to fetch existing data for user_id:" + registry.get_userid())
            return

        all_rows = self.get_all_records_from_table()

        existing_data = registry.get_immu_db().merge_records(existing_data, all_rows)
        response = registry.get_immu_db().replace_records(existing_data, registry.get_userid())

        if response.status_code == 200:
            print(f"Successfully synced the table. Response: {response.json()}")
            self.reset_to_synced_state()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response content: {response.content}")

    def mark_table_for_sync(self):

        # Fetch current table data
        current_table_data = []
        row_count = self.table_widget.rowCount()
        for row in range(row_count):
            username = self.table_widget.item(row, 0).text() if self.table_widget.item(row, 0) else ''
            password = self.table_widget.item(row, 1).text() if self.table_widget.item(row, 1) else ''
            website = self.table_widget.item(row, 2).text() if self.table_widget.item(row, 2) else ''
            current_table_data.append({
                'username': username,
                'password': password,
                'website': website
            })

        # Compare with last_fetched_data
        if self.last_fetched_data != current_table_data:
            self.show_pending_changes_state()
        else:
            self.reset_to_synced_state()

    def show_pending_changes_state(self):
        self.resetButton.show()  # Show the Reset button
        self.syncButton.setStyleSheet("background-color: red;")
        self.syncButton.setText("Sync Table (Pending Changes)")

    def reset_table_data(self):
        # Clear the table first
        self.table_widget.setRowCount(0)

        # Populate the table with last_fetched_data
        for row_data in self.last_fetched_data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(row_data.get('username', '')))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(row_data.get('password', '')))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(row_data.get('website', '')))

        # Call the function to reset the sync state
        self.reset_to_synced_state()

    def reset_to_synced_state(self):
        self.syncButton.setStyleSheet("")  # Reset the background color
        self.syncButton.setText("Sync Table")  # Reset the text
        self.resetButton.hide()  # Hide the Reset button after sync

    def get_all_records_from_table(self):
        # Step 2: Update table_data part
        row_count = self.table_widget.rowCount()
        all_rows = []
        for row in range(row_count):
            username = self.table_widget.item(row, 0).text() if self.table_widget.item(row, 0) else ''
            password = self.table_widget.item(row, 1).text() if self.table_widget.item(row, 1) else ''
            website = self.table_widget.item(row, 2).text() if self.table_widget.item(row, 2) else ''
            all_rows.append({
                'username': username,
                'password': password,
                'website': website
            })
        return all_rows
