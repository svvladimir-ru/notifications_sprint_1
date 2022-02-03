CREATE SCHEMA IF NOT EXISTS users;

-- Создать таблицу - users
CREATE TABLE IF NOT EXISTS users.user(
    id uuid PRIMARY KEY  DEFAULT gen_random_uuid(),
    login TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    confirmed boolean DEFAULT FALSE,
    mail_subscribe boolean DEFAULT TRUE,
    password TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

-- Создать таблицу - role
CREATE TABLE IF NOT EXISTS users.role(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

-- Создать таблицу - user_role
CREATE TABLE IF NOT EXISTS users.user_role(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    role_id uuid,
    created_at timestamptz DEFAULT NOW(),
	CONSTRAINT user_role_id_unique UNIQUE (user_id, role_id)
);

INSERT INTO users.role (name) VALUES ('admin'), ('user'), ('subscriber');


-- Создать функцию логирования добавления пользователя - create_user_trigger()
CREATE FUNCTION create_user_trigger() RETURNS trigger AS $$
    BEGIN
        IF TG_OP = 'INSERT'
            THEN
                INSERT INTO events.welcome (user_id, template_id)
                    VALUES (
                        NEW.id, (SELECT id FROM events.templates WHERE name = 'welcome')
                    );
                RETURN NEW;
        END IF;
    END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;

-- Создать тригеры для таблиц
CREATE TRIGGER welcome_event_fo_new_user_trigger BEFORE INSERT ON users.user
    FOR EACH ROW EXECUTE PROCEDURE create_user_trigger();