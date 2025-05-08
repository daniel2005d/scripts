from datetime import datetime
from rich.table import Table
from rich.console import Console

console = Console()


def print_table(items:list, exclude_columns=None, key_column:str=None):
    if len(items)>0:
        filters=set()

        if exclude_columns is None:
            exclude_columns = []
        
        exclude_columns.append('_sa_instance_state')

        table = Table()
        attributes = items[0].__dict__.keys()
        for attr in attributes:
            if attr not in exclude_columns:
                table.add_column(attr)
        
        for item in items:
            rows = []
            for column in table.columns:
                distinct = True if key_column and key_column != column.header else False
                item_value = getattr(item, column.header)
                
                if isinstance(item_value, datetime):
                    item_value = datetime.strftime(item_value, "%D %M %Y")
                elif isinstance(item_value, int):
                    item_value = str(item_value)
                

                if not distinct:
                    filters.add(item_value)

                #if item_value not in filters:
                rows.append(item_value)
            
            table.add_row(*rows)
        
        console.print(table)
        

