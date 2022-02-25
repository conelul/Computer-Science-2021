#!/usr/bin/env python3
import sqlite3 as sql


class DBHelper:
    def connect(self, database="crimemap.sqlite3") -> sql.Connection:
        return sql.connect(database)

    def get_all_inputs(self) -> list:
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            cursor = connection.execute(query)
            return sql.Cursor.fetchall(cursor)
        finally:
            connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (?);"
            connection.execute(query, data)
            connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            connection.execute(query)
            connection.commit()
        finally:
            connection.close()

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, latitude, longitude, description) VALUES (?, ?, ?, ?, ?)"
            connection.execute(
                query, (category, date, latitude, longitude, description)
            )
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

    def get_all_crimes(self):
        connection = self.connect()
        try:
            query = (
                "SELECT latitude, longitude, date, category, description FROM crimes;"
            )
            cursor = connection.execute(query)
            named_crimes = []
            for crime in cursor:
                named_crime = {
                    "latitude": crime[0],
                    "longitude": crime[1],
                    "date": crime[2],
                    "category": crime[3],
                    "description": crime[4],
                }
                named_crimes.append(named_crime)
            return named_crimes
        finally:
            connection.close()
