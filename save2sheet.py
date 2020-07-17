from oauth2client.service_account import ServiceAccountCredentials
import gspread
import csv
import pdb

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)

file = gc.open_by_key("1q54ukloKnibtoHJDsWjJ008y9_cTYD_jM_khefol-eg")


def update_row(sheet,index,data):
    sheet_range = ["A","E"]
    sheet_range[0] += str(index+1)
    sheet_range[1] += str(index+1)
    sheet_range_str = ":".join(sheet_range)
    print(sheet_range_str)
    cell_list = sheet.range(sheet_range_str)
    for i,cell in enumerate(cell_list):
        cell.value = data[i]
    
    sheet.update_cells(cell_list)


def get_row_by_id(sheet,id):
    cell = sheet.find(id)
    row_index = cell.row
    return row_index

def check_row_id_exists(sheet,id):
    exist = None
    try:
        cell = sheet.find(id)
    except:
        exist = False
    else:
        exist = True
    return exist

def update_sheet(name, data):
    # Take care of all cases:
    #
    # Make first char uppercase
    sheet = file.worksheet(name)
    print(sheet)
    sh_data = sheet.get_all_values()[1:]
    #pdb.set_trace()
    keys = ['id','caption','likes','comments','shares']
    if len(sh_data) == 0:
        #No data has been added
        print("sheet is empty")
        #sheet.resize(2)
        for row in data:
            row_data = [row[k] for k in keys]
            sheet.append_row(row_data)
            print("added row")
    else:
        # First we get number of all rows with existing 
        existing_id_rows = []
        for idx,row in enumerate(data):
            if check_row_id_exists(sheet,row["id"]):
                #update row
                row_index = get_row_by_id(sheet,row["id"]) - 1
                row_data = [row[k] for k in keys]
                print("row exists it will get updated ")
                update_row(sheet,row_index,row_data)

            else:
                # row id doesn't exist in the sheet we just add it
                print("row doesn't exist in sheet, we will append it")
                row_data = [row[k] for k in keys]
                sheet.append_row(row_data)



    """
    else:
        # check for each row in the sheet if it's correspending row in the csv has the same id, if not then add it
        for idx,sh_row in enumerate(sh_data):
            if sh_row[0] == data[idx]["id"]:
                # same id case: will update row
                print("same")
                row = data[idx]
                row_data = [row[k] for k in keys]
                update_row(sheet,idx,row_data)
            else:
                # not same id : will add row
                print("not same")
                row = data[idx]
                row_data = [row[k] for k in keys]
                sheet.append_row(row_data)
        sh_num_rows = len(sh_row)+1
        left_data = data[sh_num_rows:]
        for row in left_data:
            row_data = [row[k] for k in keys]
            sheet.append_row(row_data)
            print("added row")
    """

def open_data(name):
    fn = "data/"+name+".csv"
    data = []
    with open(fn) as f:
        a = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        data = a
    return data

full_data = {
    "instagram": open_data("instagram"),
    "facebook": open_data("facebook")
}

update_sheet("Facebook",full_data["facebook"])
update_sheet("Instagram",full_data["instagram"])





