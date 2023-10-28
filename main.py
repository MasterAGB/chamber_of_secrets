from PyQt6.QtWidgets import QApplication
from api.immudb import ImmuDB
from logic.class_registry import ClassRegistry
from logic.vault_operations import VaultOperations
from ui.main_window import MainWindowWidget
from ui.user_password_table import UserPasswordTableWidget

registry = ClassRegistry()
immudb_instance = ImmuDB(api_key='default.NQ2l9fEGCUAKaPzzZogZtw.3nnnrusNQ1z-_k4zzpmiibr7m_MARH4wDlC_eyu0vvTmS7K7',
                         ledger="default", collection="default")
immudb_instance.CheckStartup()

vaultOperations_instance = VaultOperations()

registry.set_immu_db(immudb_instance)
registry.register_vault_operations(vaultOperations_instance)
vaultOperations = registry.get_vault_operations()

if __name__ == '__main__':
    app = QApplication([])

    window = MainWindowWidget()
    registry.set_main_window(window)

    user_password_table = UserPasswordTableWidget()
    registry.set_user_password_table(user_password_table)

    window.show()
    app.exec()
