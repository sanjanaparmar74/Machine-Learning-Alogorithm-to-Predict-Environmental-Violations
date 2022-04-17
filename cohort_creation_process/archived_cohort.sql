
-- Establish the cohort list using the below queries
-- Some notes from the triage site: https://dssg.github.io/triage/experiments/experiment-config/#cohort-config
-- Cohort requires a cohort id and an "[as_of_date}"
-- Cohort also requires that the cohort id be an integer.
    -- We will need to resolve this once we combine all three queries together.


-- Pull the three different query sets together in one big union
-- Together there are 42,634 distinct RCRA Ids
-- Currently the '{as_of_date}' lines are commented out. Fix for final submission.


select distinct (c.entity_id), c.as_of_date
from (

    -- Setting up the List of Handler Ids with Inspections from 2012 to 2014.
    -- These ids are the same style as RCRA_ids and registry_ids
    -- 2,598 distinct handler ids

    select distinct(handler_id) as entity_id, evaluation_start_date as as_of_date
    from rcra.cmecomp3 c
    where c.state = 'NY'
    and evaluation_start_date >= '2012-01-01'
    and evaluation_start_date < '2015-01-01'

	-- union
    UNION

    -- Setting up the List of handler Ids that produced during 2012 thru 2014.
    -- This could be done more eloquently, but I don't understand how to do it.
    -- Ex: https://stackoverflow.com/questions/35486057/dynamic-union-all-query-in-postgres
    -- 10,373 distinct handler ids

    select distinct (a.handler_id) as entity_id, a.as_of_date
    from (
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm1 g
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm1nydec gn
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm2 g2
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm3 g3
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm4 g4
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm5 g5
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.gm_combined gc
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si1 s
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si2 s2
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si3 s3
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si4 s4
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si5 s5
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si6 s6
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.si7 s7
        where report_year >= '2012'
        and report_year < '2015'
        union
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.wr1 w
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.wr2 w2
        where report_year >= '2012'
        and report_year < '2015'
        UNION
        select distinct (handler_id), to_date(report_year, 'YYYY-MM-DD') as as_of_date
        from nysdec_reports.wr3 w3
        where report_year >= '2012'
        and report_year < '2015'
        ) a

	-- union 
    UNION

    -- Setting up the List of rcra Ids that generated or received during 2012 thru 2014.
    -- This could be done more eloquently, but I don't understand how to do it.
    -- Ex: https://stackoverflow.com/questions/35486057/dynamic-union-all-query-in-postgres
    -- 40,079 distinct rcra ids

    select distinct(b.rcra_id) as entity_id, b.as_of_date
    from (
        -- 12-14 for gen_rcra_id 
        select m.gen_rcra_id as rcra_id, to_date(m.gen_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani12 m 
        where m.gen_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        union
        select m.gen_rcra_id as rcra_id, to_date(m.gen_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani13 m 
        where m.gen_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        union 
        select m.gen_rcra_id as rcra_id, to_date(m.gen_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani14 m 
        where m.gen_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        and m.tsdf_sign_date < '2015-01-01'
        union 

        -- 12-14 for tsdf_rcra_id 
        select m.tsdf_rcra_id as rcra_id, to_date(m.tsdf_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani12 m 
        where m.tsdf_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        union
        select m.tsdf_rcra_id as rcra_id, to_date(m.tsdf_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani13 m 
        where m.tsdf_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        union 
        select m.tsdf_rcra_id as rcra_id, to_date(m.tsdf_sign_date, 'YYYY-MM-DD') as as_of_date
        from manifest.mani14 m 
        where m.tsdf_rcra_id in (
            select pl.pgm_sys_id 
            from frs.facilities f 
            left join frs.program_links pl 
            on f.registry_id = pl.registry_id 
            where f.fac_state = 'NY')
        and m.tsdf_sign_date < '2015-01-01'
    ) b
) c
where c.as_of_date = '{as_of_date}'::date - interval '1day'