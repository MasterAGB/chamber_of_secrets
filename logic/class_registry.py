class ClassRegistry:
    _instance = None  # Class variable to hold the single instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassRegistry, cls).__new__(cls)
            cls.immu_db = None
            cls.userPasswordTable = None
            cls.vaultOperations = None
            cls.window = None
            cls.user_id = None

        return cls._instance

    def __init__(self):
        self.immu_db = None
        self.userPasswordTable = None
        self.vaultOperations = None
        self.window = None
        self.user_id = None

    def get_main_window(self):
        return self.window

    def set_main_window(self, window_Instance):
        self.window = window_Instance

    def set_user_password_table(self, userPasswordTable_instance):
        self.userPasswordTable = userPasswordTable_instance

    def get_user_password_table(self):
        return self.userPasswordTable

    def get_immu_db(self):
        return self.immu_db

    def set_immu_db(self, immuDB_instance):
        self.immu_db = immuDB_instance

    def register_vault_operations(self, vaultOperations_instance):
        self.vaultOperations = vaultOperations_instance

    def get_vault_operations(self):
        return self.vaultOperations

    def get_userid(self):
        return self.user_id

    def set_userid(self, newu_ser_id):
        self.user_id = newu_ser_id
