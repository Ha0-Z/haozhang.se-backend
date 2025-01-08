INSERT INTO idea (title) VALUES
('3d print water cup handle'),
('clean room'),
('fix the bike'),
('ski next week'),
('sew pants'),
('do clay work');


INSERT INTO stage (stage_number, stage_index, description) VALUES
(1, 1, 'done'),
(1, 2, 'rework'),
(1, 3, 'do tasks'),
(1, 4, 'divide work'),
(1, 5, 'research'),
(1, 6, 'establish task'),
(2, 1, 'done'),
(2, 2, 'do tasks'),
(2, 3, 'decide tasks'),
(2, 4, 'plan tasks'),
(2, 5, 'expected outcome'),
(2, 6, 'purpose of work'),
(2, 7, 'establish task');



INSERT INTO task (title, description, priority, type, stage_index, stage_number, status, reward, deadline_date, create_date, last_modified) VALUES
('Personal website', 'design and establish a website with purpose of show myself, put up blogs and list my projects.', 4, 'own project', 3, 1, 'working on', 'Buy new headphone', '2025-02-13', '2024-12-13', '2025-01-07'),
('Sign to course', 'Register me to courses in the spring 2025.', 8, 'school', 6, 1, 'unstarted', '50', '2025-01-10', '2025-01-05', '2025-01-07');



INSERT INTO event (create_date, last_modified, date_start, date_end, summary, place) VALUES
('2025-01-05', '2025-01-07', '2025-01-10 08:00', '2025-01-10 10:00', 'Exam- Data', 'KTH');


INSERT INTO sub_task (task_id, requirement, status, ) VALUES
(1, 'Make the website be able to show blog', 'done');
