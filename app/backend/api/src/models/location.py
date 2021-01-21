from api.src.db import db
import api.src.models as models

class Location:
    __table__ = 'locations'
    columns = ['id', 'setting', 'zip_code', 'incident_address',
            'city', 'borough', 'latitude', 'longitude']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)


    # doesn't look like these functions are used anywhere
    def total_by_borough(self, cursor):
        borough_query = """SELECT borough, COUNT(*) FROM locations 
        JOIN incidents ON locations.id = incidents.location_id
        GROUP BY borough"""
        cursor.execute(borough_query)
        record = cursor.fetchall()
        return record
        
    def total_by_setting(self, cursor):
        setting_query = """SELECT setting, COUNT(*) FROM locations 
        JOIN incidents ON location.id = incidents.location_id
        GROUP BY setting"""
        cursor.execute(setting_query)
        record = cursor.fetchall()
        return record

    def total_by_zip_code(self, cursor):
        zip_code_query = """SELECT zip_code, COUNT(*) FROM locations
        JOIN incidents ON location.id = incidents.location_id
        GROUP BY zip_code"""
        cursor.execute(zip_code_query)
        record = cursor.fetchall()
        return record 


