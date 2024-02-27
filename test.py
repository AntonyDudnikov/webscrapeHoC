import pandas as pd

df = pd.read_json('final.json')
df.iloc[0].to_json('final[0].json')