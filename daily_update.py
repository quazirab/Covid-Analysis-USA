# Remove all old files
import time
t1  = time.time()

import shutil
import os
try:
    shutil.rmtree('processed_data')
except:
    pass
finally:
    time.sleep(5)
    os.makedirs(f"processed_data")

# # update submodule
import git

repo = git.Repo('.')

output = repo.git.submodule('update', '--remote')

filters = [1.5,2.1,2.5]

# update daily _daily_state and deaths_daily_county
from daily_mortality import daily_mortality
print(f'processing daily_mortality')
daily_mortality()

# update death_ratio
from mortality_ratio import mortality_ratio
print(f'processing mortality_ratio')
for n in range(1,8):
    mortality_ratio(n,filter=1.5)
    mortality_ratio(n,filter=2.1)
    mortality_ratio(n,filter=2.5,all=1)

# update death_ratio_1st_trigger
from state_mortality_ratio_1st_trigger import state_mortality_ratio_1st_trigger
print(f'processing state_mortality_ratio_1st_trigger')
for n in range(1,8):
    for filter in filters:
        state_mortality_ratio_1st_trigger(n,filter=filter)

# update slope and intercept
from slope_and_intercept import county_slope_and_intercept
print(f'processing county_slope_and_intercept')

for days in range(3,9):
    for filter in filters:
        for n in range(1,8):
            county_slope_and_intercept(days,n,filter)

# update projection
from county_projection import projection,graph_projection_all
print(f'processing projection')

for days in range(3,9):
    for filter in filters:
        for n in range(1,8):
            projection(days,n,filter,21)

# graph_projection_all()

# combine csv
from csv_combiner import mortality_combined
print(f'processing mortality_combined')
mortality_combined()

print(f'Processing time required - {(time.time()-t1)/60}')

