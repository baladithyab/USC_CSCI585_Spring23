-- DB => postgresql on supabase
-- Find unique user/s with the total number of paid subscribers greater than 100 for their channel/s created on 01.01.2023. Display the username, email, channel name and the subscriber count.
-- Explanation: We join users and their respective channels and filter by date. We also filter using a subquery to count the total number of paid subscriptions per channel from the overall subscriptions table. I could have joined the subscriptions table but eh. I went with this cause this also works and keeps the tuples generated small.

SELECT u.name, u.email, c.name AS channel_name, c.subscription_count
FROM users u
JOIN channels c ON u.user_id = c.owner_id
WHERE c.created_on = '2023-01-01'
AND (
    SELECT COUNT(*)
    FROM subscriptions s
    WHERE s.channel_id = c.channel_id AND s.subscription_type = 'paid'
) > 100;