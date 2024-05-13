class Singleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instances is None:
            cls._instance = cls.__new__(cls)
        return cls._instance