-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id INT;
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;
    
    DECLARE user_cursor CURSOR FOR
        SELECT id FROM users;
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND
        SET user_id = NULL;
    
    OPEN user_cursor;
    
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
       
        IF user_id IS NULL THEN
            LEAVE user_loop;
        END IF;
        
        SET weighted_sum = 0;
        SET total_weight = 0;
        
        SELECT SUM(c.score * p.weight)
        INTO weighted_sum
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id;
        
        SELECT SUM(weight)
        INTO total_weight
        FROM projects
        WHERE id IN (SELECT project_id FROM corrections WHERE user_id = user_id);
        
        IF total_weight IS NOT NULL AND total_weight > 0 THEN
            SET avg_weighted_score = weighted_sum / total_weight;
        ELSE
            SET avg_weighted_score = 0;
        END IF;
        
        UPDATE users
        SET average_score = avg_weighted_score
        WHERE id = user_id;
    END LOOP;
    
    CLOSE user_cursor;
END //

DELIMITER ;