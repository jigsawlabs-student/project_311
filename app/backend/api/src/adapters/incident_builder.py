import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2


class Builder:
    def run(self, incident_details, conn, cursor):
        incident = IncidentBuilder().run(incident_details, conn, cursor)
        if incident.exists:
            return {'incident': incident, 'location': incident.location(cursor), 
                    'complaint': incident.complaint(cursor)}
        else:
            location = LocationBuilder().run(incident_details, conn, cursor)
            complaint = ComplaintBuilder().run(incident_details, conn, cursor)
            return {'incident': incident, 'location': location, 'complaint': complaint}


class IncidentBuilder:
    attributes = ['open_data_id', 'date_time']

    def select_attributes(self, incident_details):
        open_data_id = incident_details['unique_key']
        date_time = incident_details['created_date']
        return dict(zip(self.attributes, [open_data_id, date_time]))

    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        open_data_id = selected['unique_key']
        incident = models.Incident.find_by_open_data_id(open_data_id, cursor)
        if incident:
            incident_details.exists = True
            return incident_details
        else:
            incident_details = db.save(models.Incident(**selected), conn, cursor)
            incident.exists = False
            return incident


class LocationBuilder:
    attributes = ['setting', 'zip_code', 'incident_address', 'city', 
    'borough', 'latitude', 'longitude']

    def select_attributes(self, incident_details):
        setting = incident_details['location_type']
        zip_code = incident_details['incident_zip']
        incident_address = incident_details['incident_address']
        city = incident_details['city']
        borough = incident_details['borough']
        latitude = incident_details['latitude']
        longitude = incident_details['longitude']
        # for this, may be able to refactor as 
        # {k:v for select_attributes.items() if k in self.attributes}
        # maybe not
        return dict(zip(self.attributes, [setting, zip_code, incident_address,
        city, borough, latitude, longitude]))

    def run(self, incident_details, conn, cursor):
        location_attributes = self.select_attributes(incident_details)
        location = models.Location(**location_attributes)
        location = db.save(location, conn, cursor)
        return location


class ComplaintBuilder:
    def select_attributes(self, incident_details):
        complaints = [complaint['complaint_type'] for complaint in incident_details]
        return complaints

    def run(self, incident_details, conn, cursor):
        complaint_types = self.select_attributes(incident_details)
        complaints = self.find_or_create_complaint_types(complaint_types, conn, cursor)

    def find_or_create_complaint_types(self, incident_details, conn, cursor):
        type_of_complaints =[]
            # probably should move this db.total_by_complaint_type function to the complaint class, as a class method
        # yuh oh, where is complaint_type defined?
        # also not sure that should be calculating these aggregate functions here (total_by_complaint_type), and then storing in db.  
        # talk to me about this.
        for complaint_type in incident_details:
            named_complaint = db.total_by_complaint_type(models.Complaint, conn, cursor)
            type_of_complaints.append(named_complaint)
        return type_of_complaints
        
         
