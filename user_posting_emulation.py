import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text


random.seed(100)


class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()


def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
            
            print(pin_result)
            print(geo_result)
            print(user_result)

            # invoke urls for each topic
            invoke_url_pin = "https://4ulz8vmg76.execute-api.us-east-1.amazonaws.com/test/topics/0ed442ca38ad.pin"
            invoke_url_geo = "https://4ulz8vmg76.execute-api.us-east-1.amazonaws.com/test/topics/0ed442ca38ad.geo"
            invoke_url_user = "https://4ulz8vmg76.execute-api.us-east-1.amazonaws.com/test/topics/0ed442ca38ad.user"

            # payloads for each topic
            payload_pin = json.dumps({
                "records": [
                    {"value": pin_result}]
            })

            payload_geo = json.dumps({
                "records": [
                    {"value": geo_result}]
            }, 
                default = str)

            payload_user = json.dumps({
                "records": [
                    {"value": user_result}]
            }, 
                default = str)
            
            # post requests for each topic
            headers = {'Content-Type': 'application/vnd.kafka.json.v2+json'}
            response_pin = requests.post(invoke_url_pin, headers=headers, data = payload_pin)
            response_geo = requests.post(invoke_url_geo, headers=headers, data = payload_geo)
            response_user = requests.post(invoke_url_user, headers=headers, data = payload_user)

            # response codes
            print(f"pin: {response_pin.status_code}")
            print(f"geo: {response_geo.status_code}")
            print(f"user: {response_user.status_code}")


if __name__ == "__main__":
    run_infinite_post_data_loop()
    print('Working')


