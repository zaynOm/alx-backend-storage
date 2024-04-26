-- creates a stored procedure ComputeAverageWeightedScoreForUsers that computes
-- and store the average weighted score for all students.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers () 
BEGIN
	UPDATE users
	SET average_score = (SELECT SUM(c.score * p.weight) / SUM(p.weight)
			FROM corrections AS c, projects AS p
			WHERE c.user_id = users.id AND c.project_id = p.id
			);
END;
//
DELIMITER ;
