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

sql = """
        select fac_state, count(*) 
        from frs.facilities f 
        where fac_zip <> '99999' 
        group by fac_state 
        order by fac_state asc
        """

result = db_engine.execute(sql)

states_list = []
counts_list = []
for i in result:
    if i[1] != None and i[0] != None:
        states_list.append(i[0])
        print(i[0])
        counts_list.append(i[1])

plt.plot(states_list, counts_list)

#. Fix the tick length and direction
plt.xticks(fontsize=6, rotation = 90)
plt.title('Facilities by State')
plt.savefig('data_expo_graphics/fac_by_state.png')