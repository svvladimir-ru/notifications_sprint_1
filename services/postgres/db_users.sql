CREATE SCHEMA IF NOT EXISTS users;

-- Создать таблицу - users
CREATE TABLE IF NOT EXISTS users.user(
    id uuid PRIMARY KEY  DEFAULT gen_random_uuid(),
    login TEXT NOT NULL,
    email TEXT NOT NULL,
    confirmed boolean DEFAULT FALSE,
    password TEXT NOT NULL,
    created_at timestamptz,
    updated_at timestamptz,
    CONSTRAINT user_id_login UNIQUE (id, login),
    CONSTRAINT user_id_email UNIQUE (id, email)
);

-- Создать таблицу - role
CREATE TABLE IF NOT EXISTS users.role(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT UNIQUE,
    created_at timestamptz,
    updated_at timestamptz
);

-- Создать таблицу - login_history
CREATE TABLE IF NOT EXISTS users.login_history(
    id uuid DEFAULT gen_random_uuid(),
    user_id uuid,
    ip TEXT,
    user_agent TEXT,
    device_type TEXT,
    created_at timestamptz,
    PRIMARY KEY (id, device_type),
    CONSTRAINT login_history_id_device UNIQUE (id, device_type)
);

-- Создать таблицу - user_role
CREATE TABLE IF NOT EXISTS users.user_role(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    role_id uuid,
    created_at timestamptz,
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