import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from datetime import date

today = date.today()

# dd/mm/YY
today_date = today.strftime("%d")
cell_names1=['H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ','BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ']
del_date1=int(today_date)
#{cell_names[(del_date-1)*2]}




SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# If modifying these scopes, delete the file token.json.
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '104Ixo6jiLk2PFqJqBKjt7K9IwX1kDkI89mZaWeSJHaM'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


daily_m = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f'ss!G2:BQ33').execute()
daily_meal_view = daily_m.get('values', [])


for_coocker = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range=f'ss!{cell_names1[(del_date1-1)*2]}34:{cell_names1[(del_date1-1)*2+1]}34').execute()
for_coocker_view = for_coocker.get('values', [])
f'''
তারিখ : {del_date1}

দুপুরে মিল সংখ্যা : {for_coocker_view[0][0]}      
রাতে মিল সংখ্যা : {for_coocker_view[0][1]}
'''
#st.write(f'তারিখ : {del_date1}        দুপুরে মিল সংখ্যা : {for_coocker_view[0][0]}      রাতে মিল সংখ্যা : {for_coocker_view[0][1]}')



daily_m_b = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='ss!A1:B34').execute()
daily_bazar_view = daily_m_b.get('values', [])




daily_m_d = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='ss!D1:E34').execute()
deposite_view = daily_m_d.get('values', [])




def input_data():
    ###############################################################################
    m_value=[[n,myverbs]]
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range='ss!B2', valueInputOption='USER_ENTERED', body={'values':m_value})
    response = request.execute()
    ################################################################################################

    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='ss!A1:G13').execute()
    values = result.get('values', [])
    ################################################################################################

bazar_code=st.text_input('ম্যনেজার কোড')
final_cal=st.checkbox('মাস শেষের দেনা পাওনা দেখুন')
if final_cal:
    f_cals = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                        range='ss!BW1:CA33').execute()
    f_cal = f_cals.get('values', [])
    f_dataframe=pd.DataFrame(f_cal)
    st.subheader('দেনা পাওনা')
    st.write(f_dataframe)



names=[]
date_arr=[]
for i in range(31):
    date_arr.append(i+1)
for i in range(len(daily_meal_view)):
    if i>0:
        names.append(daily_meal_view[i][0])


if bazar_code=='121':
    daily_bazar_dataframe=pd.DataFrame(daily_bazar_view)
    st.subheader('দৈনিক বাজারের তালিকা')
    st.write(daily_bazar_dataframe)

    bua_bill=st.text_input('বুয়া বিল',500)
    if bua_bill:
        request12 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'ss!H37', valueInputOption='USER_ENTERED', body={'values':[[bua_bill]]})
        response12 = request12.execute()



    see_dep=st.checkbox('টাকা জমা দেয়ার তালিকা দেখুন')
    if see_dep:
        deposite_dataframe=pd.DataFrame(deposite_view)
        st.subheader('টাকা জমা দেয়ার তালিকা')
        st.write(deposite_dataframe)
        name=st.selectbox('জমাদানকারির নাম',names)
        dp_amount=st.text_input('জমাক্ররত পরিমান')
        nx=names.index(name)+3
        dp_btn=st.button('Add')
        if dp_btn:
            request3 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'ss!E{nx}', valueInputOption='USER_ENTERED', body={'values':[[dp_amount]]})
            response3 = request3.execute()

            st.success('Addded refresh to see the change ')
    bz_date=st.selectbox(' বাজারের তারিখ',date_arr)
    bz_amount=st.text_input(' বাজার  খরচ')
    daily_bazar_btn=st.button('Update')
    if daily_bazar_btn:
        request2 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'ss!B{bz_date+2}', valueInputOption='USER_ENTERED', body={'values':[[bz_amount]]})
        response2 = request2.execute()

        st.success('Addded refresh to see the change ')






#daily_meal_dataframe.set_index(daily_meal_dataframe.iloc[1])
arr=[]
for i in range(len(daily_meal_view)):
    arr.append(daily_meal_view[i][0])

daily_meal_dataframe=pd.DataFrame(daily_meal_view,index=arr)
st.subheader('দৈনিক মিলের তালিকা')
st.write(daily_meal_dataframe)


edit=st.checkbox('EDIT')
if edit:
    
    c1,c2,c3,c4=st.beta_columns(4)
    with c1:
        name=st.selectbox('নাম',names)
    
    with c2:
        del_date=st.selectbox('তারিখ      ',date_arr)
        int(del_date)
        nn=names.index(name)+1
    


    with c3:
        no_of_meal_lunch=st.radio("দুপুরে মিলসংখ্যা",(0,1,2,3,4))
    with c4:
        no_of_meal_dinner=st.radio("রাতে মিলসংখ্যা",(0,1,2,3,4))
    cell_names=['H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ','BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BK', 'BL', 'BM', 'BN', 'BO', 'BP', 'BQ']
    up_btn=st.button('update')
    if up_btn:

        request1 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'ss!{cell_names[(del_date-1)*2]}{nn+2}', valueInputOption='USER_ENTERED', body={'values':[[no_of_meal_lunch]]})
        response1 = request1.execute()
        
        request11 = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'ss!{cell_names[(del_date-1)*2+1]}{nn+2}', valueInputOption='USER_ENTERED', body={'values':[[no_of_meal_dinner]]})
        response11 = request11.execute()












