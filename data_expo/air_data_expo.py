import yaml
import matplotlib.pyplot as plt
import os 

from sqlalchemy.engine.url import URL
from triage.util.db import create_engine



with open('database.yml','r') as dbf:
    dbconfig = yaml.safe_load(dbf)

db_url = URL(
            'postgres',
            host=dbconfig['host'],
            username=dbconfig['user'],
            database=dbconfig['db'],
            password=dbconfig['pass'],
        )

db_engine = create_engine(db_url)

#> Investigate the count of facilities by state. Ensure that we are at least
#> near average.
state_facilities = """
        select state, count(*) 
        from air.icis_air_facilities iaf 
        where zip_code <> '99999' 
        group by state 
        order by state asc
        """

stat_fac = db_engine.execute(state_facilities)

states_list = []
counts_list = []
for i in stat_fac:
    if i[1] != None and i[0] != None:
        states_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.plot(states_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 90)
# plt.title('Facilities (Air) by State')
# plt.savefig('data_expo_graphics/air_fac_by_state.png')


#> Investigate air facilities by county. We expect disparities, but hope for
#> some level of divesity 

county_facilities = """
        select county_name, count(*) 
        from air.icis_air_facilities iaf 
        where state = 'NY' 
        group by county_name 
        """

count_fac = db_engine.execute(county_facilities)

county_list = []
counts_list = []
for i in count_fac:
    if i[1] != None and i[0] != None:
        county_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.boxplot(counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 90)
# plt.title('Facilities (Air) by County')
# plt.savefig('data_expo_graphics/air_fac_by_county.png')


# #> Look into the pollutant types: 

# air_pollute = """
#         select air_pollutant_class_desc , count(*) 
#         from air.icis_air_facilities iaf 
#         where state = 'NY' 
#         group by air_pollutant_class_desc 
#         """

# air_pollute = db_engine.execute(air_pollute)

# pollute_list = []
# counts_list = []
# for i in air_pollute:
#     if i[1] != None and i[0] != None:
#         pollute_list.append(i[0])
#         print(i[0])
#         counts_list.append(i[1])

# plt.bar(pollute_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('Air Pollutant Types')
# plt.savefig('data_expo_graphics/air_pollute_type.png')


#> Look into the pollutant types: 
import pandas as pd

air_pollute = """
select 
	to_char(date_trunc('year', "HPV_RESOLVED_DATE"), 'YYYY') as violat_year
	, iaf.air_pollutant_class_desc 
	, count(*) 
from air.icis_air_facilities iaf 
inner join air.icis_air_violation_history iavh 
on iaf.pgm_sys_id = iavh."PGM_SYS_ID" 
where iaf.state = 'NY'
and to_char(date_trunc('year', "HPV_RESOLVED_DATE"), 'YYYY') is not NULL
group by violat_year, iaf.air_pollutant_class_desc
order by violat_year asc

        """

air_pollute = db_engine.execute(air_pollute)
print(type(air_pollute))

holder = []
for x in air_pollute:
    temp = [x[0], x[1], x[2]]
    holder.append(temp)

air_pollute_pd = pd.DataFrame(holder)
air_pollute_pd = air_pollute_pd.pivot(index=0, columns=1,values =2)
print(air_pollute_pd)

year_list = air_pollute_pd.index.tolist()
maj_emiss_list = air_pollute_pd['Major Emissions'].tolist()
min_emiss_list = air_pollute_pd['Minor Emissions'].tolist()
synth_min_emiss_list = air_pollute_pd['Synthetic Minor Emissions'].tolist()

plt.plot(year_list, maj_emiss_list)
plt.plot(year_list, min_emiss_list)
plt.plot(year_list, synth_min_emiss_list)
plt.legend(['Major Emissions', 'Minor Emissions', 'Synthetic Minor Emissions'])


#. Fix the tick length and direction
plt.xticks(fontsize=6, rotation = 30)
plt.title('Air Pollutant Types')
plt.savefig('data_expo_graphics/yearly_air_pollute_type.png')



#> Look into the facility types: 
#. Also we get lazy with names now

sql = """
select facility_type_code, count(*) 
from air.icis_air_facilities iaf 
where state = 'NY' 
group by facility_type_code 
        """

execute = db_engine.execute(sql)

ident_list = []
counts_list = []
for i in execute:
    if i[1] != None and i[0] != None:
        ident_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.bar(ident_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('Facility Types')
# plt.savefig('data_expo_graphics/air_facility_type.png')


#> Look into the "high priority violaters": 

sql = """
select current_hpv, count(*) 
from air.icis_air_facilities iaf 
where state = 'NY' 
group by current_hpv 
        """

execute = db_engine.execute(sql)

ident_list = []
counts_list = []
for i in execute:
    if i[1] != None and i[0] != None:
        ident_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.bar(ident_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('High Priority Violator Types')
# plt.savefig('data_expo_graphics/high_prio_viol.png')



#> Look into the compliance monitoring action types: 

sql = """
select comp_monitor_type_desc, count(*) 
from air.icis_air_fces_pces iafp 
inner join air.icis_air_facilities iaf 
on iafp.pgm_sys_id = iaf.pgm_sys_id 
where iaf.state = 'NY' 
group by comp_monitor_type_desc  
        """

execute = db_engine.execute(sql)

ident_list = []
counts_list = []
for i in execute:
    if i[1] != None and i[0] != None:
        ident_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.bar(ident_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('Compliance Monitoring Action Type')
# plt.savefig('data_expo_graphics/air_comp_monitor_type.png')


#> Look into the Formal Enforcement Actions: 

sql = """
select enf_type_desc, count(*) 
from air.icis_air_formal_actions iafa 
inner join air.icis_air_facilities iaf 
on iafa.pgm_sys_id = iaf.pgm_sys_id 
where iaf.state = 'NY' 
group by enf_type_desc 
        """

execute = db_engine.execute(sql)

ident_list = []
counts_list = []
for i in execute:
    if i[1] != None and i[0] != None:
        ident_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.bar(ident_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('Enforcement Formal Actions in NY')
# plt.savefig('data_expo_graphics/formal_enforce_actions.png')



#> Look into the Formal Penalty Amounts: 

sql = """
select penalty_amount, count(*) 
from air.icis_air_formal_actions iafa 
inner join air.icis_air_facilities iaf 
on iafa.pgm_sys_id = iaf.pgm_sys_id 
where iaf.state = 'NY'
and penalty_amount >0
group by penalty_amount 
        """

execute = db_engine.execute(sql)

ident_list = []
counts_list = []
for i in execute:
    if i[1] != None and i[0] != None:
        ident_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

# plt.plot(ident_list, counts_list)

# #. Fix the tick length and direction
# plt.xticks(fontsize=6, rotation = 15)
# plt.title('Formal Penalty Amount in NY')
# plt.savefig('data_expo_graphics/formal_penalty_amount.png')





