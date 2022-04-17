
create table public.entity_id_key(
	entity_id VARCHAR (15),
	entity_id_int INT primary key
)

commit;


insert into public.entity_id_key 
select distinct d.entity_id, row_number () over(order by d.entity_id) as entity_id_int_key
from (
    select distinct (c.entity_id)
    from (

        -- Setting up the List of Handler Ids with Inspections from 2012 to 2014.
        -- These ids are the same style as RCRA_ids and registry_ids
        -- 2,598 distinct handler ids

        select distinct(handler_id) as entity_id, extract(year from evaluation_start_date)||'-01-01' as as_of_date
        from rcra.cmecomp3 c
        where c.state = 'NY'
   
        UNION

        -- Setting up the List of handler Ids that produced during 2012 thru 2014.
        -- This could be done more eloquently, but I don't understand how to do it.
        -- Ex: https://stackoverflow.com/questions/35486057/dynamic-union-all-query-in-postgres
        -- 10,373 distinct handler ids

        select distinct (a.handler_id) as entity_id, a.as_of_date
        from (
            select distinct (handler_id)
            	, extract(year from to_date(report_year, 'YYYY-MM-DD'))||'-01-01' as as_of_date
            from nysdec_reports.gm1 g
            UNION
            select distinct (handler_id)
            	, extract(year from to_date(report_year, 'YYYY-MM-DD'))||'-01-01' as as_of_date
            from nysdec_reports.si1 
            UNION
            select distinct (handler_id)
            	, extract(year from to_date(report_year, 'YYYY-MM-DD'))||'-01-01' as as_of_date
            from nysdec_reports.wr1 w
            ) a
    ) c
) d;

select * from public.entity_id_key eik;