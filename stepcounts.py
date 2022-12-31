import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def plot_daily_counts(counts):
    counts.plot.scatter(x="date", y="value")
    plt.title("Daily Step Counts")
    plt.xlabel("Date")
    plt.ylabel("Steps")
    plt.show()


outdir = './out'
if not os.path.exists(outdir):
    os.mkdir(outdir)

plt.style.use("fivethirtyeight")

tree = ET.parse('data/export.xml')
root = tree.getroot()

print("Extracting step counts...\n")

records_list = [x.attrib for x in root.iter('Record')]
df = pd.DataFrame(records_list)
step_counts = df[df['type'] == 'HKQuantityTypeIdentifierStepCount']
step_counts = step_counts[step_counts['sourceName'].str.contains("Phone")]
step_counts = pd.DataFrame(step_counts)

for col in ['creationDate', 'startDate', 'endDate']:
    step_counts[col] = pd.to_datetime(step_counts[col])
    step_counts['date'] = step_counts[col].dt.date

step_counts['value'] = pd.to_numeric(step_counts['value'])

print("Number of records: " + str(step_counts.shape[0]))

daily_counts = step_counts.groupby('date', as_index=False)['value'].sum()

daily_counts.to_csv('out/dailycounts.csv')
step_counts.to_csv('out/stepcounts.csv')

plot_daily_counts(daily_counts)
