class Project:

    def __init__(self, file_name):
        self.project_file = open(file_name, 'r');
        self.__load()

    def __load(self):
        print(self.project_file.read())
        self.agents = []
        self.environment = None
        
    def __del__(self):
        self.project_file.close()