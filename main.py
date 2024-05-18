import sqlite3
from datetime import date
import datetime
import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk
import matplotlib
import matplotlib.figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class GolsApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry('1000x700')
        self.resizable(False, False)
        self.title('goals app')
        self.config(bg='#d9cdcc')  
        self.start_window()
        self.style_btn = Style()
        self.style_btn.configure('TButton', font = ("Verdana", 9),
                foreground = '#20223b', background='#ccefff', bordercolor = '#def1fa')
        
        self.style_frame = Style()
        self.style_frame.configure('TFrame', background = '#edf9fa')

    #----------------------добавление категорий-------------------------

    def create_cat_wind(self): # открываем окно добавления категории
            # открываем окно
        self.create_wcat = tk.Tk()
        self.create_wcat.title('Редактор категорий')
        self.create_wcat.geometry('250x200')
            # вводим данные и переходим к выполнению функции добавления
        lab = ttk.Label(self.create_wcat, text="Введите название категории: ")
        lab.place(x=50, y=40)
        self.cat = ttk.Entry(self.create_wcat)
        self.cat.place(x=60, y=70)
        
        btn = ttk.Button(self.create_wcat, text='добавить', command=self.add_to_cat).place(x=90, y=100)

    def add_to_cat(self): # добавление категории в бд
            # добавляем категорию в таблицу и закрываем всё
        category = self.cat.get()
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO category (name, hours) VALUES (?,?);", (category, 1,))
        conn.commit()
        conn.close()
        self.create_wcat.destroy()
    #------------------------------добавление категорий---------------------       

    def start_window(self):# бедненькое главное окно         
   
        self.notebook_left = ttk.Notebook(self, width=500, height=300)
        self.notebook_left.grid(row=0, column=0)  

        self.notebook_rigth = ttk.Notebook(self, width=500, height=300)
        self.notebook_rigth.grid(row=0, column=1)    

        self.statistikc_frame = ttk.Frame(self.notebook_rigth, width=500, height=300)
        self.statistikc_frame.pack()
        self.track_tasck_frame = ttk.Frame(self.notebook_rigth, width=500, height=300)
        self.track_tasck_frame.pack()

        self.tascks_list = ttk.Frame(self.notebook_left, borderwidth=1, relief="solid", padding=20, width=500, height=300)
        self.tascks_list.pack()
        self.goals_list = ttk.Frame(self.notebook_left)
        self.goals_list.pack()

        self.notebook_left.add(self.tascks_list, text='Задачи')
        self.notebook_left.add(self.goals_list, text='Цели')

        self.notebook_rigth.add(self.statistikc_frame, text='Статистика')
        self.notebook_rigth.add(self.track_tasck_frame, text='Трекер задач')    
        
        self.form_tascks()
        self.statictic_fun()
        self.diary_func()
        self.show_loop()
        self.show_goals()
        
    #-------------------------стандартные задачи----------------------------
    def form_tascks(self): # криво косо выводим задачи
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("SELECT title, clock, category FROM notes WHERE done != 1;")
        notes = cur.fetchall()

        cur.execute("SELECT id, name FROM category")
        cat = cur.fetchall()

        cat = dict(cat)

        anws, lst, j = [], [], 0
        for i in notes:
            lst.append(i[0])
            lst.append(i[1])
            lst.append(cat[i[2]])
            anws.append(lst)
            lst = []
        
        col = ("задача", "часы", "категория")

        self.tasck_tree = ttk.Treeview(self.tascks_list, columns=col, show="headings")
        self.tasck_tree.grid(row=1, column=0, columnspan=2)

        self.tasck_tree.heading("задача", text="задача")
        self.tasck_tree.heading("часы", text="часы")
        self.tasck_tree.heading("категория", text="категория")

        self.tasck_tree.column("#1", stretch=tk.NO, width=250)
        self.tasck_tree.column("#2", stretch=tk.NO, width=50)
        self.tasck_tree.column("#3", stretch=tk.NO, width=150)

        for anw in anws:
            self.tasck_tree.insert("", tk.END, values=anw)
        btn_add_cat = ttk.Button(self.tascks_list, text='добавить категорию', command=self.create_cat_wind).grid(row=2, column=0)
        btn_create = ttk.Button(self.tascks_list, text='добавить задачу', command=self.create_tasck).grid(row=2, column=1)  
        self.btn_del_one = ttk.Button(self.tascks_list, text="Удалить?", command=self.delet).grid(row=0, column=0)
        self.btn_done = ttk.Button(self.tascks_list, text="Сделанно?", command=self.done_func).grid(row=0, column=1)
   
    def add_to_data(self): # добавление задачи в бд
            # получение данных
        name = self.title.get()
        desc = self.description.get("1.0", "end")   
        clock = self.clock.get()
        category = self.category.get()
            # достать нужный id у категории
        conn = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("SELECT id FROM category WHERE name=(?);", (category,))
        id = cur.fetchall()
            # добавить всё в таблицу и всё закрыть
        lst = (name, desc, int(clock), id[0][0], 0)
        cur.execute("""INSERT INTO notes (title, desc, 
                    clock, category, done) 
                    VALUES (?,?,?,?,?);""", lst)
        conn.commit()
        conn.close()
        print('задача добавленна')
        self.tasck_tree.pack_forget()
        self.create_wind.destroy()  
        self.form_tascks() 
        
    def delet(self):        
        item = self.tasck_tree.selection()
        it = self.tasck_tree.item(item)
        print(it["values"][0])

        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute("DELETE FROM notes WHERE id=(?);", (it["values"][0],))
        con.commit()
        con.close()

        self.tasck_tree.delete(self.item[0])
        self.tasck_tree.config(height=len(self.tasck_tree.get_children()))

    def done_func(self):
        item = self.tasck_tree.selection()
        it = self.tasck_tree.item(item)
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute("UPDATE notes SET done = 1 WHERE title = (?);", (it["values"][0],))
        con.commit()
        cur.execute(f"UPDATE category SET hours = hours + {it['values'][1]} WHERE name = (?)", (it['values'][2],))
        con.commit()
        con.close()
        print('done')
        
    def create_tasck(self): # редактор задач
        self.create_wind = tk.Tk()
        self.create_wind.title('Редактор задач')
        self.create_wind.geometry('600x500')

        lab_tit = ttk.Label(self.create_wind, text='Название').place(x=30, y=50)
        self.title = ttk.Entry(self.create_wind, width=70)
        self.title.place(x=100, y=50)

        lab_desc = ttk.Label(self.create_wind, text='Описание задачи').place(x=30, y=100)
        self.description = tk.Text(self.create_wind, width=70, height=10)
        self.description.place(x=30, y=120)        

        lab_clock = ttk.Label(self.create_wind, text='часы').place(x=30, y=300)
        self.clock = ttk.Entry(self.create_wind, width=70)
        self.clock.place(x=100, y=300)      

        conn  = sqlite3.connect('notes.db')
        cur = conn.cursor()
        cur.execute("SELECT name FROM category;")
        categorys = cur.fetchall()
        conn.close()

        lab_cat = ttk.Label(self.create_wind, text='категория').place(x=30, y=360)
        self.category = ttk.Combobox(self.create_wind, values=categorys, width=70)
        self.category.place(x=100, y=360)
        btn_add = ttk.Button(self.create_wind, text='Создать задачу', command=self.add_to_data).place(x=30, y=420)

    # -------------------------ЗАДАЧИ---------------------------

    # ----------------------статистика---------------------
    def statictic_fun(self):
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM category;")
        category = cur.fetchall()
        con.close()
        lst_name, lst_val = [], []
        for cat in category:
            lst_name.append(cat[1])
            lst_val.append(cat[2])
        figure = matplotlib.figure.Figure(figsize=(6, 3), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self.statistikc_frame)
        axes = figure.add_subplot()
        axes.pie(lst_val, labels=lst_name)
        axes.set_title("статистика приоритетов категорий")
        figure_canvas.get_tk_widget().pack(anchor="ne", padx=70, pady=10)

    # ----------------------------реализация дневника------------------------------

    def diary_func(self):

        self.diary_wind = ttk.Frame(self, height=500)
        self.diary_wind.grid(row=1, column=0, columnspan=2)

        self.diary_edit = tk.Text(self.diary_wind, font="Arial 14", width=60, height=50)
        self.diary_edit.pack(side="bottom")
        scrollbar = ttk.Scrollbar(orient='vertical', command=self.diary_edit.yview)
        self.diary_edit["yscrollcommand"]=scrollbar.set
        btn_add_str = ttk.Button(self.diary_wind, text='добавить запись', command=self.add_diary).pack(side="right")
        btn_show_str = ttk.Button(self.diary_wind, text='открыть дневник', command=self.show_funck_diary).pack(side="right")
        data_lab = ttk.Label(self.diary_wind, text='дата-время').pack()
        self.data_d = ttk.Entry(self.diary_wind)
        self.data_d.pack(side="right")
        emo_lab = ttk.Label(self.diary_wind, text='яркая эмоция сейчас').pack()
        self.emtional = ttk.Entry(self.diary_wind)
        self.emtional.pack(side="right")

    def show_funck_diary(self):
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM diary;')
        notest = cur.fetchall()

        con.close()

        diary_wind = tk.Tk()
        diary_wind.geometry("500x800")
        diary_wind.title('сохранённые записи')

        for note in notest:            
            ttk.Label(diary_wind, text=note[2]).pack()
            ttk.Label(diary_wind, text=note[3]).pack()
            ttk.Label(diary_wind, text=note[1]).pack()
        notest = []

    def add_diary(self):
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        lst = []
        lst.append(self.diary_edit.get('1.0', tk.END))
        lst.append(self.data_d.get())
        lst.append(self.emtional.get())
        cur.execute("INSERT INTO diary(notes, data, emotional) VALUES (?,?,?);", lst)
        print('запись добавлена')
        con.commit()
        con.close()

    #-------------------------------реализация дневника------------------------------------------------------------------
    
    # ------------------------трекер задач------------------------
    def add_looper(self):
        day = date.today()
        text = self.entry_loop.get()
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('INSERT INTO looper(name, done_today) VALUES (?,?);', (text, 0))
        con.commit()
        con.close()

    def check_loop(self):
        check = self.loopers.selection_get()
        print(check)
        day = date.today()
        print(day)
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        s = ''
        cur.execute(f'UPDATE looper SET done_today = (?) WHERE id=(?);', (day,check))
        print('done')
        con.commit()
        con.close()
    
    def show_loop(self):        
        self.entry_loop = ttk.Entry(self.track_tasck_frame)
        self.entry_loop.pack()
        btn_add_loop = ttk.Button(self.track_tasck_frame, text='добавить трекер', command=self.add_looper).pack()
        btn_is_done = ttk.Button(self.track_tasck_frame, text='сделано', command=self.upd_loop).pack()
        self.listboxx = tk.Listbox(self.track_tasck_frame, width=80)
        self.listboxx.pack()
        
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM looper;")
        self.loops = cur.fetchall()
        con.close()
        day = date.today()
        for loop in self.loops:        
            if str(loop[2]) == str(day):
                self.listboxx.insert(tk.END, (loop[1] + ' (на сегодня сделано)'))
            else:
                self.listboxx.insert(tk.END, loop[1])   

    def upd_loop(self):
        sel= self.listboxx.curselection()
        sel_id = self.loops[sel[0]]
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute(f"UPDATE looper SET done_today=date('now') WHERE id={sel_id[0]};")
        con.commit()
        con.close()
        print('all done')
    # ------------------------трекер задач---------------------------------

    #-------------------ЦЕЛИ------------------------------------
    def show_goals(self):
        #self.goals_list
        self.goalsbox = tk.Listbox(self.goals_list, width=70, height=10)
        self.goalsbox.pack(side='top')
        btn_done = ttk.Button(self.goals_list, text='сделано', command=self.done_goal).pack(side='bottom')
        btn_del = ttk.Button(self.goals_list, text='удалить', command=self.del_goal).pack(side='bottom')

        self.entry_goal = ttk.Entry(self.goals_list)
        self.entry_goal.pack(side='bottom')
        btn_del = ttk.Button(self.goals_list, text='добавить', command=self.goals_add).pack(side='bottom')       

        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('SELECT name FROM goals')
        self.goals = cur.fetchall()
        con.close()

        for goal in self.goals:
            self.goalsbox.insert(tk.END, goal)

    def upd_goal(self):
        self.goalsbox = tk.Listbox(self.goals_list, width=70, height=10)
        self.goalsbox.pack(side='top')
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('SELECT name FROM goals')
        self.goals = cur.fetchall()
        print(self.goals)
        con.close()

        for goal in self.goals:
            self.goalsbox.insert(tk.END, goal)

    def goals_add(self):
        name = self.entry_goal.get()
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('INSERT INTO goals(name) VALUES (?)', (name,))
        con.commit()
        con.close()
        self.goalsbox.pack_forget()
        self.upd_goal()

    def del_goal(self):
        ind = self.goalsbox.curselection()
        name = self.goals[ind[0]]
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('DELETE FROM goals WHERE name = (?)', (name))
        con.commit()
        con.close()
        self.goalsbox.pack_forget()
        self.upd_goal()

    def done_goal(self):
        ind = self.goalsbox.curselection()
        name = self.goals[ind[0]]
        con = sqlite3.connect('notes.db')
        cur = con.cursor()
        cur.execute('DELETE FROM goals WHERE name = (?)', (name))
        con.commit()
        con.close()
        p_wind = tk.Tk()
        p_wind.geometry('150x200')
        ttk.Label(p_wind, text=f'''Поздравляем! \nВы достигли цели: \n{name[0]}''').pack(anchor='center')
        self.goalsbox.pack_forget()
        self.upd_goal()
    #-------------------ЦЕЛИ------------------------------------

root = GolsApp()
root.mainloop()