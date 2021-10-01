import motor.motor_asyncio
from server.models.rackmodel import Rack, RackUpdate, Growcycle
from server.models.rackautomationmodel import RackAutomationTimer, RackAutomationSwicht
from bson import ObjectId
from datetime import datetime

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')  # mongodb uri
db = client.microstation    # mongodb database
collection = db.rack        # mongodb collection
# collection = sensor.rack        # mongodb collection

# fetch rack by id  in database
async def get_rack_id(rack_id):
    document = await collection.find_one({"_id": ObjectId(rack_id)})  
    return document

# fetch all rack by id in database
async def get_all_racks_id():                                        
    racks_id = []
    cursor = collection.find({})
    async for document in cursor:
        racks_id.append(Rack(**document))
    return racks_id


# save new rack in database                                          
    racks_id = []          
async def add_new_rack(data_rack):
    document = data_rack
    result = await collection.insert_one(document)
    return document


# update rack items in database                                        
async def update_rack_items(rack_id,  model):
    print(model)
    await collection.update_one({"_id": ObjectId(rack_id)}, {"$set": model})
    document = await collection.find_one({"_id": ObjectId(rack_id)})
    return document


# remove rack in database                                              
async def delete_rack(rack_id):
    await collection.delete_one({"_id": ObjectId(rack_id)})
    return True


# save sensor data by rackid in database                                
async def save_sensor_data(rack_id, data, schedule):
    timenow = datetime.now()
    if timenow == schedule:
        document = dict(data)
        result = await collection.insert_one({"rack_id": (rack_id)}, document)
        

# add automations by rackid
async def save_automation(rack_id, model):
    automation = model
    await collection.update_one({"_id": ObjectId(rack_id)}, {"$set": model})
    document = await collection.find_one({"_id": ObjectId(rack_id)})
    return document