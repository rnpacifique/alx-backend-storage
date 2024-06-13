-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUser
-- The procedure computes and stores the average weighted score for a student

-- Create the stored procedure
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;
    
    -- Compute the weighted sum of scores for the given user
    SELECT SUM(c.score * p.weight)
    INTO weighted_sum
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    -- Compute the total weight of projects for the given user
    SELECT SUM(weight)
    INTO total_weight
    FROM projects
    WHERE id IN (SELECT project_id FROM corrections WHERE user_id = user_id);
    
    -- Compute the average weighted score
    IF total_weight IS NOT NULL AND total_weight > 0 THEN
        SET avg_weighted_score = weighted_sum / total_weight;
    ELSE
        SET avg_weighted_score = 0;
    END IF;
    
    -- Update the average score for the given user
    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;