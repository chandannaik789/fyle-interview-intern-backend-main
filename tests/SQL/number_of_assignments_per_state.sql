-- Write query to get number of assignments for each state
-- Count the number of assignments per state (SUBMITTED, DRAFT, GRADED)
SELECT state, COUNT(*) AS assignment_count
FROM assignments
GROUP BY state;
