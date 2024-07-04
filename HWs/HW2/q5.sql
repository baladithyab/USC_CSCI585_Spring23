-- DB => postgresql on supabase
-- Find the minimum and maximum age of viewers who watched the most commented on video on Taylor Swift’s channel. Display the video title, minimum age and the maximum age.
-- Explanation: We join the videos, comments, channels, and users table to make sure we get tuples with the data we need and not any tuples where the data isnt related. then we use a subquery to find the user_id of the user with the name 'Taylor Swift' and match that to the tuples we already have. then we group by video so we can show that we have tuples of video and a count of comments. by ordering DESC we can get the top one which is the most commented video.

SELECT v.title AS video_title, MIN(u.age) AS min_age, MAX(u.age) AS max_age
FROM videos v
JOIN channels c ON v.channel_id = c.channel_id
JOIN comments co ON v.video_id = co.video_id
JOIN users u ON co.user_id = u.user_id
WHERE c.owner_id = (SELECT user_id FROM users WHERE name = 'Taylor Swift')
GROUP BY v.video_id
ORDER BY COUNT(*) DESC
LIMIT 1;

