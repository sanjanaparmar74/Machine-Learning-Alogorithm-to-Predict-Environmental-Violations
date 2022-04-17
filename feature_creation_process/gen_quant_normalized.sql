drop table public.gen_quant_normalized;
--select * from public.gen_quant_normalized gqn 
commit;

create table public.gen_quant_normalized(
	entity_id INT,
	gen_qty float8,
	gq_norm float8,
	report_year date
);

commit;



insert into public.gen_quant_normalized
select c.entity_id_int as entity_id, c.gen_qty, c.gq_norm, c.report_year
from (
	select z.handler_id, z.gen_qty, z.gq_norm, z.report_year, eik.entity_id_int
	from (
		select handler_id, gen_qty, (gen_qty-gq_avg)/gq_stddev as gq_norm, to_date(report_year, 'YYYY-MM-DD') as report_year
		from 
			nysdec_reports.gm1 g, (
			select avg(gen_qty) as gq_avg, stddev(gen_qty) as gq_stddev
			from nysdec_reports.gm1
			) b
		) z
	left join public.entity_id_key eik 
	on z.handler_id = eik.entity_id 
) c

select * from public.gen_quant_normalized