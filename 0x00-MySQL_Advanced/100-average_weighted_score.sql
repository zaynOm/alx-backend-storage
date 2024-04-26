-- creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
	UPDATE users
	SET average_score = (SELECT SUM(c.score * p.weight) / SUM(p.weight)
			FROM corrections AS c, projects AS p
			WHERE c.user_id = user_id AND c.project_id = p.id
			)
	WHERE id = user_id;
END;
//
DELIMITER ;
