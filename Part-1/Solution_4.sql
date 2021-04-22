-- Flatten the transaction table to derive all items received by user. Do the same to get all items spent by user. The first table is then left joined with second table to generate another temp table which has
-- user, item, and total count of each item. Use library function to group this final view by user_id and generate player state for each user.

select USER, jsonb_object_agg(items, total_balance) as player_state
from 
(
select received_items.usr as USER, received_items.key as items, received_items.RECEIVED - CASE(WHEN spent_items.ITEM IS NULL then 0 else spent_items.ITEM) as total_balance

(select t.user_id as usr, r.key as ITEM, sum(CAST(r.value as INTEGER)) as RECEIVED
from transactions as t
JOIN json_each_text(t.received) as r
group by t.user_id, r.key) received_items

left join 

(select t.user_id as usr, s.key as ITEM, sum(CAST(s.value as INTEGER)) as SPENT
from transactions as t
JOIN json_each_text(t.spent) as s
where t.spent IS NOT NULL
group by t.user_id, s.key) spent_items

on received_items.usr = spent_items.usr and received_items.ITEM = spent_items.ITEM
)
group by 1;