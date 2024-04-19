import csv
import os
import xlsxwriter

# Directory containing the switch information files
directory = "/home/sysadmin/Documents/switchingautomation/"

# Create a new Excel file
workbook = xlsxwriter.Workbook('switch_results.xlsx')
worksheet = workbook.add_worksheet()

# Write the header row
worksheet.write(0, 0, "File Name")
worksheet.write(0, 1, "Connected Ports")
worksheet.write(0, 2, "Not Connected Ports")
worksheet.write(0, 3, "Disabled Ports")

# Keep track of the current row
row = 1

# Loop through all the files in the directory
for filename in os.listdir(directory):
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        # Initialize counters
        connected = 0
        not_connected = 0
        disabled = 0

        # Open the file and read the data
        with open(os.path.join(directory, filename), 'r') as file:
            # Read the file as a CSV file
            reader = csv.reader(file)
            # Skip the header row
            next(reader)
            # Loop through the rows
            for values in reader:
                # Check the status of each port
                if values[2] == "connected":
                    connected += 1
                elif values[2] == "notconnect":
                    not_connected += 1
                elif values[2] == "disabled":
                    disabled += 1

        # Write the results to the Excel file
        worksheet.write(row, 0, filename)
        worksheet.write(row, 1, connected)
        worksheet.write(row, 2, not_connected)
        worksheet.write(row, 3, disabled)
        # Increment the current row
        row += 1

# Save the Excel file
workbook.close()