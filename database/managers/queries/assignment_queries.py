# database.managers.queries.assignments.py

# Skapa tabell
CREATE_ASSIGNMENTS_TABLE = """
CREATE TABLE IF NOT EXISTS assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kommun TEXT,
    adress TEXT,
    ort TEXT,
    material TEXT,
    tomningsfrekvens TEXT,
    info TEXT,
    chauffor TEXT,
    koordinater TEXT,
    status TEXT,
    senast_hamtad DATE,
    image_path TEXT,
    next_occurrence_date DATE
);
"""

# SQL fråga: Insert
INSERT_ASSIGNMENT = """
INSERT INTO assignments 
(kommun, adress, ort, material, 
tomningsfrekvens, info, chauffor, 
koordinater, next_occurrence_date, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
"""

INSERT_RECURRING_ASSIGNMENT = """
INSERT INTO assignments 
(kommun, adress, ort, material, tomningsfrekvens, 
info, chauffor, koordinater, status, senast_hamtad, 
image_path, next_occurrence_date)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

# SQL fråga: Update
UPDATE_JOB_STATUS = """
UPDATE assignments 
SET status = ?, senast_hamtad = CURRENT_DATE, image_path = ? 
WHERE id = ?
"""

# SQL fråga: Radera
DELETE_ASSIGNMENT = """
DELETE FROM assignments WHERE id = ?
"""

# SQL fråga: Val, selektion:
# Hämtar alla uppdrag
SELECT_ALL_ASSIGNMENTS = """
SELECT * FROM assignments
"""

# Hämtar och sorterar uppdrag efter datum
SELECT_ASSIGNMENTS_SORTED_BY_DATE = """
SELECT * FROM assignments 
WHERE next_occurrence_date IS NOT NULL 
ORDER BY next_occurrence_date ASC
"""

# Hämtar uppdrag för aktuell vecka
SELECT_ASSIGNMENTS_FOR_CURRENT_WEEK = """
SELECT * FROM assignments 
WHERE next_occurrence_date BETWEEN ? AND ?
"""

# Ställer frågan till SQL att välja ett uppdrag baserat på dess ID
SELECT_ASSIGNMENT_BY_ID = "SELECT * FROM assignments WHERE id = ?"
