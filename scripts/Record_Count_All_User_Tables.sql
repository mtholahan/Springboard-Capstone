DO $$
DECLARE
    r RECORD;
    result BIGINT;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    LOOP
        EXECUTE format('SELECT COUNT(*) FROM public.%I', r.tablename)
        INTO result;

        RAISE NOTICE 'Table: % | Row count: %', r.tablename, result;
    END LOOP;
END $$;
