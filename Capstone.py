import pandas as pd
import numpy as np
from tkinter import *
from pandastable import Table, TableModel

df_new =pd.read_csv('Capstone_modified.csv')
support_data = pd.read_csv('Support_harkirat.csv')
cosine_sim = np.load('cosing_harkirat.npy')
indices = pd.read_csv('indices_harkirat.csv',names = ['name','indices'])

indices = pd.Series(indices.index, index=indices['name']).drop_duplicates()

#get_subsitute ("Girls Nike Pro shorts")

# initialize gui
#insert widgets to process input


class MyWindow:
    def __init__(self, win, win2):
        frame = Frame(win2)
        frame.pack(fill = 'both', expand = True)
        lbl1=Label(win, text='Item')
        t1=Entry(win, bd=3)
        btn1=Button(win, text='Complement')
        btn2=Button(win, text='Substitute')
        lbl1.place(x=100, y=50)
        t1.place(x=300, y=50)
        
        #define user inputs after the command function
        def get_comp():
            value = t1.get()
            df = ( support_data[(support_data['name_x'] == value) | (support_data['name_y'] == value)].sort_values(by = 'support',ascending = False).head(10) )
            pt = Table(frame, dataframe=df)
            pt.place(x = 0, y = 300)
            pt.show()

        def get_subsitute():
            name = t1.get()
            # Get the index of the item that matches the title
            idx = indices[name]

            # Get the pairwsie similarity scores of all items with that items
            sim_scores = list(enumerate(cosine_sim[idx]))

            # Sort the items based on the similarity scores
            def get_key(elem):
                return elem[1]
            sim_scores.sort(key= get_key, reverse=True)
            
            # Get the scores of the 10 most similar items
            sim_scores = sim_scores[1:11]

            # Get the items indices
            item_indices = [i[0] for i in sim_scores]
            
            # Return the top 10 most similar items
            #print (type( df_new['name'].iloc[item_indices]))
            df = (( df_new.iloc[item_indices].sort_values(by = 'price')))
            pt = Table(frame, dataframe=df)
            pt.place(x = 0, y = 300)
            pt.show()
        b1=Button(win, text='Complement',command=get_comp)
        b2=Button(win, text='Substitute',command=get_subsitute)
        #bind functions here
        b1.bind('<Button1>')
        b2.bind('<Button1>')
        b1.place(x=100, y=150)
        b2.place(x=300, y=150)
        #define backend after this line
window=Tk()
window2 = Tk()
mywin=MyWindow(window, window2)
window.title('Pricing Engine')
window.geometry("500x300+10+10")
window2.title('Substitute')
window2.geometry("500x300+10+10")
window.mainloop()
window2.mainloop()