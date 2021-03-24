import tkinter
from ver3 import logic


class MainWindow:

    def __init__(self):

        self.root=tkinter.Tk()
        self.main_frame=tkinter.Frame(self.root)
        self.all_heroes_frame = tkinter.Frame(self.root)

        self.teams_radio_var=tkinter.StringVar(self.all_heroes_frame)
        self.team_a_radio=tkinter.Radiobutton(self.all_heroes_frame,variable=self.teams_radio_var,value='Team A',text='Team A')
        self.team_b_radio = tkinter.Radiobutton(self.all_heroes_frame, variable=self.teams_radio_var,value='Team B',text='Team B')


        self.team_a_entry=tkinter.Entry(self.main_frame)
        self.team_b_entry=tkinter.Entry(self.main_frame)

        self.team_a_label=tkinter.Label(self.main_frame,text='Team A')
        self.team_b_label=tkinter.Label(self.main_frame,text='Team B')

        self.team_a_auto_or_manual_search_var=tkinter.StringVar(self.main_frame)
        self.team_a_auto_or_manual_search_var.set('Auto')
        self.team_a_auto_search_radio=tkinter.Radiobutton(self.main_frame,variable=self.team_a_auto_or_manual_search_var,value='Auto',text='Auto')
        self.team_a_auto_search_radio=tkinter.Radiobutton(self.main_frame,variable=self.team_a_auto_or_manual_search_var,value='Auto',text='Auto')
        self.team_a_manual_search_radio=tkinter.Radiobutton(self.main_frame,variable=self.team_a_auto_or_manual_search_var,value='Manual',text='Manual')

        self.team_b_auto_or_manual_search_var=tkinter.StringVar(self.main_frame)
        self.team_b_auto_or_manual_search_var.set('Auto')
        self.team_b_auto_search_radio=tkinter.Radiobutton(self.main_frame,variable=self.team_b_auto_or_manual_search_var,value='Auto',text='Auto')
        self.team_b_manual_search_radio=tkinter.Radiobutton(self.main_frame,variable=self.team_b_auto_or_manual_search_var,value='Manual',text='Manual')

        self.date_button=tkinter.Button(self.main_frame,text='Choose date',command=self.choose_date)
        self.date= []

        self.submit_button=tkinter.Button(self.main_frame,text='Submit',command=self.search)

        self.a_choice_heroes_button=tkinter.Button(self.main_frame,text='Choose 5 heroes(A)',command=self.switch_to_all_heroes_frame)
        self.b_choice_heroes_button=tkinter.Button(self.main_frame,text='Choose 5 heroes(B)',command=self.switch_to_all_heroes_frame)

        self.a_choice_heroes_button.bind('<Button-1>',self.set_teams_radio_var_a)
        self.b_choice_heroes_button.bind('<Button-1>',self.set_teams_radio_var_b)

        self.reset_a_button=tkinter.Button(self.main_frame, text='Reset', command=self.reset_chosen_heroes)
        self.reset_b_button=tkinter.Button(self.main_frame,text='Reset',command=self.reset_chosen_heroes)

        self.reset_a_button.bind('<Button-1>',self.set_teams_radio_var_a)
        self.reset_b_button.bind('<Button-1>',self.set_teams_radio_var_b)

        self.team_a_analyze_results_label=None  #will be changed in set_teams_power_info_labels
        self.team_b_analyze_results_label=None


        self.analyze_button=tkinter.Button(self.main_frame,text='Analyze',command=self.analyze)
        self.first_stege_place()

    def set_teams_radio_var_a(self,event):
        self.teams_radio_var.set('Team A')

    def set_teams_radio_var_b(self,event):
        self.teams_radio_var.set('Team B')

    def reset_chosen_heroes(self):
        if self.teams_radio_var.get() == 'Team A':
            self.team_a.heroes_for_analyze=[]
        elif self.teams_radio_var.get() == 'Team B':
            self.team_b.heroes_for_analyze=[]

    def get_vector_module(self,power_h,power_c):
        return (power_h**2+power_c**2)**0.5

    def set_teams_power_info_labels(self):
        a_vector_module=self.get_vector_module(self.team_a.heroes_power,self.team_a.connection_power)
        b_vector_module=self.get_vector_module(self.team_b.heroes_power,self.team_b.connection_power)
        print(a_vector_module)
        print(b_vector_module)
        self.team_a_analyze_results_label=tkinter.Label(self.main_frame,text='Pick hero power:{}\n Pick connections power:{}\n Probability:{}%'
                                                        .format(self.team_a.heroes_power,self.team_a.connection_power,
                                                                a_vector_module/(a_vector_module+b_vector_module)*100))

        self.team_b_analyze_results_label=tkinter.Label(self.main_frame,text='Pick hero power:{}\n Pick connections power:{}\n Probability:{}%'
                                                        .format(self.team_b.heroes_power,self.team_b.connection_power,
                                                                b_vector_module/(a_vector_module+b_vector_module)*100))

    def analyze(self):
        print(self.team_a.heroes_for_analyze)
        print(self.team_b.heroes_for_analyze)
        self.team_a.analyze()
        self.team_b.analyze()
        self.set_teams_power_info_labels()
        self.third_stage_grid()

    def choose_date(self):
        def del_dayes_and_end_calendar():
            self.date.insert(0,date_var.get())

            calendar_frame.destroy()
            self.main_frame.grid()


        def del_mounthes_and_grid_dayes():
            self.date.insert(0,date_var.get())
            for button in mounth_buttons:
                mounth_buttons[button].destroy()

            row=0
            column=0

            for day in range(1,32):
                day_buttons[str(day)] = tkinter.Radiobutton(calendar_frame, text=str(day), variable=date_var,
                                                             value=str(day) if day>9 else '0'+str(day), command=del_dayes_and_end_calendar,
                                                             indicatoron=False)
                day_buttons[str(day)].grid(row=row, column=column)
                if column == 6:
                    row += 1
                    column = -1
                column += 1


        def del_years_and_grid_mounth():
            self.date.insert(0,date_var.get())
            for button in year_buttons:
                year_buttons[button].destroy()

            row=0
            column=0

            for mounth in range(len(mounthes)):
                mounth_buttons[mounthes[mounth]] = tkinter.Radiobutton(calendar_frame, text=mounthes[mounth], variable=date_var,
                                                              value=mounth+1 if mounth>9 else '0'+str(mounth+1), command=del_mounthes_and_grid_dayes,
                                                              indicatoron=False)
                mounth_buttons[mounthes[mounth]].grid(row=row, column=column)
                if column == 3:
                    row += 1
                    column = -1
                column += 1

        def grid_years():

            row = 0
            column = 0

            for year in range(2019, 2031):
                year_buttons[str(year)] = tkinter.Radiobutton(calendar_frame, text=str(year), variable=date_var,
                                                              value=str(year), command=del_years_and_grid_mounth,
                                                              indicatoron=False)
                year_buttons[str(year)].grid(row=row, column=column)
                if column == 3:
                    row += 1
                    column = -1
                column += 1


        self.date=[]
        year_buttons={}
        mounth_buttons={}
        day_buttons={}

        date_var=tkinter.StringVar()

        mounthes=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

        calendar_frame=tkinter.Frame(self.root)
        self.main_frame.grid_forget()
        calendar_frame.grid()

        grid_years()


    def switch_to_all_heroes_frame(self):
        self.main_frame.grid_forget()
        self.all_heroes_frame.grid()

    def switch_to_main_frame(self):
        self.all_heroes_frame.grid_forget()
        self.main_frame.grid()

    def first_stege_place(self):
        self.main_frame.grid()

        self.team_a_label.grid(row=0,column=0)
        self.team_a_entry.grid(row=0,column=1)
        self.team_a_auto_search_radio.grid(row=0,column=2)
        self.team_a_manual_search_radio.grid(row=0,column=3)

        self.team_b_label.grid(row=1,column=0)
        self.team_b_entry.grid(row=1,column=1)
        self.team_b_auto_search_radio.grid(row=1,column=2)
        self.team_b_manual_search_radio.grid(row=1,column=3)

        self.date_button.grid(row=2,column=0)
        self.submit_button.grid(row=2,column=1)

    def second_stage_place(self):

        self.a_choice_heroes_button.grid(row=3,column=0)
        self.b_choice_heroes_button.grid(row=3,column=1)

        self.reset_a_button.grid(row=4,column=0)
        self.reset_b_button.grid(row=4,column=1)
        self.analyze_button.grid(row=5,column=1)

        self.team_a_radio.grid(row=0,column=0)
        self.team_b_radio.grid(row=0,column=1)

        self.all_heroes_window()

    def third_stage_grid(self):
        self.team_a_analyze_results_label.grid(row=6,column=0)
        self.team_b_analyze_results_label.grid(row=6,column=1)

    def all_heroes_window(self):

        def add_hero_to_analyze_list():
            nonlocal all_heroes_var
            nonlocal self
            if self.teams_radio_var.get() == 'Team A':
                self.team_a.heroes_for_analyze.append(all_heroes_var.get())
            elif self.teams_radio_var.get() == 'Team B':
                self.team_b.heroes_for_analyze.append(all_heroes_var.get())

        all_heroes_var=tkinter.StringVar()
        all_heroes_var.set(None)
        row=1
        colomn=0
        for hero_name in self.team_a.heroes_stats:
            tkinter.Radiobutton(self.all_heroes_frame,text=hero_name,value=hero_name,variable=all_heroes_var,command=add_hero_to_analyze_list,indicatoron=False).grid(row=row,column=colomn)
            row+=1
            if row==15:
                row=1
                colomn+=1
        tkinter.Button(self.all_heroes_frame,text='Comfirm',command=self.switch_to_main_frame).grid(row=row,column=colomn+2)


    def search(self):

        def manual_search(team):
            def send_diccerct_url():
                id=id_entry.get()
                team.get_team_glico_and_id(id)
                team.fill_hero_dict()

                manual_search_frame.destroy()
                self.main_frame.grid()

            self.main_frame.grid_forget()
            manual_search_frame=tkinter.Frame(self.root)
            team_label=tkinter.Label(manual_search_frame,text='Open page with matches for team {} manualy\n and input team\'s id please'.format(team.team_name.capitalize()))
            id_label=tkinter.Label(manual_search_frame,text='Id:')
            id_entry=tkinter.Entry(manual_search_frame)
            search_submit_button=tkinter.Button(manual_search_frame,text='Submit',command=send_diccerct_url)

            manual_search_frame.grid()
            team_label.grid(row=0,column=0)
            id_label.grid(row=1,column=0)
            id_entry.grid(row=1,column=1)
            search_submit_button.grid(row=2,column=1)

        def auto_search(team):
            try:
                team.find_all_matches()
                team.fill_hero_dict()
            except KeyError:
                print('switching to manual search')
                manual_search(team)


        team_a_name = self.team_a_entry.get()
        self.team_a=logic.DictBuilder(team_a_name)
        if self.date!=[]:
            print(self.date)
            self.team_a.choose_date(self.date)

        if self.team_a_auto_or_manual_search_var.get()=='Auto':
            auto_search(self.team_a)
        elif self.team_a_auto_or_manual_search_var.get()=='Manual':
            manual_search(self.team_a)

        team_b_name=self.team_b_entry.get()
        self.team_b=logic.DictBuilder(team_b_name)
        if self.date!=[]:
            self.team_b.choose_date(self.date)

        if self.team_b_auto_or_manual_search_var.get()=='Auto':
            auto_search(self.team_b)
        elif self.team_b_auto_or_manual_search_var.get()=='Manual':
            manual_search(self.team_b)

        self.second_stage_place()




test=MainWindow()
test.root.mainloop()
