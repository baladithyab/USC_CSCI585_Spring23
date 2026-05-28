-- DB => postgresql on supabase
-- Find the sponsor who has sponsored the highest amount in YouTube. Display the sponsor’s name, phone number and the total amount sponsored.
-- Explanation: By joining videos, sponsored_videos, sponsors we get the tuples we can pull information from. we group by name and phone to make sure that we are getting the unique sponsors since we use that as our primary key. after that we order by the total amt sponsored which the the sum overall sponsors and finally pull the top one for the final result.

SELECT s.name, s.phone, SUM(sv.amount) AS total_amount_sponsored
FROM videos v
JOIN sponsored_videos sv ON v.video_id = sv.video_id
JOIN sponsors s ON sv.sponsor_id = s.sponsor_id
GROUP BY s.name, s.phone
ORDER BY total_amount_sponsored DESC
LIMIT 1;
