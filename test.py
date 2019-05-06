# file to test short code blocks
import pandas as pd

schema = {
        'date': '05-23-2019',
        'close': 50.00
        }

schema_2 = {
        'date': '05-24-2019',
        'close': 70.00
        }

test_list = [schema, schema_2]

test_frame = pd.DataFrame(test_list)
print(test_frame)
print(test_frame.loc[test_frame['date'] == '05-23-2019'])
