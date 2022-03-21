from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Thought:

    db_name = "thought_schema"

    def __init__(self,data):
        self.id = data['id']
        self.thought = data['thought']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None
        self.users_who_like = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM thoughts;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results

    @classmethod 
    def create_thought(cls, data):
        query = "INSERT INTO thoughts (thought, user_id) VALUES (%(thought)s, %(user_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_one(cls, data):
        all_thoughts = []
        query = "SELECT * FROM thoughts WHERE user_id = %(user_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for result in results:
            all_thoughts.append(result)
        print(all_thoughts)
        return all_thoughts
    @classmethod
    def update_thought(cls, data):
        query = "UPDATE thoughts SET thought = %(thought)s, WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def like(cls, data):
        query = "INSERT INTO likes (user_id, thought_id) VALUES (%(user_id)s, %(thought_id)s);"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results
    
    @classmethod
    def unlike(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND thought_id = %(thought_id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_all_likes(cls, data):
        all_likes = []
        query = "SELECT thought_id FROM likes JOIN users ON users.id = likes.user_id WHERE user_id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for result in results:
            all_likes.append(result['thought_id'])
        return all_likes
    
    @classmethod
    def show_all_thoughts(cls):
        query = "SELECT thoughts.thought, thoughts.id, users.first_name, users.id AS user, likes.thought_id, COUNT(likes.thought_id) AS likes FROM thoughts "\
                "LEFT JOIN users ON users.id = thoughts.user_id "\
                "LEFT JOIN likes ON thoughts.id = likes.thought_id "\
                "GROUP by thoughts.id "\
                "ORDER BY COUNT(likes.thought_id) DESC;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        return results
        
    @classmethod
    def destroy_thought(cls, data):
        query = "DELETE FROM thoughts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results

    @classmethod
    def get_thought_and_user(cls):
        query = "SELECT * FROM thoughts LEFT JOIN users ON users.id = thoughts.user_id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return results

    @staticmethod
    def validate_thought(thought):
        is_valid = True
        if len(thought['thought']) < 5:
            is_valid = False
            flash("Thought must be at least 5 characters","thought")
        return is_valid

    @classmethod
    def getAll_likes(cls, data):
        all_thoughts = []
        query = "SELECT * FROM likes WHERE thought_id = %(thought_id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        for result in results:
            all_thoughts.append(result)
        print(all_thoughts)
        return all_thoughts