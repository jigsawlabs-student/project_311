from api.src.db import db
import api.src.models as models

class Complaint:
    __table__ = 'complaints'
    columns = ['id', 'agency', 'agency_name', 'complaint_type', 'descriptor']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise f'{key} not in {self.columns}' 
        for k, v in kwargs.items():
            setattr(self, k, v)


    @classmethod
    def find_by_complaint_type(self, name, cursor):
        complaint_query = """SELECT * FROM complaints 
        WHERE complaint_type = %s """
        cursor.execute(complaint_query, ('complaint_type',))
        complaint_record =  cursor.fetchone()
        complaint = db.build_from_record(self, complaint_record)
        return complaint 

    @classmethod
    def find_or_create_complaint_type(self, name, conn, cursor):
        complaint = self.find_by_complaint_type(name, cursor)
        if not complaint:
            new_complaint = models.Complaint()
            new_complaint.name = name
            db.save(new_complaint, conn, cursor)
            complaint = self.find_by_complaint_type(name, cursor)
        return complaint 

    #calculates complaint totals gourped by complaint type
    def total_by_complaint_type(self, cursor):
        complaint_type_query = """SELECT complaint_type, COUNT(*) FROM complaints
        JOIN incidents ON complaints.id = incidents.complaint_id
        GROUP BY complaint_type"""
        cursor.execute(complaint_type_query)
        record = cursor.fetchall()
        return record

    #calculates total complaints handled by each agency
    def total_complaints_by_agency(self, cursor):

        agency_query = """SELECT agency_name, COUNT(*) FROM complaints 
        JOIN incidents ON complaints.id = incidents.complaint_id 
        GROUP BY agency_name"""
        cursor.execute(agency_query)
        record = cursor.fetchall()
        return record

    #calculates total by complaint type, example: NYPD -> will return {'name': 'NYPD', 'complaint_total': 500}
    # yuh oh, don't think this works.  Where is agency_name used?
    @classmethod
    def complaint_type_total_by_agency(agency_name):
        complaint_total_query = """SELECT complaint_type, COUNT(*) FROM complaints
        WHERE agency_name = %s"""
        cursor.execute(complaint_total_query)
        record = cursor.fetchall()
        return record
