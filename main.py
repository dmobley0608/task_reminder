import csv
import random
import time
import DataRetrieval
from TextMessage import Text as txt_msg
from tkinter import Tk, Canvas, Frame, Label, Entry, Button, StringVar, Text
from threading import Thread

dr = DataRetrieval.AutoDataRetrieval()


def insert_task(date, sched_time, phone, email, message):
    with open("scheduled_tasks.csv", 'a+', newline='') as tasks:
        fieldnames = ["Date", "Time", "Phone", "Email", "Message"]
        writer = csv.DictWriter(tasks, fieldnames)
        writer.writerow({"Date": date, "Time": sched_time, "Phone": phone, "Email": email, "Message": message})


root = Tk()
root.title("Task Scheduler")

# Input Variable
date = StringVar()
sched_time = StringVar()
phone = StringVar()
email = StringVar()
message = StringVar()

main_canvas = Canvas(root)
main_canvas.pack()
main_frame = Frame(main_canvas)
main_frame.pack()
submit_btn_frame = Frame(main_canvas)
submit_btn_frame.pack()

header = Label(main_frame, text='Task Scheduler')
header.grid(column=0, row=0, columnspan=3)

date_lbl = Label(main_frame, text='Date:')
date_lbl.grid(column=0, row=1, sticky='sw')
date_input = Entry(main_frame, textvariable=date)
date_input.grid(column=1, row=1, sticky='w', pady=(0, 5))

time_lbl = Label(main_frame, text='Time:')
time_lbl.grid(column=0, row=2, sticky='sw')
time_input = Entry(main_frame, textvariable=sched_time)
time_input.grid(column=1, row=2, sticky='w', pady=(0, 5))

phone_lbl = Label(main_frame, text='Phone #:')
phone_lbl.grid(column=0, row=3, sticky='sw')
phone_input = Entry(main_frame, textvariable=phone)
phone_input.grid(column=1, row=3, sticky='w', pady=(0, 5))

email_lbl = Label(main_frame, text='Email:')
email_lbl.grid(column=0, row=4, sticky='sw')
email_input = Entry(main_frame, textvariable=email)
email_input.grid(column=1, row=4, sticky='w', pady=(0, 5))

msg_lbl = Label(main_frame, text='Message:')
msg_lbl.grid(column=0, row=5, sticky='sw')
msg_input = Text(main_frame, height=5, width=75)
msg_input.grid(column=1, row=5, pady=(0, 5))

current_time_lbl = Label(main_frame)
current_time_lbl.grid(column=7, row=2, sticky='w')
current_time_lbl_1 = Label(main_frame, text='Current Time:')
current_time_lbl_1.grid(column=6, row=2, sticky='w')

current_date_lbl = Label(main_frame)
current_date_lbl.grid(column=7, row=1)
current_date_lbl_1 = Label(main_frame, text='Today is:')
current_date_lbl_1.grid(column=6, row=1)

report_lbl = Label(main_frame)
report_lbl.grid(column=2, row=2, columnspan=4)


submit_btn = Button(submit_btn_frame, text='ADD REMINDER',
                    command=lambda: insert_task(date.get(), sched_time.get(), phone.get(), email.get(),
                                                msg_input.get("1.0", "end").strip()))
submit_btn.pack()


def send_reminder():
    while True:
        time.sleep(1)

        day = time.strftime("%m%d%Y")
        current_date_lbl.config(text=day)

        current_time = time.strftime("%H%M%S")
        current_time_lbl.config(text=current_time)

        with open('scheduled_tasks.csv', 'r') as tasks_doc:
            tasks = csv.DictReader(tasks_doc)
            try:
                for task in tasks:
                    if day == task["Date"] and current_time == task["Time"]:
                        log_txt = open("log.txt", 'a+')
                        text = txt_msg()
                        text.send_msg(task["Phone"] + "@txt.att.net", task["Message"].strip())
                        report_lbl.config(text=f"sent message to {task['Phone']} on {day} at {current_time}\n")
                        log_txt.write(f"sent message to {task['Phone']} on {day} at {current_time}\n")
                        log_txt.close()
                    if task['Date'] == '' and current_time == task["Time"]:
                        log_txt = open("log.txt", 'a+')
                        text = txt_msg()
                        text.send_msg(task["Phone"] + "@txt.att.net", task["Message"].strip())
                        report_lbl.config(text=f"sent message to {task['Phone']} on {day} at {current_time}\n")
                        log_txt.write(f"sent message to {task['Phone']} on {day} at {current_time}\n")
                        log_txt.close()
            except Exception as e:
                lbl = Label(main_frame, text=e)
                lbl.grid(column=2, row=4, columnspan=3)


thread_1 = Thread(target=send_reminder)
thread_1.daemon = True
thread_1.start()
root.mainloop()
