import boto3
import json
from random import randrange
import uuid

TABLE_NAME = "tablename"
names = open("names.txt", "r").readlines()
lastnames = open("names.txt", "r").readlines()

#structure: uuid, name, lastname, birthdate
def lambda_handler(event, context):
    print(event)
    if(event.get('ACTION') == "PREPARE"):
        load = int(int(event.get('LOAD'))/1000)
        items = []
        for i in range(load):
            items.append(i)
        return {'items': items}
        
    elif(event.get('ACTION') == "RUN"):
        for i in range(50):
            items = []
            for j in range(20):
                id = uuid.uuid1()
                name = names[randrange(0, len(names)-1, 2)]
                lastname = lastnames[randrange(0, len(lastnames)-1, 2)]
                date = str(randrange(1900, 2000, 2)) + "/" + str(randrange(1, 12, 2)) + "/" + str(randrange(1, 28, 2))
                items.append({
                    "uuid": str(id),
                    "name": name,
                    "lastname": lastname,
                    "birthdate": date
                })
            print(items)
            putItemsDynamo(TABLE_NAME, items)
        return {'processed': 1000}

def putItemsDynamo(TABLE_NAME, items):
    client = boto3.client('dynamodb')
    itemsPut = []
    for i in items:
        itemsPut.append({"PutRequest": { 
            "Item": {
                'uuid': {
                    'S': i['uuid'],
                },
                'name': {
                    'S': i['name'],
                },
                'lastname': {
                    'S': i['lastname'],
                },
                'birthdate': {
                    'S': i['birthdate'],
                }
            }
        }})
    request = {}
    request[TABLE_NAME] = itemsPut
    response = client.batch_write_item(RequestItems=request)