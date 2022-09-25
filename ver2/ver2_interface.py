import tkinter
import ver2


def take_url():
    global collector
    collector= ver2.GrafMaker(entery_space.get())
    collector.fill_heroes_rel_with_data()
    # collector.graf_make()
    hero_rels_button.pack()
    hero_names_button.pack()
    # graff_vision_based_on_wight.pack()

def copy_hero_rels():
    global collector
    global root
    root.clipboard_clear()
    root.clipboard_append(collector.heroes_rel_to_str())

def copy_hero_names():
    global collector
    global root
    root.clipboard_clear()
    root.clipboard_append(collector.heroes_dic_to_str())

def weight_vision_on():
    global collector
    global root
    collector.wight_vision_on()


root=tkinter.Tk()
collector=''
entery_space= tkinter.Entry(root)
submit_button=tkinter.Button(root,text='submit',command=take_url)

hero_names_button=tkinter.Button(root,text='Copy name list',command=copy_hero_names)
hero_rels_button=tkinter.Button(root,text='Copy matrix',command=copy_hero_rels)
graff_vision_based_on_wight=tkinter.Button(root,text='Weight vision ON',command=weight_vision_on)
entery_space.pack()
submit_button.pack()

root.mainloop()

