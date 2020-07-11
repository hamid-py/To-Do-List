from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
import datetime
 
engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
 
 
class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='Nothing to do!')
    deadline = Column(Date, default=datetime.datetime.today().date())
 
    def __repr__(self):
        return self.task
 
 
def menu():
    MENU_ITEM = ["Today's tasks", "Week's tasks", "All tasks", "Missed tasks", "Add task", "Delete task", "Exit"]
    for i in range(len(MENU_ITEM)):
        if i == 6:
            print('0) Exit')
        else:
            print(f'{i + 1}) {MENU_ITEM[i]}')
 
 
def add_task_dead_line():
    a = input("Enter deadline")
    b = a.split('-')
    year = b[0]
    month = b[1]
    day = b[2]
    return datetime.datetime(int(year), int(month), int(day)).date()
 
 
def print_task(row):
    if len(row) == 0:
        print('Nothing to do!')
 
    else:
        for i in range(len(row)):
            print(f'{i + 1}. {row[i]}')
 
 
def week_task():
    for i in range(8):
        print()
        today_task = session.query(Task).filter(Task.deadline == (datetime.datetime.now()
                                                + datetime.timedelta(days=i)).date()).all()
        print((datetime.datetime.now() + datetime.timedelta(days=i)).strftime('%A %d %b') + ':')
        print_task(today_task)
 
def prin_task_date(all_task_list):
    for i in range(len(all_task_list)):
        print(f'{i + 1}. {all_task_list[i]}. {(all_task_list[i].deadline).strftime("%d %b")}')
 
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
 
 
exit_ = True
while exit_:
    menu()
    what_to_do = int(input())
    print()
    if what_to_do == 1:
        row = session.query(Task).filter(Task.deadline == datetime.datetime.today().date()).all()
        print(datetime.datetime.now().strftime('%d %b'))
        print_task(row)
    elif what_to_do == 2:
        week_task()
    elif what_to_do == 3:
        print('All tasks:')
        all_task_list = session.query(Task).all()
        prin_task_date(all_task_list)
 
    elif what_to_do == 4:
        missed_task = session.query(Task).filter(Task.deadline < (datetime.datetime.now()
                                                + datetime.timedelta(days= 0)).date()).all()
        print("Missed tasks:")
        prin_task_date(missed_task)
        print()
    elif what_to_do == 5:
        add_task = input('Enter task')
        add_dead = add_task_dead_line()
        new_row = Task(task=add_task, deadline=add_dead)
        print('The task has been added!')
        session.add(new_row)
        session.commit()
    elif what_to_do == 6:
        print('Chose the number of the task you want to delete:')
        all_task_list = session.query(Task).order_by(Task.deadline).all()
        prin_task_date(all_task_list)
        delete_task = int(input())
        for i in range(len(all_task_list)):
            if delete_task == i+1:
                delete_task_final = all_task_list[i]
                session.delete(delete_task_final)
                session.commit()
                print('The task has been deleted!')
 
            elif delete_task - 1 not in range(len(all_task_list)):
                print("Nothing to delete")
                break
 
 
 
    elif what_to_do == 0:
        exit_ = False
