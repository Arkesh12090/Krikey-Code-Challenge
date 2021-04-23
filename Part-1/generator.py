import uuid
import psycopg2
from config import config
import random
import json

'''
This script will generate 100 unique user ids, and 5000 unique rows for location, transaction and game_item_location tables.
'''


all_transactions = {} # To keep track of userid and transactionid mappings
all_locations = {} # To keep track of userid and location id mappings
all_items = {} # To keep track of userid and itemid mappings


# SQL strings for insert statements.
location_sql = '''\
INSERT INTO locations(id, geom)
VALUES(%s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
'''

transaction_sql = '''\
INSERT INTO transactions(id, user_id, received, spent)
VALUES(%s, %s, %s, %s);
'''

game_item_sql = '''\
INSERT INTO game_item_locations(item_id, transaction_id, location_id, user_id)
VALUES(%s, %s, %s, %s);
'''


# Get connection to execute sql statements
def get_cursor():
	try:
	    connection = psycopg2.connect(user="user",
	                                  password="pwd",
	                                  host="127.0.0.1",
	                                  port="5432",
	                                  database="postgres_db")
	    cursor = connection.cursor()
	    return connection, cursor

	except (Exception, psycopg2.Error) as error:
	    print("Failed to insert record into mobile table", error)
	    return -1

# Close connection
def close_conenction(conn, cursor):
	if conn:
		cursor.close()
		conn.close()

# Generate UUID
def generate_uuid():
	'''
	This method will generate time uuids.
	'''
	return uuid.uuid4()

def get_users():
	'''
	This method will generate 100 unique users.
	'''
	users = []
	for i in range(100):
		users.append(generate_uuid())
	return users

def store_item(user_id, id):
	'''
	This method will keep track of user id and item id mappings.
	'''
	if user_id in all_transactions:
		all_items[user_id].append(id)
	else:
		all_items[user_id] = []
		all_items[user_id].append(id)

def store_transaction(user_id, id):
	'''
	This method will keep track of user id and transaction id mappings.
	'''
	if user_id in all_transactions:
		all_transactions[user_id].append(id)
	else:
		all_transactions[user_id] = []
		all_transactions[user_id].append(id)

def store_location(user_id, id):
	'''
	This method will keep track of user id and location id mappings.
	'''
	if user_id in all_transactions:
		all_transactions[user_id].append(id)
	else:
		all_transactions[user_id] = []
		all_transactions[user_id].append(id)


def generate_transactions(users):
	'''
	For each userid in the users list, this method will generate 500 unique transactions.
	'''
	transactions = []
	for user_id in users:
		for i in range(500):
			received = {}
			spent = {}
			id = generate_uuid()

			received_id = generate_uuid() # Received item
			spent_id = generate_uuid() # Spent item

			received[received_id] = random.randint(1, 10)
			spent[spent_id] = random.randint(1, 3)

			received_json = json.dumps(received)
			spent_json = json.dumps(spent)

			store_items(user_id, received_id)
			store_items(user_id, spent_id)

			transactions.append((id, user_id, received_json, spent_json))

			store_transaction(user_id, id)
	return transactions

def generate_locations(users):
	'''
	For each user id this method will generate 500 unique locations.
	'''
	locations = []
	for user_id in users:
		for i in range(500):
			id = generate_uuid()
			lng1, lat1 = random.randrange(-18000, 18000)/100, random.randrange(-9000, 9000)/100
			loc_lst = [(lng1, lat1)]
			row = [(id, loc_lst)]
			locations.append(row)

			store_location(user_id, locations)
	return locations


def generate_item_locations(users):
	'''
	For each itemid, locationid and transactionid mapping, this method will generate an unique game item location.
	'''
	item_locations = []
	for user_id in users:
		locations = all_locations[user_id]
		transactions = all_transactions[user_id]
		items = all_items[user_id]
		j = 0
		for i in range(500):
			item_locations.append((items[j], transactions[i], locations[i], user_id))
			j += 1
			item_locations.append((items[j], transactions[i], locations[i], user_id))
			j += 1
	return item_locations

def load_game_locations(locations):
	'''
	Dumps all locations into the db.
	'''
	conn, cursor = get_cursor()
	for loc in locations:
		id, point = loc
		lat, lng = point
		insert_record = (id, lat, lng)
		cursor.execute(location_sql, insert_record)
	close_connection(conn, cursor)

def load_transactions(transactions):
	'''
	Dumps all transactions into the db.
	'''
	conn, cursor = get_cursor()
	for tx in transactions:
		cursor.execute(transaction_sql, tx)
	close_connection(conn, cursor)

def load_game_item_locations(game_item_locations):
	'''
	Dumps all game_item_locations into the db.
	'''
	conn, cursor = get_cursor()
	for gil in game_item_locations:
		cursor.execute(game_item_sql, gil)
	close_connection(conn, cursor)


# Entry point of the script.
if __name__ == "__main__":
    users = get_users()
	transactions = generate_transactions(users)
	locations = generate_locations(users)
	item_locations = generate_item_locations(users)

	load_transactions(transactions)
	load_game_locations(locations)
	load_game_item_locations(item_locations)




