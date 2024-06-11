from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask_bcrypt import Bcrypt



client = MongoClient('localhost', 27017)
db = client['chatDB']
users = db['users']
rooms = db['rooms']
room_members = db['room_members']
messages = db['messages']


def save_user(username, email, phone, password):
    hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')
    users.insert_one({
        'username': username,
        'email': email,
        'phone': phone,
        'password': hashed_password
    })
    # print(save_user('username', 'email', 'phone', 'password'))




def get_user(phone):
    return users.find_one({'phone': phone})

    
    

def get_username(username):
    return users.find_one({'username': username})



def update_user(user_id, username, email, phone):
    return users.update_one({'_id': ObjectId(user_id)}, {'$set': {'username': username, 'email': email, 'phone': phone}})


def get_user_by_id(user_id):
    return users.find_one({'_id': ObjectId(user_id)})



def save_room(room_name, creator):
    room_id = rooms.insert_one({'room_name': room_name, 'creator': creator, 'created_at': datetime.now()}).inserted_id
    phone = get_user_by_id(creator)['phone']
    print(phone)
    add_room_member(room_id, room_name, phone, creator, is_admin=True)
    return room_id



def update_room(room_id, room_name):
    rooms.update_one({'_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})
    room_members.update_many({'_id.room_id': ObjectId(room_id)}, {'$set': {'room_name': room_name}})



def get_room(room_id):
    return rooms.find_one({'_id': ObjectId(room_id)})



def save_message(room_id, sender, message):
    messages.insert_one({'room_id': ObjectId(room_id), 'sender': sender, 'message': message, 'sent_at': datetime.now()})



def get_message(room_id):
    return list(messages.find({'room_id': ObjectId(room_id)}))



def get_messages(room_id):
    messages.find({'room_id': ObjectId(room_id)})
    for message in messages:
        message['sent_at'] = message['sent_at'].strftime('%Y-%m-%d %H:%M')




def add_room_member(room_id, room_name, phone, added_by, is_admin=False):
    room_members.insert_one({'_id': {'room_id': ObjectId(room_id), 'phone': phone},
                            'room_name': room_name, 'added_by': added_by,
                            'is_admin': is_admin, 'joined_at': datetime.now()})
    


def add_room_members(room_id, room_name, phones, added_by):
    for phone in phones:
        add_room_member(room_id, room_name, phone, added_by)



def remove_room_members(room_id, phones):
    room_members.delete_many({'_id': {'$in': [{'room_id': ObjectId(room_id), 'phone': phone} for phone in phones]}})



def get_room_member(room_id, phone):
    return room_members.find_one({'_id': {'room_id': ObjectId(room_id), 'phone': phone}})


def get_room_members(room_id):
    members = room_members.find({'_id.room_id': ObjectId(room_id)})
    return [member['_id']['phone'] for member in members]

    


def remove_room_members(room_id, usernames):
    room_members.delete_many(
        {'_id': {'$in': [{'room_id': ObjectId(room_id), 'username': username} for username in usernames]}})



def get_user_rooms(phone):
    room_members.find({'_id.phone': phone})



def is_room_member(room_id, phone):
    return room_members.count_documents({'_id': {'room_id': ObjectId(room_id), 'phone': phone}})



def is_room_admin(room_id, phone):
    return room_members.count_documents(
        {'_id.room_id': ObjectId(room_id), 'is_admin': True, '_id.phone': phone}
    )