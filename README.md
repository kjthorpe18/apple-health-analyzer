# Apple Health Data Analyzer

Scripts to extract records from an Apple Health data export, converting them to CSV format and providing daily stats.

### Export Apple Health Data
1. From the Apple "Health" app, click your profile in the upper right corner
2. Select `Export All Health Data` > `Export`, and wait for the export to complete
3. Extract the export files, and save the `export.xml` file. This contains all workouts, step counts, and other health data

### To Run
1. Install dependencies:
   ```
   pip3 install -r requirements.txt
   ```
1. Place health data `export.xml` file into the `data/` directory in this project
1. Run the script(s):
   ```
   python3 workouts.py
   python3 stepcounts.py
   ```
1. Resulting CSVs and charts will be placed in the `out/` directory.