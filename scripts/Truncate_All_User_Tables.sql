DO $$
DECLARE
    r RECORD;
BEGIN
    -- Loop through all tables in reverse dependency order
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename DESC
    LOOP
        EXECUTE 'TRUNCATE TABLE public.' || quote_ident(r.tablename) || ' CASCADE;';
        RAISE NOTICE 'Truncated: %', r.tablename;
    END LOOP;
END $$;
