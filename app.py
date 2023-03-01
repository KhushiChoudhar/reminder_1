import os
import streamlit as st
import telebot
from apscheduler.schedulers.blocking import BlockingScheduler
from telebot import types
import re
from datetime import datetime
from bob_telegram_tools.bot import TelegramBot
import matplotlib.pyplot as plt
import firebase_admin
from flask import Flask,request
from firebase_admin import credentials,db,firestore
from firebase_admin import initialize_app, delete_app, get_app
try:
    default_app = get_app()
except ValueError:
    default_app = initialize_app()

try:
    delete_app(default_app)
except ValueError:
    pass
cred = credentials.Certificate({
  "type": os.environ.get("FIREBASE_TYPE"),
  "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
  "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
  "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
  "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
  "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
  "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
  "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
  "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
  "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL")
})

default_app = firebase_admin.initialize_app(cred, {
	'databaseURL': "https://telebot-1ec79-default-rtdb.firebaseio.com"
	})
firestore_client = firebase_admin.firestore.client()
ref_for_user_table = firebase_admin.db.reference("/user")
ref_for_reminder_table = firebase_admin.db.reference("/reminder")

categories = {"Meeting": 1, "Task": 2, "Other": 3}
categoryId = 0
date = ''
time = ''
context = ''
resultSet = ''
li = []
li1 = []
ltvs = []
lim = []
li1m = []
ltvsm = []

bot = telebot.TeleBot(st.secrets["API_TOKEN"])
app = Flask(__name__)
@app.route('/')
@bot.message_handler(commands=['start', 'Start','help','What can u do for me'])
def Send_Welcome(message):
    global msg,chat_id,ref_for_reminder_individual,user_id,user_info,bot_graph
    chat_id = message.chat.id
    user_info_including_key = ref_for_user_table.get()
    for key in user_info_including_key:
        user_info = user_info_including_key[key]
        if user_info['chatId']==chat_id:
            user_id =key
            ref_for_reminder_individual = firebase_admin.db.reference("/reminder/" + str(chat_id))
            msg = bot.reply_to(message,'Hi ' + user_info['DisplayName']+ '\n\nWhat would you like to do today :'+ "  \n\n1. /Add_Reminder \n\n2. /View_Reminders \n\n3. /Delete_Reminders \n\n4./Mark_Reminders_Complete \n\n5./Visualize_your_progress \n\n6./Exit")
            break
    else:
        msg = bot.reply_to(message, 'Hello, Welcome to the Bot.\n\n Pls Enter a Username: ')
        bot.register_next_step_handler(msg, Register_User)
def Register_User(message):
    value = message.text
    user_information = {'chatId':chat_id,'DisplayName':value,'Completed_assignment':0}
    ref_for_user_table.push(user_information)
    data_in_reminder_table = ref_for_reminder_table.get()
    data_in_reminder_table[chat_id] = {"nothing": "nothing"}
    ref_for_reminder_table.set(data_in_reminder_table)
    bot.send_message(chat_id, 'Registered user succesfully \n /Exit')
    bot.register_next_step_handler(msg, Send_Welcome)
@bot.message_handler(commands=['Exit'])
def Exit(message):
   markup = types.ReplyKeyboardMarkup()
   itembtn = types.KeyboardButton('/Start')
   markup.add(itembtn)
   msg = bot.reply_to(message, 'Well then, Good Bye.',reply_markup=markup)
   bot.register_next_step_handler(msg, Send_Welcome)
@bot.message_handler(commands=['Mainmenu'])
def Mainmenu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('/Add_Reminder')
    itembtn2 = types.KeyboardButton('/View_Reminders')
    itembtn3 = types.KeyboardButton('/Delete_Reminders')
    itembtn4 = types.KeyboardButton('/Mark_Reminders_Complete')
    itembtn5 = types.KeyboardButton('/Visualize_your_progress')
    itembtn6 = types.KeyboardButton('/Edit_Reminders')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4,itembtn5,itembtn6)
    msg = bot.reply_to(message, "options : ", reply_markup=markup)
@bot.message_handler(commands=['Add_Reminder'])
def Add_Reminder(message):
    global time_add_1
    time_add_1 = datetime.now()
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('/Meeting')
    itembtn2 = types.KeyboardButton('/Task')
    itembtn3 = types.KeyboardButton('/Other')
    itembtn4 = types.KeyboardButton('/Exit')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4)
    msg = bot.reply_to(message, "Please select a category for the new reminder:",reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Category_Reminder_Start_Date)
def Add_Category_Reminder_Start_Date(message):
    value = message.text
    value=value.replace('/','')
    global categories
    global categoryId
    categoryId = categories[value]
    markup = types.ReplyKeyboardMarkup(row_width=6)
    itembtn1 = types.KeyboardButton('01')
    itembtn2 = types.KeyboardButton('02')
    itembtn3 = types.KeyboardButton('03')
    itembtn4 = types.KeyboardButton('04')
    itembtn5 = types.KeyboardButton('05')
    itembtn6 = types.KeyboardButton('06')
    itembtn7 = types.KeyboardButton('07')
    itembtn8 = types.KeyboardButton('08')
    itembtn9 = types.KeyboardButton('09')
    itembtn10 = types.KeyboardButton('10')
    itembtn11 = types.KeyboardButton('11')
    itembtn12 = types.KeyboardButton('12')
    itembtn13 = types.KeyboardButton('13')
    itembtn14 = types.KeyboardButton('14')
    itembtn15 = types.KeyboardButton('15')
    itembtn16 = types.KeyboardButton('16')
    itembtn17 = types.KeyboardButton('17')
    itembtn18 = types.KeyboardButton('18')
    itembtn19 = types.KeyboardButton('19')
    itembtn20 = types.KeyboardButton('20')
    itembtn21 = types.KeyboardButton('21')
    itembtn22 = types.KeyboardButton('22')
    itembtn23 = types.KeyboardButton('23')
    itembtn24 = types.KeyboardButton('24')
    itembtn25 = types.KeyboardButton('25')
    itembtn26 = types.KeyboardButton('26')
    itembtn27 = types.KeyboardButton('27')
    itembtn28 = types.KeyboardButton('28')
    itembtn29 = types.KeyboardButton('29')
    itembtn30 = types.KeyboardButton('30')
    itembtn31 = types.KeyboardButton('31')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6,itembtn7,itembtn8,itembtn9,itembtn10,itembtn11,itembtn12,itembtn13,itembtn14,itembtn15,itembtn16,itembtn17,itembtn18,itembtn19,itembtn20,itembtn21,itembtn22,itembtn23,itembtn24,itembtn25,itembtn26,itembtn27,itembtn28,itembtn29,itembtn30,itembtn31)
    msg = bot.reply_to(message, 'Enter Start Date :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Month)
def Add_Month(message):
    value = message.text
    if re.match(r"^(0?[1-9]|[12][0-9]|3[01])$", str(value)):
        global date
        date = value
        markup = types.ReplyKeyboardMarkup(row_width=3)
        jan = types.KeyboardButton('January')
        feb = types.KeyboardButton('February')
        mar = types.KeyboardButton('March')
        apr = types.KeyboardButton('April')
        may = types.KeyboardButton('May')
        jun = types.KeyboardButton('June')
        jul = types.KeyboardButton('July')
        aug = types.KeyboardButton('August')
        sep = types.KeyboardButton('September')
        oct = types.KeyboardButton('October')
        nov = types.KeyboardButton('November')
        dec = types.KeyboardButton('December')
    markup.add(jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec)
    msg = bot.reply_to(message, 'Enter Month :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Year)

def Add_Year(message):
    value = message.text
    global date
    if(value=='January'):
        value = '01'
    if(value=='February'):
        value = '02'
    if(value=='March'):
        value = '03'
    if(value=='April'):
        value = '04'
    if(value=='May'):
        value = '05'
    if(value=='June'):
        value = '06'
    if(value=='July'):
        value = '07'
    if(value=='August'):
        value = '08'
    if(value=='September'):
        value = '09'
    if(value=='October'):
        value = '10'
    if(value=='November'):
        value = '11'
    if(value=='December'):
        value = '12'
    date = value + '-' + date
    markup = types.ReplyKeyboardMarkup(row_width=4)

    y2023 = types.KeyboardButton('2023')
    y2024 = types.KeyboardButton('2024')
    y2025 = types.KeyboardButton('2025')
    y2026 = types.KeyboardButton('2026')
    y2027 = types.KeyboardButton('2027')
    y2028 = types.KeyboardButton('2028')
    y2029 = types.KeyboardButton('2029')
    y2030 = types.KeyboardButton('2030')
    y2031 = types.KeyboardButton('2031')
    markup.add(y2023,y2024,y2025,y2026,y2027,y2028,y2029,y2030,y2031)
    msg = bot.reply_to(message, 'Enter Year :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Time)
def Add_Time(message):
    value = message.text
    global date
    date = value + '-' + date
    markup = types.ReplyKeyboardMarkup(row_width=4)
    itembtn12am = types.KeyboardButton('12 AM')
    itembtn1am = types.KeyboardButton('01 AM')
    itembtn2am = types.KeyboardButton('02 AM')
    itembtn3am = types.KeyboardButton('03 AM')
    itembtn4am = types.KeyboardButton('04 AM')
    itembtn5am = types.KeyboardButton('05 AM')
    itembtn6am = types.KeyboardButton('06 AM')
    itembtn7am = types.KeyboardButton('07 AM')
    itembtn8am = types.KeyboardButton('08 AM')
    itembtn9am = types.KeyboardButton('09 AM')
    itembtn10am = types.KeyboardButton('10 AM')
    itembtn11am = types.KeyboardButton('11 AM')
    itembtn12pm = types.KeyboardButton('12 PM')
    itembtn1pm = types.KeyboardButton('01 PM')
    itembtn2pm = types.KeyboardButton('02 PM')
    itembtn3pm = types.KeyboardButton('03 PM')
    itembtn4pm = types.KeyboardButton('04 PM')
    itembtn5pm = types.KeyboardButton('05 PM')
    itembtn6pm = types.KeyboardButton('06 PM')
    itembtn7pm = types.KeyboardButton('07 PM')
    itembtn8pm = types.KeyboardButton('08 PM')
    itembtn9pm = types.KeyboardButton('09 PM')
    itembtn10pm = types.KeyboardButton('10 PM')
    itembtn11pm = types.KeyboardButton('11 PM')
    markup.add(itembtn12am,itembtn1am,itembtn2am,itembtn3am,itembtn4am,itembtn5am,itembtn6am,itembtn7am,itembtn8am,itembtn9am,itembtn10am,itembtn11am,itembtn12pm,itembtn1pm,itembtn2pm,itembtn3pm,itembtn4pm,itembtn5pm,itembtn6pm,itembtn7pm,itembtn8pm,itembtn9pm,itembtn10pm,itembtn11pm)
    msg = bot.reply_to(message, 'Enter Hour :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Minute)
def Add_Minute(message):
    value = message.text
    global time
    time = value[0:2]
    time1=value[3:6]
    tmp=0
    if(time1=="AM" and time=="12"):
        time="00"
    elif(time1=="PM" and time=="12"):
        print("")
    else:
        if(time1=="PM"):
            tmp=int(time,10)
            tmp=tmp+12
            time=str(tmp)
    markup = types.ReplyKeyboardMarkup(row_width=4)
    itembtn1 = types.KeyboardButton('00')
    itembtn2 = types.KeyboardButton('05')
    itembtn3 = types.KeyboardButton('10')
    itembtn4 = types.KeyboardButton('15')
    itembtn5 = types.KeyboardButton('20')
    itembtn6 = types.KeyboardButton('25')
    itembtn7 = types.KeyboardButton('30')
    itembtn8 = types.KeyboardButton('35')
    itembtn9 = types.KeyboardButton('40')
    itembtn10 = types.KeyboardButton('45')
    itembtn11 = types.KeyboardButton('50')
    itembtn12 = types.KeyboardButton('55')
    markup.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6,itembtn7,itembtn8,itembtn9,itembtn10,itembtn11,itembtn12)
    msg = bot.reply_to(message, 'Enter Minute :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Context)

def Add_Context(message):
    global time,date1
    value = message.text
    date1=""

    time = time+':'+value
    global categoryId,msg,output
    markup = types.ReplyKeyboardMarkup()
    markup = types.ReplyKeyboardRemove(selective=False)
    date[0:4] + "-" + date[5:7] + "-" + date[8:10] + " " + time[0:2] + ":" + time[3:] + ":00"
    startDate = datetime(int(date[:4]), int(date[5:7]), int(date[8:10]), int(time[0:2]), (int(time[3:])+1),59)
    date_now = datetime.now()
    if categoryId == 1 and startDate>date_now :
        msg = bot.reply_to(message, 'Where is the meeting ?',reply_markup=markup)
        bot.register_next_step_handler(msg, Add_Reminder_To_DB)
    elif categoryId == 2 and startDate>date_now:
        msg = bot.reply_to(message, 'What task it is ?',reply_markup=markup)
        bot.register_next_step_handler(msg, Add_Category_Reminder_End_Date)
    elif categoryId == 3 and startDate>date_now:
        msg = bot.reply_to(message, 'What reminder it is ?',reply_markup=markup)
        bot.register_next_step_handler(msg, Add_Category_Reminder_End_Date)
    elif startDate<date_now:
        msg = bot.reply_to(message, 'Wrong date entered.Try Again \n /Exit',reply_markup=markup)
def Add_Category_Reminder_End_Date(message):
    global messageContent
    messageContent = message.text
    markup = types.ReplyKeyboardMarkup(row_width=6)
    itembtn1 = types.KeyboardButton('01')
    itembtn2 = types.KeyboardButton('02')
    itembtn3 = types.KeyboardButton('03')
    itembtn4 = types.KeyboardButton('04')
    itembtn5 = types.KeyboardButton('05')
    itembtn6 = types.KeyboardButton('06')
    itembtn7 = types.KeyboardButton('07')
    itembtn8 = types.KeyboardButton('08')
    itembtn9 = types.KeyboardButton('09')
    itembtn10 = types.KeyboardButton('10')
    itembtn11 = types.KeyboardButton('11')
    itembtn12 = types.KeyboardButton('12')
    itembtn13 = types.KeyboardButton('13')
    itembtn14 = types.KeyboardButton('14')
    itembtn15 = types.KeyboardButton('15')
    itembtn16 = types.KeyboardButton('16')
    itembtn17 = types.KeyboardButton('17')
    itembtn18 = types.KeyboardButton('18')
    itembtn19 = types.KeyboardButton('19')
    itembtn20 = types.KeyboardButton('20')
    itembtn21 = types.KeyboardButton('21')
    itembtn22 = types.KeyboardButton('22')
    itembtn23 = types.KeyboardButton('23')
    itembtn24 = types.KeyboardButton('24')
    itembtn25 = types.KeyboardButton('25')
    itembtn26 = types.KeyboardButton('26')
    itembtn27 = types.KeyboardButton('27')
    itembtn28 = types.KeyboardButton('28')
    itembtn29 = types.KeyboardButton('29')
    itembtn30 = types.KeyboardButton('30')
    itembtn31 = types.KeyboardButton('31')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10,
              itembtn11, itembtn12, itembtn13, itembtn14, itembtn15, itembtn16, itembtn17, itembtn18, itembtn19,
              itembtn20, itembtn21, itembtn22, itembtn23, itembtn24, itembtn25, itembtn26, itembtn27, itembtn28,
              itembtn29, itembtn30, itembtn31)
    msg1 = bot.reply_to(message, 'Enter End Date :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg1,Add_End_Month)

def Add_End_Month(message):
    value = message.text
    global date1
    if re.match(r"^(0?[1-9]|[12][0-9]|3[01])$", str(value)):
        date1 = value
        markup = types.ReplyKeyboardMarkup(row_width=3)
        jan = types.KeyboardButton('January')
        feb = types.KeyboardButton('February')
        mar = types.KeyboardButton('March')
        apr = types.KeyboardButton('April')
        may = types.KeyboardButton('May')
        jun = types.KeyboardButton('June')
        jul = types.KeyboardButton('July')
        aug = types.KeyboardButton('August')
        sep = types.KeyboardButton('September')
        oct = types.KeyboardButton('October')
        nov = types.KeyboardButton('November')
        dec = types.KeyboardButton('December')
    markup.add(jan,feb,mar,apr,may,jun,jul,aug,sep,oct,nov,dec)
    msg1 = bot.reply_to(message, 'Enter Month :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg1, Add_End_Year)

def Add_End_Year(message):
    value = message.text
    global date1
    if(value=='January'):
        value = '01'
    if(value=='February'):
        value = '02'
    if(value=='March'):
        value = '03'
    if(value=='April'):
        value = '04'
    if(value=='May'):
        value = '05'
    if(value=='June'):
        value = '06'
    if(value=='July'):
        value = '07'
    if(value=='August'):
        value = '08'
    if(value=='September'):
        value = '09'
    if(value=='October'):
        value = '10'
    if(value=='November'):
        value = '11'
    if(value=='December'):
        value = '12'

    date1 = value + '-' + date1
    markup = types.ReplyKeyboardMarkup(row_width=4)

    y2023 = types.KeyboardButton('2023')
    y2024 = types.KeyboardButton('2024')
    y2025 = types.KeyboardButton('2025')
    y2026 = types.KeyboardButton('2026')
    y2027 = types.KeyboardButton('2027')
    y2028 = types.KeyboardButton('2028')
    y2029 = types.KeyboardButton('2029')
    y2030 = types.KeyboardButton('2030')
    y2031 = types.KeyboardButton('2031')
    markup.add(y2023,y2024,y2025,y2026,y2027,y2028,y2029,y2030,y2031)
    msg = bot.reply_to(message, 'Enter Year :\n\n/Exit',reply_markup=markup)
    bot.register_next_step_handler(msg, Add_Reminder_To_DB)

def Add_Reminder_To_DB(message):
    value = message.text
    global date1,start_date,end_date
    global output,categoryId
    date1 = value + '-' + date1
    if categoryId == 1:
        output = '\u2757 Reminder - You have a meeting at ' + str(value)+'\u2757'
        date1 = date
    elif categoryId == 2:
        output = '\u2757 Reminder - You have to ' + str(messageContent) +'\u2757'

    elif categoryId == 3:
        output = '\u2757 Reminder - ' + str(messageContent)+'\u2757'

    reminder_info = {"chatId": message.chat.id, "date": date, "time": time, "message": output, "end_date": date1}
    ref_for_reminder_individual.push(reminder_info)
    reminder_info_including_key = ref_for_reminder_individual.get()
    keys=[]
    for key in reminder_info_including_key:
        keys.append(key)
    msg = bot.reply_to(message, 'Reminder Added  \n/Exit')
    global sched
    sched = BlockingScheduler()
    sched.configure(timezone="Asia/Kolkata")
    start_date = date[0:4]+"-"+date[5:7]+"-"+ date[8:10]+" "+time[0:2]+":"+time[3:]+":00"
    end_date = date1[0:4]+"-"+ date1[5:7]+"-"+date1[8:]+" "+time[0:2]+":"+time[3:]+":00"
    print(keys)
    def reminder_update():
        bot.send_message(message.chat.id, output)
    job_id = keys[-2]
    job_id = job_id.replace('-','')
    print(job_id)
    sched.add_job(reminder_update,'interval', id=job_id, days=1, start_date=start_date, end_date=end_date)
    sched.start()
@bot.message_handler(commands=['View_Reminders'])
def View_Reminders(message):
    reminder_info_including_key = ref_for_reminder_individual.get()
    for key in reminder_info_including_key:
        reminder_info = str(reminder_info_including_key[key]).replace('}', '')
        reminder_info =reminder_info.replace('{','')
        msg = bot.reply_to(message,reminder_info)
@bot.message_handler(commands=['Mark_Reminders_Complete'])
def Mark_Reminders_Complete(message):
    global key_dict
    reminder_info_including_key = ref_for_reminder_individual.get()
    key_dict ={}
    Index_no =0
    for key in reminder_info_including_key:
        Index_no = Index_no+1
        key_dict[Index_no]=key
        if (key=='nothing'):
            break
        reminder_info = str(reminder_info_including_key[key]).replace('}', '')
        reminder_info = reminder_info.replace('{', '')
        reminder_info = reminder_info.replace(':', ' ',5)
        msg = bot.reply_to(message, '/'+str(Index_no)+'\n'+reminder_info+'\n')
    msg = bot.reply_to(message,"Please select a reminder by clicking the unique identification number \n /Exit")
    bot.register_next_step_handler(msg, Delete_reminder_database)
    bot.register_next_step_handler(msg, Complete_reminder_database)

def Delete_reminder_database(message):
    index_no = message.text.replace('/', '')
    key = key_dict[int(index_no)]
    print(key)
    ref_for_reminder_individual.child(key).set({})

def Complete_reminder_database(message):
    completedTask = user_info['Completed_assignment']+1
    ref_for_user_table.child(user_id).update({'Completed_assignment': completedTask})
    msg = bot.reply_to(message, "Marked the assignment completed \n /Exit")

@bot.message_handler(commands=['Visualize_your_progress'])
# def Run_asyncio_func(message):
#     asyncio.run(Visualize_your_progress(msg))
def Visualize_your_progress(message):
    bot_graph = TelegramBot(API_TOKEN, chat_id)
    ref_for_completed = firebase_admin.db.reference("/user/"+user_id+'/Completed_assignment')
    complete = ref_for_completed.get()
    if not ref_for_reminder_individual.get():
        pending =0
    else:
        pending = len(ref_for_reminder_individual.get())-1
    Bar_name = ["Completed Assignment","Pending Assignment"]
    Values =[complete, pending]
    plt.figure(figsize=(5, 5))
    plt.bar(Bar_name, Values, color='black',width=0.4)
    plt.xlabel("Type of Assignment")
    plt.ylabel("No. of Assignment")
    plt.title("Track your Progress")
    bot_graph.send_plot(plt)
    if(pending<complete):
        msg = bot.reply_to(message, '\U0001F929 \U0001F973 To be honest, I don’t know how you manage to do such a good job every single time. \n/Exit to main menu')
        bot.register_next_step_handler(msg, Send_Welcome)
    else:
        msg = bot.reply_to(message,"\U0001F913 \U0001F605 LESSSSGOOOOOOO \n/Exit to main menu")
        bot.register_next_step_handler(msg, Send_Welcome)

@bot.message_handler(commands=['Delete_Reminders'])
def Delete_Reminders(message):
    global key_dict
    value = message.text
    reminder_info_including_key = ref_for_reminder_individual.get()
    key_dict = {}
    Index_no = 0
    for key in reminder_info_including_key:
        if (key == 'nothing'):
            break
        Index_no = Index_no + 1
        key_dict[Index_no] = key
        reminder_info = str(reminder_info_including_key[key]).replace('}', '')
        reminder_info = reminder_info.replace('{', '')
        reminder_info = reminder_info.replace(':', ' ', 5)
        msg = bot.reply_to(message, '/'+str(Index_no)+" "+ reminder_info + '\n')
    msg = bot.reply_to(message, "Please select a reminder by clicking the unique identification number \n /Exit")
    bot.register_next_step_handler(msg, Delete_apscheduler)
    bot.register_next_step_handler(msg, Delete_reminder_database)

def Delete_apscheduler(message):
    index_no = message.text.replace('/', '')
    job_id = key_dict[int(index_no)]
    job_id = job_id.replace('-', '')
    sched.remove_job(job_id)
    bot.reply_to(message, "Deleting Reminder \U0001F929 \U0001F973  \n /Exit")

bot.enable_save_next_step_handlers(delay=2)
bot.polling()
if __name__ == '__main__':
    socketio.run(app)
