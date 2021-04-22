-- CTE to pull out user and locations where they hold items in. Joins game item location table with location table to find mappings of transactions and locations, then joins the result with transaction table and groups by -- user id, location id and location geometry to create groups of user and locations where they have items.

with user_item_locations(user_id, geom_point) as
(select t.user_id, l.geom
from game_item_locations g_l join locations l on g_l.location_id = l.id 
join transactions t on t.id = g_l.transaction_id
group by t.user_id, l.id, l.geom) 

-- Using the above CTE, we join user_item_locations with location to find which locations have user items. The filter uses library function ST_Distance_Sphere to join the 2 tables using a non-equality join.
select uil.user_id, l.geom
from location as l join user_item_locations as uil
where ST_Distance_Sphere(l.geom, uil.geom_point) <= 3000
order ST_Distance_Sphere(l.geom, uil.geom_point) desc;