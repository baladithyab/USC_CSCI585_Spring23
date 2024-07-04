-- DB => postgresql on supabase
-- Find the ratio of likes to views of each video belonging to any of the channels owned by users having the word “Marvel Entertainment” in them. Display the Video Title, channel name and the ratio in the ascending order of the title.
-- Explanation: We join videos, channels, and video statistics to get the tuples with all the information we need. then we filter by the channel name for the one we are looking for and finally order by the title alphabetically.

SELECT v.title, c.name, (cast(vs.likes as decimal)/vs.view_count) AS ratio_likes_to_views
FROM videos v
JOIN channels c ON v.channel_id = c.channel_id
JOIN video_statistics vs ON v.video_id = vs.video_id
WHERE c.name LIKE '%Marvel Entertainment%'
ORDER BY v.title ASC;