import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2

# remove comments from this file
#run Client and Builder (from incident_builder) to retrieve and configure data
class RequestAndBuild:
    def __init__(self):
        self.client = adapters.Client()
        self.builder = adapters.Builder()
        # read these values of database, and user from settings.py, which reads from .env
        self.conn = psycopg2.connect(database = 'three_one_one_development', 
                user = 'robertsawyer')
        self.cursor = self.conn.cursor()

    def run(self, search_params):
        incidents = self.client.request_incidents(search_params) #request_incidents from Client
        incident_objs = []
        for incident in incidents:
            incident_details = self.client.request_incidents()
            incident_obj = self.builder.run(incident_details, self.conn, self.cursor)
            incident_objs.append(incident_obj)
        return incident_objs

