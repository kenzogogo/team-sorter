from asyncio import selector_events
import json, os
from time import sleep
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from numpy import array

#Tkinter(GUI) version 1.0

class app():
    def __init__(self):
        self.path1  = "data/teams.json" #path to teams database
        self.path2 = "data/playoffs.json" #path to the playoffs database
        #check if both files exists
        try:
            if os.path.exists(self.path1) == True:
                with open(self.path1, "r") as team_json:
                    self.team_list = json.load(team_json)
                print(f"{self.path1} Loaded")
            else:
                f = open(self.path1, "a")
                f.write("{}")
                f.close
                print(f"{self.path1} File Created")
            if os.path.exists(self.path2) == True:
                with open(self.path2, "r") as games_json:
                    self.games_list = json.load(games_json)
                print(f"{self.path2} Loaded")
            else:
                f = open(self.path2, "a")
                f.write("{}")
                f.close
                print(f"{self.path2} File Created")
        except:
            print("Error creating .json files.")
            for i in range(1,3, -1):
                print(f"Exiting in {i}")
                sleep(1)
        try:
            with open(self.path1, "r") as team_json:
                self.team_list = json.load(team_json)
            with open(self.path2, "r") as games_json:
                self.games_list = json.load(games_json)
            os.system("title Team Sorter GUI")
        except:
            print("Error reading .json files.")
            for i in range(1,3, -1):
                print(f"Exiting in {i}")
                sleep(1)

    #dump data into database
    def jdump(self, content, target):
        json.dump(content, open(target, "w"), indent=4)

    #create team(and players key) and then call jdump
    def create_team(self, team):
        for i in range(1,25):
            self.team_list[i] = {}
        self.jdump(self.team_list, self.path1)
        # if not team in self.team_list:
        #     self.team_list[team] = {}
        #     try:
        #         for i in range(1,6):
        #             self.team_list[team][f"Player{i}"] = ""
        #         self.jdump(self.team_list, self.path1)
        #     except:
        #         messagebox.showerror("Error", "Unable to write team in database.")
        # else:
        #     messagebox.showerror("Error", "This team already exists")

    #create GUI  
    def root(self):
        #setup main gui
        root = Tk()
        root.geometry("1440x800")
        root.title('Team Sorter GUI')
        root.resizable(True, True)

        #setup dropdown menu
        menubar = Menu(root)
        options = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Team Editor", command=lambda : self.team_editor_gui())
        options.add_separator()
        options.add_command(label="Exit", command=root.destroy)

        team_label = Label(root, text="Team Name")
        team_label.config(font=("Courier", 20))
        team_label.place(x=20, y=10)

        team_entry = Entry(root)
        team_entry.config(font=("Courier", 20))
        team_entry.place(x=20,y=50, width=250, height=40)

        team_create = Button(root, text="Create Team", command=lambda : [self.create_team(team_entry.get()), team_entry.delete(0, 'end')])
        team_create.config(font=("Courier", 10))
        team_create.place(x=20, y=100, height=40, width=110)
        
        root.config(menu=menubar)
        root.mainloop()

    #START OF TEAM EDITOR GUI
    #create team_editor GUI  
    def team_editor_gui(self):
        #setup team_editor gui
        team_editor = Tk()
        team_editor.geometry("1440x800")
        team_editor.title('Team Editor')
        team_editor.resizable(False, False)

        #setup dropdown menu
        menubar = Menu(team_editor)
        options = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options)
        options.add_command(label="Refresh", command=lambda : team_refresh())
        options.add_separator()
        options.add_command(label="Exit", command=team_editor.destroy)
        
        #team selected label
        team_selected_label = Label(team_editor, text=f"Selected > ")
        team_selected_label.config(font=("Courier", 20))
        team_selected_label.place(x=20, y=10)

        #team refresh button
        team_refresh_button = Button(team_editor, text="Refresh", command=lambda : [team_refresh(), team_refresh_button.destroy()])
        team_refresh_button.config(font=("Courier", 10))
        team_refresh_button.place(x=20, y=50, height = 40, width=110)

        #creates the team_select button for each team
        def team_refresh():
            team_edit_panel = LabelFrame(team_editor, text="EDIT PANEL", borderwidth=1, relief=SOLID)
            team_edit_panel.place(x=5, y= 5, width=1430, height=790)
            var1 = 10 #y value for the button to be placed 
            var2 = 240 #x value for the button to be placed
            if len(self.team_list) > 12:
                teams = list(self.team_list)
                for i in range(0, len(teams)):
                    if (i % 2) == 0:
                        team = teams[i]
                        var1 += 40
                        team_select = Button(team_edit_panel, text=team, command=lambda team=team: team_selected(team)) #use lambda team=team to assign the team value in the time of creation!
                        team_select.config(font=("Courier", 10))
                        team_select.place(x=20, y=var1, height = 40, width=110)
                    else:
                        team = teams[i]
                        team_select = Button(team_edit_panel, text=team, command=lambda team=team: team_selected(team))
                        team_select.config(font=("Courier", 10))
                        team_select.place(x=var2, y=var1, height = 40, width=110)
            else:
                for team in self.team_list:
                    var1 += 40
                    team_select = Button(team_edit_panel, text=team, command=lambda team=team: team_selected(team))
                    team_select.config(font=("Courier", 10))
                    team_select.place(x=20, y=var1, height = 40, width=110)

            #Creates buttons for the team selected, creates the team_edit_frame which contains buttons to edit name and edit players
            def team_selected(team):
                team_selected_label.config(text=f"Selected > {team}")
                
                team_edit_frame = LabelFrame(team_edit_panel, text="EDIT OPTIONS", borderwidth=1, relief=SOLID)
                team_edit_frame.place(x=820, y= 10, width=600, height=(team_edit_panel.winfo_height() - 60))

                edit_name = Button(team_edit_frame, text="Edit name", command=lambda : edit_teams_name(team))
                edit_name.config(font=("Courier", 10))
                edit_name.place(x=10, y=10, height = 40, width=110)

                edit_players = Button(team_edit_frame, text="Edit players", command=lambda : edit_teams_players(team))
                edit_players.config(font=("Courier", 10))
                edit_players.place(x=130, y=10, height = 40, width=110)

                #edit teams name, creates entry and button to change team name
                def edit_teams_name(team):
                    new_name = Entry(team_edit_frame)
                    new_name.config(font=("Courier", 10))
                    new_name.place(x=10,y=90, height=40, width=250)

                    change_name = Button(team_edit_frame, text="Apply Change", command=lambda : change_name_apply(team))
                    change_name.config(font=("Courier", 10))
                    change_name.place(x=270, y=90, height=40, width=110)
                    def change_name_apply(team):
                        if not new_name.get() in self.team_list:
                            self.team_list[new_name.get()] = self.team_list[team]
                            del self.team_list[team]
                            self.jdump(self.team_list, self.path1)
                        else:
                            messagebox.showerror(title="Error", message="There is a team with the same name.")

                #edit teams players, creates entries and buttons to change players name
                def edit_teams_players(team):
                    var1 = 90
                    arr = []
                    for i in range(0,5):
                        new_player = Entry(team_edit_frame)
                        arr.append(new_player)
                        new_player.config(font=("Courier", 10))
                        new_player.place(x=10,y=var1, height=40, width=250)

                        change_player = Button(team_edit_frame, text=f"Apply Player {i + 1}", command=lambda i=i: change_player_apply(team, i, arr[i].get()))
                        change_player.config(font=("Courier", 10))
                        change_player.place(x=270, y=var1, height=40, width=130)
                        var1 += 60
                    change_all_players = Button(team_edit_frame, text="Apply All Players", command=lambda : change_player_apply(team, None, None, True))  
                    change_all_players.config(font=("Courier", 10))
                    change_all_players.place(x=430, y=210, height=40, width=150)
                    
                    #function used to apply team players name
                    def change_player_apply(team, number, player, all=False):
                        if all == False:
                            self.team_list[team][f"Player{number + 1}"] = player
                            self.jdump(self.team_list, self.path1)
                        else:
                            for i in range(0,5):
                                self.team_list[team][f"Player{i + 1}"] = arr[i].get()
                            self.jdump(self.team_list, self.path1)
        
        team_editor.config(menu=menubar)
        team_editor.mainloop()
        #END OF TEAM EDITOR GUI


    def main(self):
        self.root()
        
if __name__ == "__main__":
    App = app()
    App.main()
