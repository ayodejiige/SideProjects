from datetime import datetime
from commute import CommuteModes, CommuteTracker, CommuteReport
import json


import gspread # used for gsheet access
from oauth2client.service_account import ServiceAccountCredentials # used for gsheet access

class SheetColumns(object):
    ADDRESS_COL = 3
    DRIVE_COL = 5
    TRANSIT_COL = 7
    BIKING_COL = 9
    WALKING_COL = 11
    COLS = [DRIVE_COL, TRANSIT_COL, BIKING_COL, WALKING_COL]

def main():
    #  Open google sheet
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    wks = client.open("Vancouver Move").sheet1


    tracker = CommuteTracker()

    values_list = wks.col_values(2)

    for row, val in enumerate(values_list):
        if val:
            # Home address from spreadsheet
            src_address = wks.cell(row+1, SheetColumns.ADDRESS_COL).value
            print ("Updating cells for %s" %(src_address))
            # Work address
            dest_address = "725 Granville St, Vancouver, BC"
            departure_time = datetime(year=2019, day=30, month=9, hour=13)

            # Calculate commute for each mode guve
            for idx, commute_mode in enumerate(CommuteModes.MODES):
                res: CommuteReport = tracker.get_commute(src_address, dest_address, commute_mode, departure_time)

                # Update spreadsheet
                wks.update_cell(row+1, SheetColumns.COLS[idx], res.dist_in_km)
                wks.update_cell(row+1, SheetColumns.COLS[idx]+1, res.time_in_minutes)

if __name__ == '__main__':
    main()
