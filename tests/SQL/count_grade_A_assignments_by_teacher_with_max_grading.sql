-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
-- Count the number of grade 'A' assignments for each teacher with the maximum grading count
WITH GradingCounts AS (
    SELECT teacher_id, COUNT(*) AS grading_count
    FROM assignments
    WHERE grade = 'A'
    GROUP BY teacher_id
)
SELECT t.id AS teacher_id, t.name AS teacher_name, COALESCE(gc.grading_count, 0) AS grade_A_count
FROM teachers t
LEFT JOIN GradingCounts gc ON t.id = gc.teacher_id
WHERE gc.grading_count = (SELECT MAX(grading_count) FROM GradingCounts);
