-- Method 1
select user_id as User, count(id) as Woodpeckers_Received
from transactions 
where lower(display_name) = 'downy woodpecker'
group by user_id
having count(id) = (select max(count(id)) from transactions where lower(display_name) = 'downy woodpecker' group by user_id);

-- Method 2
select User, Woodpeckers_Received
from
(select user_id as User, count(id) as Woodpeckers_Received, rank() over (order by count(id) desc) as Rank_Received
from transactions 
where lower(display_name) = 'downy woodpecker'
group by user_id)
where Rank_Received = 1;
