class Task:
    def __init__(self, name, description, status):
        self.name = name
        self.description = description
        self.status = status

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_description(self):
        return self.description
      
    def set_description(self, description):
        self.description = description

    def get_status(self):
        return self.status
      
    def set_status(self, status):
        self.status = status

