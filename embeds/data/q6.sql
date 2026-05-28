-- DB => postgresql on supabase
-- Find all the content creators living in the US who have consistently posted at least 1 video each week of the last month. Display their username, channel/s they own and their total subscriber count.
-- Explanation: We use the users table as a source of truth and find the channels that this user owns. Then we join a subquery where we look for videos that have been made within the last month. Grouping by uploader_id allows us to return just the id that we can join with the tuples in the "super"-query. We add a having clause to make sure that the distinct dates that have been truncated to show the week it is part of is greater than 4. This way we can make sure the channel has uplaoded at least 4 videos within the past month with at least 1 per week.

SELECT u.name AS username, c.name AS channel_name, c.subscription_count
FROM users u
JOIN channels c ON u.user_id = c.owner_id
JOIN (
    SELECT v.uploader_id, COUNT(*) AS video_count
    FROM videos v
    WHERE v.upload_date >= CURRENT_DATE - INTERVAL '1 month'
    GROUP BY v.uploader_id
    HAVING count(DISTINCT date_trunc('week', v.upload_date)) >= 4
) vu ON u.user_id = vu.uploader_id
WHERE u.address LIKE '%US%'
