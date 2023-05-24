import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()


class Dog:
    all = []

    def __init__(self, name, breed) -> None:
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        sql = '''
        CREATE TABLE IF NOT EXISTS 
        dogs(id INTEGER PRIMARY KEY, name TEXT, breed TEXT)
        '''
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS dogs")

    def save(self):
        sql = '''
        INSERT INTO dogs(name, breed) VALUES (?, ?)
        '''

        CURSOR.execute(sql, (self.name, self.breed))
        self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = '''
        SELECT *
        FROM dogs
        '''
        all = CURSOR.execute(sql).fetchall()
        x = [cls.new_from_db(row) for row in all]
        return x

    @classmethod
    def find_by_name(cls, name):
        sql = '''SELECT * FROM dogs WHERE name = ? LIMIT 1'''
        x = CURSOR.execute(sql, (name,)).fetchone()
        if x == None:
            dog = None
        else:
            dog = cls.new_from_db(x)
        return dog

    @classmethod
    def find_by_id(cls, id):
        sql = '''SELECT * FROM dogs WHERE id = ? LIMIT 1'''
        x = CURSOR.execute(sql, (id,)).fetchone()
        dog = cls.new_from_db(x)
        return dog

    @classmethod
    def find_or_create_by(cls, name, breed):
        sql = '''SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1'''
        x = CURSOR.execute(sql, (name, breed)).fetchone()
        if x is None:
            dog = cls.create(name, breed)
        else:
            dog = cls.new_from_db(x)
        return dog

    def update(self):
        sql = '''UPDATE dogs SET name = ?, breed = ? WHERE id = ?'''
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()



