-- Table: idea
CREATE TABLE idea (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    priority INT DEFAULT 0,
    taken CHAR(1) NOT NULL DEFAULT 'N',
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Table: evaluation
CREATE TABLE evaluation (
    id SERIAL PRIMARY KEY,
    score INT NOT NULL,
    explanation TEXT NOT NULL,
    advice TEXT,
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Table: stage
CREATE TABLE stage (
    stage_number SERIAL,
    stage_index SERIAL,
    description VARCHAR(50) NOT NULL,
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (stage_number, stage_index)
);

-- Table: task
CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    priority INT DEFAULT 0,
    type VARCHAR(30) NOT NULL,
    stage_index INT NOT NULL,
    stage_number INT NOT NULL,
    status VARCHAR(50) DEFAULT 'unstarted',
    reward VARCHAR(30) DEFAULT 10,
    routine TEXT,
    material TEXT,
    evaluation INT,
    idea_id INT,
    deadline_date TIMESTAMPTZ NOT NULL,
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (stage_number, stage_index) REFERENCES stage(stage_number, stage_index) ON DELETE CASCADE,
    FOREIGN KEY (evaluation) REFERENCES evaluation(id) ON DELETE SET NULL,
    FOREIGN KEY (idea_id) REFERENCES idea(id) ON DELETE SET NULL
);

-- Table: sub_task
CREATE TABLE sub_task (
    id SERIAL PRIMARY KEY,
    task_id INT NOT NULL,
    requirement TEXT NOT NULL,
    status VARCHAR(10) DEFAULT 'unstarted',
    date_done TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE
);

-- Table: alarm
CREATE TABLE alarm (
    id SERIAL PRIMARY KEY,
    trigger VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    action VARCHAR(100) NOT NULL,
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Table: event
CREATE TABLE event (
    id SERIAL PRIMARY KEY,
    sub_task_id INT,
    create_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    date_start TIMESTAMPTZ NOT NULL,
    date_end TIMESTAMPTZ NOT NULL,
    summary TEXT NOT NULL,
    place VARCHAR(50),
    color VARCHAR(30) DEFAULT 'OPAQUE',
    routine TEXT,
    alarm INT,
    FOREIGN KEY (sub_task_id) REFERENCES sub_task(id) ON DELETE SET NULL,
    FOREIGN KEY (alarm) REFERENCES alarm(id) ON DELETE SET NULL
);
