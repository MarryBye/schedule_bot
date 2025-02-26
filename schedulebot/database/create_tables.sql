DROP TABLE IF EXISTS "disciplines";
DROP TABLE IF EXISTS "schedule";
DROP TABLE IF EXISTS "teachers";

CREATE TABLE IF NOT EXISTS "disciplines" (
	"id"	INTEGER,
	"name"	TEXT,
	"is_exam"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	INTEGER,
	"day_of_week"	TEXT,
	"time"	TEXT,
	"teacher_id"	INTEGER,
	"discipline_id"	INTEGER,
	"zoom_link"	TEXT,
	"period"	TEXT,
	"additional_info"	TEXT,
	"type"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("discipline_id") REFERENCES "disciplines"("id"),
	FOREIGN KEY("teacher_id") REFERENCES "teachers"("id")
);

CREATE TABLE IF NOT EXISTS "teachers" (
	"id"	INTEGER,
	"name"	TEXT,
	"lastname"	TEXT,
	"surname"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);