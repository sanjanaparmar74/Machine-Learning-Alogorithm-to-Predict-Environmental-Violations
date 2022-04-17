drop table public.cohort_acs_info;
commit;

create table public.cohort_acs_info as (
select d.entity_id, d.entity_id_str as entity_id_str, d.zip_code, to_date(d.as_of_date, 'YYYY-MM-DD') as as_of_date, 
	case when ad.high_income = 1 then 'Y' else 'N' end as high_income, 
	case when ad.large_minority_pop = 1 then 'Y' else 'N' end as large_minority_pop
	from (
		select distinct
			c.entity_id,
			c.entity_id_str,
			case when c.zip_code is not null then c.zip_code
			else c.location_zip
			end as zip_code,
			c.as_of_date
		from (
			select
				ec.entity_id
				, eik.entity_id as entity_id_str
				, left(f.zip_code,5) as zip_code
				, left(si1.location_zip,5) as location_zip
				, ec.as_of_date
			from public.epa1_cohort ec
			left join public.entity_id_key eik
			on ec.entity_id = eik.entity_id_int
			left join rcra.facilities f
			on eik.entity_id = f.id_number
			left join nysdec_reports.si1
			on eik.entity_id = si1.handler_id
		) c
	) d
	left join public.acs_data2 ad
	on d.zip_code = ad.zip_code
)

commit;
