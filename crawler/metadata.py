class MetadataItem:
    def __init__(self, **kwargs):
        self.id = 0
        self.file_id = 0
        self.created = None
        self.key = None
        self.value = None
        self.url = None

        for key,value in kwargs.items():
            setattr(self, key, value)