import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def get_workouts(df, workout_type):
    # Example use:
    # get_workouts(workout_data, "FunctionalStrengthTraining")
    return df[df["Type"] == workout_type]


def plot_workouts_pie(workouts):
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


def main():
    outdir = './dir'
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    plt.style.use("fivethirtyeight")

    print("Extracting workout data...")

    # create element tree object
    tree = ET.parse('data/export.xml')
    root = tree.getroot()

    # Extract workouts from other Apple Health data and create a DataFrame
    workout_list = [x.attrib for x in root.iter('Workout')]
    workout_data = pd.DataFrame(workout_list)

    # Clean up the names of the columns and workouts. Example: HKWorkoutActivityTypeRunning -> Running
    workout_data.drop('device', axis=1, inplace=True)
    workout_data['workoutActivityType'].replace('HKWorkoutActivityType','', inplace=True, regex=True)
    workout_data.rename(columns={'workoutActivityType': 'Type'}, inplace=True)

    # Apple Health data is stored in XML tags as strings.
    # Rework strings to dates and numbers
    for col in ['creationDate', 'startDate', 'endDate']:
        workout_data[col] = pd.to_datetime(workout_data[col])
        workout_data['date'] = workout_data[col].dt.date

    workout_data[['duration', 'totalEnergyBurned', 'totalDistance']].apply(pd.to_numeric, errors='coerce', axis=1)

    print("Number of records: " + str(workout_data.shape[0]))

    # Output processed data as CSV
    workout_data.to_csv('out/workouts.csv')
    durations = workout_data.groupby('date', as_index=False)['duration'].sum()
    durations.to_csv('out/aggregated_workout_durations_per_day.csv')

if __name__ == "__main__":
    main()