import numpy as np
import pandas as pd
import os
from datetime import datetime

tarama=os.scandir()

print("""#####################""")
limit = int(input("Doğruluk alt limitini giriniz: "))
print("""#####################""")

for belge in tarama:
    try:
        filename = belge.name
        #filename = "data.xlsx"
        df = pd.read_excel(filename, skiprows=19, names=["data"])
        print(df.info())
        print(df.iloc[0])

        df.iloc[0:20]

        date = df.apply(lambda row: datetime.strptime(row.values[0].split()[0], '%Y-%m-%dT%H:%M:%S.000Z'), axis=1)
        _initial_time = date.values[0]
        time = np.array([float(row - _initial_time)*1e-9*(1/60) for row in date.values])
        q = df.apply(lambda row: float(row.values[0].split()[1]), axis=1)
        vals = df.apply(lambda row: float(row.values[0].split()[2]), axis=1)
        
        # date.values
        # time = df.apply(lambda row: float(row.values[0] - _initial_time)*1e-9, axis=1)
        # q.values
        # vals.values

        df["date"] = date
        df["time"] = time
        df["vals"] = vals
        df["q"] = q

        current_day = df.date[0].day
        current_day

        df.date[0].date()

        current_date = df.date[0].date()

        day_by_day = dict()
        all_time_options = set()
        

        for i in range(len(q)):
            if(df.q[i] >= limit):
                _value = df.vals[i]
                _date_i = df.date[i].replace(second=0)
                _date_i_time = _date_i.time()
                _date_i_date = _date_i.date()

                all_time_options.add(_date_i_time)
                    
                if _date_i_date in day_by_day.keys():
                    day_by_day[_date_i_date][_date_i_time] = _value
                else:
                    day_by_day[_date_i_date] = dict()
                    day_by_day[_date_i_date][_date_i_time] = _value
                
        #_ = [print(d) for d in day_by_day.keys()]

        day_list = list(day_by_day.keys())
        

        #day_by_day[day_list[1]]

        new_df = pd.DataFrame(day_by_day)
        new_df = new_df.sort_index(ascending=True)
        new_col_names = [col.__str__() for col in new_df.columns]
        new_df.columns = new_col_names
        
        listData = list()
        x=0
        y=0
        for y in range(len(new_df.columns)):
            for x in range(len(new_df.index[:].values)):
                listData.append(new_df.iloc[x,y])
        listData_df = pd.DataFrame(listData)

        path = belge.name
        with pd.ExcelWriter(path) as writer:
            new_df.to_excel(writer, sheet_name='new_sheet1')
            listData_df.to_excel(writer, sheet_name="new_sheet2")
    
    
    except OSError:
        print("""#####\tOS Error Found\t#####""")
        continue
    except ValueError:
        print("""#####\tValue Error Found\t#####""")
        continue
    except AttributeError:
        print("""#####\tAttribute Error Found\t#####""")
        continue
