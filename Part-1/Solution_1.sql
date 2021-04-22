-- Can join with transaction table and then use a group by with user_id to see user level items and locations.

DROP TABLE IF EXISTS game_item_locations;

CREATE TABLE game_item_locations (
item_id uuid,
transaction_id uuid, 
location_id uuid,
user_id uuid,
PRIMARY KEY(item_id, transaction_id, location_id),
CONSTRAINT fk_item FOREIGN KEY(item_id) REFERENCES game_items(id),
CONSTRAINT fk_user FOREIGN KEY(transaction_id) REFERENCES transactions(id),
CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES locaitions(id)
);