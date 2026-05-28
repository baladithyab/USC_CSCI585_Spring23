-- DB => postgresql on supabase
-- Find the average sentiment score for each keyword category. Display the keyword name along with average score such that the highest score is displayed first.
-- Explanation: We join videos and comments so we can get all the comments matched to a video. then we group by keyword so we can aggregate the avg score of the sentiment for each of the comments in each video for all the keywords that show up among all the videos

SELECT v.keyword AS keyword_name, AVG(c.sentiment) AS avg_score
FROM videos v
JOIN comments c ON v.video_id = c.video_id
GROUP BY v.keyword
ORDER BY avg_score DESC;

