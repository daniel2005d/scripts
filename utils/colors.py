from colored import Style, Fore, Back, fore, style
from datetime import datetime
import re

class Color:
    
    @staticmethod
    def print_allcolors():
        for color in Style._COLORS:
            print(f"{fore(color)}{color}{Style.reset}")

    @staticmethod
    def format(message):
        pattern = r'\[([^]]+)\]'
        
        for color in re.findall(pattern, message):
            forecolor=''
            if color == 'reset':
                forecolor = Style.reset
            elif color == 'bold':
                forecolor = Style.BOLD
            elif color in Style._COLORS:
                forecolor = fore(color)
            
            if forecolor != '':
                message=message.replace(f"[{color}]", f"{forecolor}")
        
        return message

    @staticmethod
    def print_error(message):
        Color.print(f"[red][-] {message}[reset]")
    
    @staticmethod
    def print_info(message, end=None):
        Color.print(f"[blue][!] {message}[reset]", end=end)
    
    def print_timestamp(message):
        current = datetime.now()
        current_time = current.strftime("%d-%m-%Y %H:%M:%S")
        Color.print(f"[aquamarine_1a][{current_time}] {message} [reset]")
    
    @staticmethod
    def print(message, end=None):
        """
        Print message with color, using format string.
        Example:
        [red][bold]Hello World!![reset]


        """
        print(Color.format(message), end=end)
    
    def highlight_text(text:str, match_word:str, color:str='red')->str:
        text = str(text)
        formatted = False
        hight_light = re.sub(match_word, f"[{color}]{match_word}[reset]", text, flags=re.IGNORECASE)
        return Color.format(hight_light), formatted

if __name__ == '__main__':
    Color.print_allcolors()