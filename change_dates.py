from datetime import datetime, timedelta
import numpy as np
from os.path import join
import os

# We start on the 19th, so the with two days of warm up
# So the actual run will start on the 21st noon, NZT
start_date = datetime(2019, 6, 19, 0)
end_date = datetime(2019, 7, 20, 0)

# Run every day for 72 hours (with a 48 hour warm up)
run_length = timedelta(hours=24*3)
run_step = timedelta(hours=24)

all_dates = np.arange(start_date, end_date + timedelta(hours=1), run_step, dtype=datetime)

input_file = 'namelist.input.small_dom_conus'
out_folder = 'all_dates/'

with open(input_file) as f:
    all_lines = f.readlines()
#all_lines = [x.strip() for x in all_lines]

print(f'Making {len(all_dates)} files')

if not os.path.exists(out_folder):
    os.makedirs(out_folder)


def get_year(dt):
    return str(dt.year)


def get_month(dt):
    return str(dt.month).zfill(2)


def get_day(dt):
    return str(dt.day).zfill(2)


def get_hour(dt):
    return str(dt.hour).zfill(2)


target_vars = {'start_year': get_year, 'start_month': get_month, 'start_day': get_day,'start_hour': get_hour,
              'end_year': get_year, 'end_month': get_month, 'end_day': get_day, 'end_hour': get_hour}


def get_line(or_line, ):
    new_line = None

    for key, key_func in target_vars.items():
        if key in or_line:
            if 'start' in key:
                new_line = '\t' + key + " = " + (key_func(r_dt) + ', ') * 5 + '\n'
            else:
                new_line = '\t' + key + " = " + (key_func(r_dt_end) + ', ') * 5 + '\n'

    if new_line is None:
        return or_line
    else:
        return new_line


for n, r_dt in enumerate(all_dates):
    r_dt_end = r_dt + run_length

    out_file = join(out_folder, 'namelist.input.{}.{}'.format(get_month(r_dt), get_day(r_dt)))

    with open(out_file, 'w') as curr_namelist:
        for line in all_lines:
            new_l = get_line(line)
            curr_namelist.write(new_l)
