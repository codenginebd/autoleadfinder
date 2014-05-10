class CSVFileReader:
    def __init__(self):
        pass
    @staticmethod
    def read_file():
        lead_records = []
        with open('lead_list.csv','r') as file:
            content_list = file.read().split('\n')
            for each_lead in content_list:
                each_lead_cols = each_lead.strip().split(',')
                lead_record_row = {
                    'full_name':'','name2':'','name3':'','address1':'','address2':'','tel':'','fax':'','email':'','web':''
                }
                if len(each_lead_cols) >= 1:
                    lead_record_row['full_name'] = each_lead_cols[0].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 2:
                    lead_record_row['name2'] = each_lead_cols[1].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 3:
                    lead_record_row['name3'] = each_lead_cols[2].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 4:
                    lead_record_row['address1'] = each_lead_cols[3].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 5:
                    lead_record_row['address2'] = each_lead_cols[4].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 6:
                    lead_record_row['tel'] = each_lead_cols[5].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 7:
                    lead_record_row['fax'] = each_lead_cols[6].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 8:
                    lead_record_row['email'] = each_lead_cols[7].replace('"','').decode('utf_8','ignore')
                if len(each_lead_cols) >= 9:
                    lead_record_row['web'] = each_lead_cols[8].replace('"','').decode('utf_8','ignore')
                lead_records += [lead_record_row]
        return lead_records

    @staticmethod
    def read_keywords():
        keywords_file = 'keywords.csv'
        keywords = []
        with open(keywords_file,'r') as file:
            content_list = file.read().split('\n')
            keywords = content_list
        return keywords