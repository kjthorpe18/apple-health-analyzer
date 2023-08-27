import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt


def plot_daily_counts(counts):
    plt.scatter(counts["date"], counts["value"], c="blue")
    plt.title("Daily Step Counts")
    plt.xlabel("Date")
    plt.ylabel("Steps")

    fig = plt.gcf()
    fig.set_size_inches(30.5, 15.5)
    fig.savefig("out/step_counts.png", dpi=100)
    plt.clf()


def main():
    outdir = "./out"
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    plt.style.use("fivethirtyeight")

    print("Extracting step counts...\n")

    tree = ET.parse("data/export.xml")
    root = tree.getroot()

    # Step counts are stored under an element like `<Record type="HKQuantityTypeIdentifierStepCount" .../>`
    records_list = [x.attrib for x in root.iter("Record")]
    df = pd.DataFrame(records_list)
    step_counts = df[df["type"] == "HKQuantityTypeIdentifierStepCount"]

    # Only use one device (e.g. Phone vs an Apple watch)
    step_counts = step_counts[step_counts["sourceName"].str.contains("Phone")]
    step_counts = pd.DataFrame(step_counts)

    # Apple Health data is stored in XML tags as strings.
    # Rework strings to dates and numbers
    for col in ["creationDate", "startDate", "endDate"]:
        step_counts[col] = pd.to_datetime(step_counts[col])
        step_counts["date"] = step_counts[col].dt.date

    step_counts["value"] = pd.to_numeric(step_counts["value"])

    print("Number of records: " + str(step_counts.shape[0]))

    daily_counts = step_counts.groupby("date", as_index=False)["value"].sum()

    # Output processed data as CSV
    daily_counts.to_csv("out/dailycounts.csv")
    step_counts.to_csv("out/stepcounts.csv")

    plot_daily_counts(daily_counts)


if __name__ == "__main__":
    main()
