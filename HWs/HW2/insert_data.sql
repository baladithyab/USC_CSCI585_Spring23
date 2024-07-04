-- DB => postgresql on supabase
-- Insert 1000 users with random information
INSERT INTO users (user_id, name, email, age, address)
SELECT uuid_generate_v4(), 
       CONCAT('user_', i), 
       CONCAT('user_', i, '@example.com'), 
       floor(random() * 50) + 18, 
       CASE round(random()*5)
       WHEN 0 THEN CONCAT('Address ', i,' USA')
       WHEN 1 THEN CONCAT('Address ', i,' CA')
       WHEN 2 THEN CONCAT('Address ', i,' US')
       WHEN 3 THEN CONCAT('Address ', i,' UK')
       WHEN 4 THEN CONCAT('Address ', i,' SP')
       WHEN 5 THEN CONCAT('Address ', i,' RU')
       END
FROM generate_series(1, 1000) as i;

-- Insert Taylor Swift user
INSERT INTO users (user_id, name, email, age, address)
VALUES (uuid_generate_v4(), 'Taylor Swift', 'taylor.swift@example.com', 32, 'Nashville, Tennessee, USA');

-- Insert channels with random information
INSERT INTO channels (channel_id, name, owner_id, subscription_count, created_on)
SELECT uuid_generate_v4(),
       concat('channel_', i),
       (SELECT user_id FROM users ORDER BY random() LIMIT 1),
       floor(random() * 1000),
       DATE (now() - random() * (TIMESTAMP '2023-01-01 00:00:00' - TIMESTAMP '2020-01-01 00:00:00'))
FROM generate_series(1, 10) as i;

-- Insert a channel created on '2023-01-01'
INSERT INTO channels (channel_id, name, owner_id, subscription_count, created_on)
SELECT uuid_generate_v4(), 'channel_created_on_2023-01-01', 
       (SELECT user_id FROM users ORDER BY random() LIMIT 1), 
       floor(random() * 1000), '2023-01-01';

-- Insert a Taylor Swift channel owned by a user named Taylor Swift
WITH ts AS (SELECT user_id FROM users WHERE name = 'Taylor Swift')
INSERT INTO channels (channel_id, name, owner_id, subscription_count, created_on)
SELECT uuid_generate_v4(), 'Taylor Swift Channel', ts.user_id, 
       floor(random() * 1000), CURRENT_DATE
FROM ts;

-- Insert a Marvel Entertainment channel
INSERT INTO channels (channel_id, name, owner_id, subscription_count, created_on)
SELECT uuid_generate_v4(), 'Marvel Entertainment Channel', 
       (SELECT user_id FROM users ORDER BY random() LIMIT 1),
       floor(random() * 1000), CURRENT_DATE;

-- Insert subscriptions for each channel with a mix of free and paid subscriptions
INSERT INTO subscriptions (subscriber_id, channel_id, subscription_type)
SELECT u.user_id, c.channel_id,
    CASE WHEN random() < 0.5 THEN 'paid' ELSE 'free' END AS subscription_type
FROM users u
CROSS JOIN channels c
WHERE u.user_id != c.owner_id AND random() < 0.5;


UPDATE channels c
SET subscription_count = (
    SELECT COUNT(*)
    FROM subscriptions s
    WHERE s.channel_id = c.channel_id
);

-- generate 50 videos for each channel
INSERT INTO videos (video_id, url, title, channel_id, thumbnail_url, category, keyword, tag, duration, description, uploader_id, upload_date, upload_time)
SELECT uuid_generate_v4(), CONCAT('https://www.youtube.com/watch?v=', i), CONCAT(c.name,' Video ', i), c.channel_id, CONCAT('https://www.youtube.com/thumbnail?v=', i), 
    CASE WHEN random() < 0.5 THEN 'entertainment' ELSE 'informational' END, 
    CASE round(random()*5)
         WHEN 0 THEN 'math'
         WHEN 1 THEN 'chemistry'
         WHEN 2 THEN 'physics'
         WHEN 3 THEN 'compsci'
         WHEN 4 THEN 'economics'
         WHEN 5 THEN 'english'
         END, 
    CASE round(random()*5)
         WHEN 0 THEN 'diy'
         WHEN 1 THEN 'game'
         WHEN 2 THEN 'reddit'
         WHEN 3 THEN 'tiktok'
         WHEN 4 THEN 'minecraft'
         WHEN 5 THEN 'dnd'
         END, 
    random() * (TIME '01:00:00' - TIME '00:00:00'), 
    'Lorem ipsum dolor sit amet', 
    c.owner_id, 
    DATE (now() - random() * (TIMESTAMP '2023-04-01 00:00:00' - TIMESTAMP '2022-08-01 00:00:00')),
    TIME '00:01:00'
FROM channels c, generate_series(1, 50) as i;

-- generate video statistics for each video
INSERT INTO video_statistics (video_id, likes, dislikes, view_count, share_count)
SELECT v.video_id, floor(random() * 1000), floor(random() * 100), floor(random() * 100000), floor(random() * 100)
FROM videos v;

-- generate random number of comments for each video
INSERT INTO comments (comment_id, video_id, user_id, text, likes, sentiment, commented_on)
SELECT uuid_generate_v4(), v.video_id, u.user_id, 
    'Lorem ipsum dolor sit amet', 
    floor(random() * 100), random(), (now() - random() * (TIMESTAMP '2023-01-01 00:00:00' - TIMESTAMP '2020-01-01 00:00:00'))
FROM videos v, users u
WHERE random() < 0.6; -- 60% chance of generating a comment for each video

INSERT INTO sponsors (sponsor_id, name, phone, address)
SELECT uuid_generate_v4(), CONCAT('Sponsor ', i), CONCAT(floor(random() * 999),'-',floor(random() * 999),'-', floor(random() * 9999)), CONCAT(floor(random() * 999),'Sponsor Ave')
FROM generate_series(1, 200) as i;

-- generate random number of sponsors for each video
INSERT INTO sponsored_videos (video_id, sponsor_id, amount)
SELECT v.video_id, s.sponsor_id, floor(random() * 10000)
FROM videos v, sponsors s
WHERE random() < 0.4;
