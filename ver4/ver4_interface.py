import tkinter
import re
import ver4_logic



class MainWindow:
    def __init__(self):

        self.root=tkinter.Tk()
        self.main_frame=tkinter.Frame(self.root)
        self.all_heroes_frame = tkinter.Frame(self.root)
        self.driver=ver4_logic.GrafMaker("url")

        self.teams_radio_var=tkinter.StringVar(self.all_heroes_frame)
        # self.team_radio=tkinter.Radiobutton(self.all_heroes_frame,variable=self.teams_radio_var,value='Team A',text='Team A')


        self.team_entry=tkinter.Entry(self.main_frame)
        self.team_label=tkinter.Label(self.main_frame,text='Url')


        self.submit_button=tkinter.Button(self.main_frame,text='Submit',command=self.take_url)

        self.choice_heroes_button=tkinter.Button(self.main_frame,text='Choose picked heroes',command=self.switch_to_all_heroes_frame)

        # self.choice_heroes_button.bind('<Button-1>',self.set_teams_radio_var)

        self.chosen_hero_label=tkinter.Label()

        self.reset_button=tkinter.Button(self.main_frame, text='Reset', command=self.reset_chosen_heroes)



        self.analyze_button=tkinter.Button(self.main_frame,text='Analyze',command=self.analyze)
        self.first_stege_place()

    def take_url(self):
        self.driver = ver4_logic.GrafMaker(self.team_entry.get())
        self.driver.fill_heroes_rel_with_data()
        # hero_rels_button.pack()
        # hero_names_button.pack()
        self.second_stage_place()

    def set_teams_radio_var(self,event):
        self.teams_radio_var.set('Team A')

    def reset_chosen_heroes(self):
        self.choose_heroes_all_heroes_var.set(None)
        self.driver.picked_heroes_names = []
        self.chosen_hero_label.grid_forget()


    def analyze(self):
        self.driver.plot_graff()



        """
        cords = {
            "x y":["hero_name"]
        }

        hero_coords = ( self.driver.picked_heroes_dict[hero][total_number_of_picks] , self.driver.picked_heroes_dict[hero][winrate]  )
        dict{
            hero{
                id : 
                total_number_of_picks : int,
                winrate : float % , # round(float, 2)
                connections { # will have info about connections with every other hero
                    hero_name : {
                        win : int,
                        lose : int
                    }
                }
                
            
            }
        
        }
        
        
        """
        ''' Make graffiti'''


    def switch_to_all_heroes_frame(self):
        self.main_frame.grid_forget()
        self.all_heroes_frame.grid()

    def switch_to_main_frame(self):
        self.all_heroes_frame.grid_forget()
        self.main_frame.grid()

    def first_stege_place(self):
        self.main_frame.grid()

        self.team_label.grid(row=0,column=0)
        self.team_entry.grid(row=0,column=1)

        self.submit_button.grid(row=2,column=1)

    def second_stage_place(self):

        self.choice_heroes_button.grid(row=3,column=0)

        self.reset_button.grid(row=5,column=0)
        self.analyze_button.grid(row=6,column=1)

        # self.team_radio.grid(row=0,column=0)

        self.all_heroes_window()


    def all_heroes_window(self):
        def grid_chosen_hero_label(event):
            hero_list_to_str=''.join([hero_name+'\n' for hero_name in self.driver.picked_heroes_names])
            self.chosen_hero_label.grid_forget()
            self.chosen_hero_label=tkinter.Label(self.main_frame,text=hero_list_to_str)
            self.chosen_hero_label.grid(row=4,column=0)


        def add_hero_to_analyze_list():
            nonlocal self
            self.driver.picked_heroes_names.append(self.choose_heroes_all_heroes_var.get())


        self.choose_heroes_all_heroes_var=tkinter.StringVar()
        self.choose_heroes_all_heroes_var.set(None)
        row=1
        colomn=0
        for hero_name in self.driver.heroes_dic:
            tkinter.Radiobutton(self.all_heroes_frame,text=hero_name,value=hero_name,variable=self.choose_heroes_all_heroes_var,command=add_hero_to_analyze_list,indicatoron=False).grid(row=row,column=colomn)
            row+=1
            if row==15:
                row=1
                colomn+=1
        confirm_button=tkinter.Button(self.all_heroes_frame,text='Comfirm',command=self.switch_to_main_frame)
        confirm_button.bind('<Button-1>',grid_chosen_hero_label)
        confirm_button.grid(row=row,column=colomn+2)





test=MainWindow()
test.root.mainloop()
