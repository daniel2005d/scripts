import os


class Folder:
    @staticmethod
    def get_script_folder():
        current_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(current_path)
        return script_dir.replace("utils","")
    
    @staticmethod
    def get_current_folder():
        return os.getcwd()

    @staticmethod
    def get_chromedriver_path():
        script_path = Folder.get_script_folder()
        return os.path.join(script_path,"chromedriver")
    
    @staticmethod
    def get_local_folder():
        local_path = os.path.expanduser("~/.local/doc_crawler")
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        
        return local_path
    
    @staticmethod
    def create_folder(path:str):
        if not os.path.exists(path):
            os.makedirs(path)

    
