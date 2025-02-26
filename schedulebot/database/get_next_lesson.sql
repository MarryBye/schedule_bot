SELECT 
	s.day_of_week AS day,
	s.time AS time,
	(t.name || ' ' || t.lastname || ' ' || t.surname) AS teacher,
    d.is_exam AS is_exam_discipline,
    d.name AS discipline_name,
    s.period AS period,
    s.type AS type,
    s.zoom_link AS zoom_link,
	s.additional_info AS info
FROM 
    schedule AS s
INNER JOIN
    disciplines AS d ON s.discipline_id = d.id,
    teachers AS t ON s.teacher_id = t.id 
WHERE
    s.day_of_week = ? AND TIME(s.time) >= TIME(?);