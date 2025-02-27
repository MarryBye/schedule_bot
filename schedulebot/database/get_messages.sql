SELECT * FROM 
    messages
WHERE 
    chat_id = ?
    AND
    author_username = COALESCE(?, author_username)
    AND
    creation_date >= DATE(COALESCE(?, creation_date))
    AND
    creation_time >= TIME(COALESCE(?, creation_time))