CREATE SCHEMA IF NOT EXISTS events;

CREATE TABLE IF NOT EXISTS events.templates(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    template TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW(),
    updated_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.welcome(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid,
    template_id uuid,
    created_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.discounts(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id uuid,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.updating_content(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id uuid,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at timestamptz DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS events.events(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at timestamptz DEFAULT now(),
    schema_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    record_id uuid NOT NULL
);

-- Создать функцию логирования создания событий - create_event_trigger()
CREATE FUNCTION create_event_trigger() RETURNS trigger AS $$
    BEGIN
        IF TG_OP = 'INSERT'
            THEN
                INSERT INTO events.events (schema_name, table_name, record_id)
                    VALUES (TG_TABLE_SCHEMA, TG_RELNAME, NEW.id);
                RETURN NEW;
        END IF;
    END;
$$ LANGUAGE 'plpgsql' SECURITY DEFINER;

-- Создать тригеры для таблиц
CREATE TRIGGER welcome_event_trigger BEFORE INSERT ON events.welcome
    FOR EACH ROW EXECUTE PROCEDURE create_event_trigger();

CREATE TRIGGER update_content_event_trigger BEFORE INSERT ON events.updating_content
    FOR EACH ROW EXECUTE PROCEDURE create_event_trigger();

CREATE TRIGGER discounts_event_trigger BEFORE INSERT ON events.discounts
    FOR EACH ROW EXECUTE PROCEDURE create_event_trigger();