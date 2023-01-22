@user.get('/')
async def find_all_users():
    return serializeList(client.testingwb.profile.find())

@user.get('/{id}')
async def find_one_user(id):
        return serializeDict(client.testingwb.profile.find_one_and_delete({"_id": ObjectId(id)}))

@user.post('/')
async def create_user(user: User):
    client.testingwb.profile.insert_one(dict(user))
    return serializeList(client.testingwb.profile.find_one())

@user.put('/{id}')
async def update_user(id,user: User):
    client.testingwb.profile.find_one_and_update({"_id":ObjectId(id)},{
        "$set":dict(user)
    })
    return serializeDict(client.testingwb.profile.find_one({"_id":ObjectId(id)}))

@user.delete('/{id}')
async def delete_user(id,user: User):
    return serializeDict(client.testingwb.profile.find_one_and_delete({"_id":ObjectId(id)}))




return serializeList(client.testingwb.profile.find({"active": True}))




