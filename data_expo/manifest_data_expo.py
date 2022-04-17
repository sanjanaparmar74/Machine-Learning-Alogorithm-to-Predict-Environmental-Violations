# import yaml
import config
import numpy as np
import matplotlib.pyplot as plt

from sqlalchemy.engine.url import URL
from triage.util.db import create_engine

# with open('database.yml', 'r') as dbf:
#     dbconfig = yaml.safe_load(dbf)

# db_url = URL(
#             'postgres',
#             host=dbconfig['host'],
#             username=dbconfig['user'],
#             database=dbconfig['db'],
#             password=dbconfig['pass'],
#             port=dbconfig['port'],
#         )

db_url = URL(
            'postgres',
            host=config.host,
            username=config.user,
            database=config.db,
            password=config.password,
            port=config.port,
        )

db_engine = create_engine(db_url)

# 2016

sqlList = ["select discr_quantity_ind, count(distinct manifest_tracking_num) from manifest.mani16 group by discr_quantity_ind;", \
"select discr_type_ind, count(distinct manifest_tracking_num) from manifest.mani16 group by discr_type_ind;", \
"select discr_residue_ind, count(distinct manifest_tracking_num) from manifest.mani16 group by discr_residue_ind;", \
"select discr_partial_reject_ind, count(distinct manifest_tracking_num) from manifest.mani16 group by discr_partial_reject_ind;", \
"select discr_full_reject_ind, count(distinct manifest_tracking_num) from manifest.mani16 group by discr_full_reject_ind;"]

yes2016 = []
for statement in sqlList:
    out = []
    result = db_engine.execute(statement)
    for i, j in result:
        out.append(j)
    yes2016.append(out[1])

# 2007

sqlList = ["select discr_quantity_ind, count(distinct manifest_tracking_num) from manifest.mani07 group by discr_quantity_ind;", \
"select discr_type_ind, count(distinct manifest_tracking_num) from manifest.mani07 group by discr_type_ind;", \
"select discr_residue_ind, count(distinct manifest_tracking_num) from manifest.mani07 group by discr_residue_ind;", \
"select discr_partial_reject_ind, count(distinct manifest_tracking_num) from manifest.mani07 group by discr_partial_reject_ind;", \
"select discr_full_reject_ind, count(distinct manifest_tracking_num) from manifest.mani07 group by discr_full_reject_ind;"]

yes2007 = []
for statement in sqlList:
    out = []
    result = db_engine.execute(statement)
    for i, j in result:
        out.append(j)
    yes2007.append(out[1])

# Make a graph 
plt.figure('a')
N = len(yes2007)
ind = np.arange(N) 
width = 0.35       
plt.bar(ind, yes2007, width, label='2007')
plt.bar(ind + width, yes2016, width, label='2016')

plt.ylabel('# Discrepencies')
plt.title('Discrepancies by Year')

plt.xticks(ind + width / 2, ('Quantity', 'Type', 'Residue', 'Partial', 'Full'))
plt.legend(loc='best')
plt.savefig('discrepanciesByYear')

# Plot manifests by year, 2007 - 2017
plt.figure('b')
tablelist = ["manifest.man8081"]
i = 82
while i <= 99:
    table = "manifest.mani" + str(i)
    tablelist.append(table)
    i += 1

print("first part of tablelist done")

i = 0
while i <= 17:
    if i == 9:
        table = "manifest.mani9"
    elif i < 10:
        table = "manifest.mani0" + str(i)
    else:
        table = "manifest.mani" + str(i)
    tablelist.append(table)
    i += 1

print("second part of tablelist done, querying data")

manifestCounts = []
for table in tablelist[0:25]:
    sql = "select count(distinct manifest_number) from " + table + ";"
    result = db_engine.execute(sql)
    for i in result:
        manifestCounts.append(i[0])

for table in tablelist[25:]:
    sql = "select count(distinct manifest_tracking_num) from " + table + ";"
    result = db_engine.execute(sql)
    for i in result:
        manifestCounts.append(i[0])

print(manifestCounts)
years = np.arange(1981,2018)
     
plt.plot(years, manifestCounts)
plt.xticks(years, rotation=90)
plt.title('# of Manifests by Year')

plt.savefig('manifestsByYear')

# Plot by handling type code, 1980, 1990, 2000, 2010, 2016
out81 = []
out90 = []
out00 = []
tables = ["manifest.man8081", "manifest.mani90", "manifest.mani00"]
x = 1
for table in tables:
    out = []
    sql = "select handling_method1, count(distinct manifest_number) from " + \
    table + " group by handling_method1;"
    result = db_engine.execute(sql)
    for i, j in result:
        if i != ' ':
            out.append(j)
    if x == 1:
        out81.append(out)
    if x == 2:
        out90.append(out)
    if x == 3:
        out00.append(out)
    x += 1

tables = ["manifest.mani10", "manifest.mani16"]
out10 = []
out16 = []
x = 1
for table in tables:
    out = []
    sql = "select handling_type_code, count(distinct manifest_tracking_num) from " + \
    table + " group by handling_type_code;"
    result = db_engine.execute(sql)
    for i, j in result:
        if i != '':
            out.append(j)
    if x == 1:
        out10.append(out)
    if x == 2:
        out16.append(out)
    x += 1

print(out81)
print(out16)

Make a graph 
plt.figure('c')
years = [1980, 1990, 2000, 2010, 2016]
     
plt.plot(years, b, label = 'Incineration')
plt.plot(years, l, label = 'Landfill')
plt.plot(years, t, label = 'Chemical, Physical, or Biological')
plt.plot(years, r, label = 'Material Recovery')
plt.xticks(years, rotation=90)
plt.title('# of Manifests by Handling Type and Year')

plt.savefig('handlingByYear')
plt.figure('a')

print(out81[0])
print(out90[0])
print(out00[0])
print(out10[0])
print(out16[0])

N = len(out81[0])
print(N)

ind = np.arange(N) 
width = 0.15     
print(2*width)  
plt.bar(ind, out81[0], width, label='1981')
plt.bar(ind + width, out00[0], width, label='2000')
plt.bar(ind + (2*width), out16[0], width, label='2016')

plt.ylabel('# of Manifests')
plt.title('# of Manifests by Handling Type and by Year')

plt.xticks(ind + (2*width) / 2, ('Incinerator', 'Landfill', 'Recovery', 'Chem, Bio, or Phys'))
plt.legend(loc='best')
plt.savefig('handlingByYear')
