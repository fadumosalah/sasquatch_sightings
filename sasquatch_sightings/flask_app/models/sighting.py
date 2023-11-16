from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

db = "sasquatch_sightings_schema"

class Sighting:
    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data ['date']
        self.amount = data['amount']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
        self.sightors = None


    @classmethod
    def get_all (cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(db).query_db(query)
        sightings = []
        for sighting in results:
            sightings.append(cls(sighting))
        return sightings

    @classmethod
    def create_sighting(cls, data):
        query = """
            INSERT INTO sightings (location, description, date, amount, user_id) 
            VALUES ( %(location)s, %(description)s, %(date)s, %(amount)s, %(user_id)s);
            """
        return connectToMySQL(db).query_db(query,data)


    @staticmethod
    def validate_sighting(sighting):
        is_valid = True # we assume this is true
        if len(sighting['location']) < 1:
            flash("Location must be at least 2 characters.")
            is_valid = False
        if len(sighting['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False
        if int(sighting['amount']) < 1:
            flash("Number of Sasquatches must be a min of 1")
            is_valid = False
        return is_valid
    
    
    @classmethod
    def get_sighting(cls, data):
        query = """
            SELECT * FROM sightings
            JOIN users ON users.id = sightings.user_id
            WHERE sightings.id = %(id)s;
            """
        results = connectToMySQL(db).query_db(query,data)
        sighting = cls(results[0])
        sightor_data ={
            "id" : results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["users.created_at"],
            "updated_at": results[0]["users.updated_at"]
        }
        sighting.sightor = User(sightor_data)
        return sighting

    @classmethod
    def updatesighting(cls, form_data, sighting_id):
        query = f"UPDATE sightings SET location = %(location)s, description = %(description)s, date = %(date)s, amount = %(amount)s WHERE id = {sighting_id};"
        return connectToMySQL(db).query_db(query,form_data)
    
    @classmethod
    def delete_sighting(cls,data):
        query = "DELETE FROM sightings WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query,data)
    

    @classmethod
    def get_sightings_with_users(cls, data):
        query = "SELECT * FROM sightings LEFT JOIN users ON sightings.user_id = users.id "
        results = connectToMySQL(db).query_db(query, data)
        all_sightings =[]
        user_class = cls(results[0])
        for row_from_db in results:
            user_data = {
                "id": row_from_db['id'],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "email": row_from_db["email"],
                "password": row_from_db["password"],
                "created_at": row_from_db["created_at"],
                "updated_at": row_from_db["updated_at"]
            }
            user_class.sighting= User(user_data)
            all_sightings.append(user_class)
        return all_sightings

# Missing something. Only shows the first row and repeats it

