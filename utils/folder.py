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
