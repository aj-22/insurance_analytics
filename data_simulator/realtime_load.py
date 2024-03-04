from connection import SQL
import os

class Live_Loader:
    def __init__(self):
        self.sql = SQL()

    def load_json(self, filepath):
        sql_statement = f'''
        INSERT INTO staging.lead_blob
        SELECT bulkColumn, '{filepath}' as file_name, current_timestamp as loaded_at
        FROM OPENROWSET(BULK '{filepath}', SINGLE_CLOB) as j
        '''
        self.sql.cursor.execute(sql_statement)
        self.sql.cursor.commit()

    def archive_file(self, filepath, filename):
        archive_path = os.path.abspath('.'+os.sep+'archive'+os.sep+filename)
        os.replace(filepath, archive_path)

    def iterate_load_archive(self, folder='.'+os.sep+'data_output'):
        filenames = os.listdir(folder)
        for filename in filenames:
            if filename[-5:] == '.json':
                filepath = os.path.abspath(f'{folder}{os.sep}{filename}')
                self.load_json(filepath)
                self.archive_file(filepath, filename)
    
    

if __name__ == '__main__':
    loader = Live_Loader()
    loader.iterate_load_archive()