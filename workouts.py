import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def get_workouts(df, workout_type):
    # Example use:
    # get_workouts(workout_data, "FunctionalStrengthTraining")
    return df[df["Type"] == workout_type]


def plot_workouts(workouts):
    labels = []
    slices = []
    for wo_type in workouts.Type.unique():
        labels.append(wo_type)
        wo_of_type = workouts[workouts["Type"] == wo_type]
        num_workouts_of_type = wo_of_type.shape[0]
        slices.append(num_workouts_of_type)

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

        return my_autopct

    plt.figure(figsize=(10, 10))
    plt.pie(slices, labels=labels, shadow=False,
            startangle=90, autopct=make_autopct(slices),
            wedgeprops={'edgecolor': 'black'})

    plt.title("Workouts")
    plt.tight_layout()
    plt.show()


outdir = './dir'
if not os.path.exists(outdir):
    os.mkdir(outdir)

plt.style.use("fivethirtyeight")

# create element tree object
tree = ET.parse('data/export.xml')

# for every health record, extract the attributes
root = tree.getroot()

print("Extracting apple_health_analyzer...\n")

workout_list = [x.attrib for x in root.iter('Workout')]

workout_data = pd.DataFrame(workout_list)
workout_data['workoutActivityType'] = workout_data['workoutActivityType'].str.replace('HKWorkoutActivityType', '')
workout_data = workout_data.rename({"workoutActivityType": "Type"}, axis=1)

for col in ['creationDate', 'startDate', 'endDate']:
    workout_data[col] = pd.to_datetime(workout_data[col])
    workout_data['date'] = workout_data[col].dt.date

workout_data['duration'] = pd.to_numeric(workout_data['duration'])
workout_data['totalEnergyBurned'] = pd.to_numeric(workout_data['totalEnergyBurned'])
workout_data['totalDistance'] = pd.to_numeric(workout_data['totalDistance'])

workout_data.drop('device', axis=1, inplace=True)
workout_data.to_csv('out/apple_health_analyzer.csv')

print("Number of apple_health_analyzer: " + str(workout_data.shape[0]))

durations = workout_data.groupby('date', as_index=False)['duration'].sum()
durations.to_csv('out/aggregated_durations.csv')
