"""
Muhammad Subhan & Jawad Ahmed

20I-0873 & 20I-0945

CS-D

"""

from command import Command
import numpy as np
from buttons import Buttons
import torch
from torch import nn


"""

Model Definition 

"""
class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(19, 64)
        self.fc2 = nn.Linear(64, 128)
        self.fc3 = nn.Linear(128, 256)
        self.fc4 = nn.Linear(256, 512)
        self.fc5 = nn.Linear(512, 1)
        self.relu = nn.Sigmoid()       
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.relu(self.fc3(x))
        x = self.relu(self.fc4(x))
        x = self.fc5(x)
        return x
    
class Bot:

    def __init__(self):

        """
        
        Loading the model and putting it into Evaluation Mode

        """
        self.loadmodel = Model()
        self.loadmodel.load_state_dict(torch.load('NN_Model3.pth', map_location=torch.device('cpu')))
        self.loadmodel.eval()
        self.fire_code=["<","!<","v+<","!v+!<","v","!v","v+>","!v+!>",">+Y","!>+!Y"]

        self.exe_code = 1
        self.start_fire=True
        self.remaining_code=[]
        self.my_command = Command()
        self.buttn= Buttons()

    def fight(self,current_game_state,player):

        """
            Determining the My player and enemy player the player variable sent to the function
        """
        if (player=='2'):
            myplayer = current_game_state.player2
            enemyplayer = current_game_state.player1
        elif (player=='1'):
            myplayer = current_game_state.player1
            enemyplayer = current_game_state.player2

        """
        
        Data collection and pre-processing to the requried format

        """
        objects = [
            (current_game_state.timer)/100,
            (myplayer.x_coord-enemyplayer.x_coord)/100,
            (myplayer.y_coord-enemyplayer.y_coord)/100,
            (myplayer.health - enemyplayer.health)/100,
            myplayer.player_id,
            myplayer.health / 100,
            myplayer.x_coord / 100,
            myplayer.y_coord / 100,
            int(myplayer.is_jumping),
            int(myplayer.is_crouching),
            int(myplayer.is_player_in_move),
            #int(''.join(str(var) for var in [int(enemyplayer.player_buttons.up),int(enemyplayer.player_buttons.down),int(enemyplayer.player_buttons.right),int(enemyplayer.player_buttons.left),int(enemyplayer.player_buttons.Y),int(enemyplayer.player_buttons.B),int(enemyplayer.player_buttons.X),int(enemyplayer.player_buttons.A),int(enemyplayer.player_buttons.L),int(enemyplayer.player_buttons.R)]),2),
            enemyplayer.player_id,
            enemyplayer.health / 100,
            enemyplayer.x_coord / 100,
            enemyplayer.y_coord / 100,
            int(enemyplayer.is_jumping),
            int(enemyplayer.is_crouching),
            int(enemyplayer.is_player_in_move),
            int(''.join(str(var) for var in [int(enemyplayer.player_buttons.up),int(enemyplayer.player_buttons.down),int(enemyplayer.player_buttons.right),int(enemyplayer.player_buttons.left),int(enemyplayer.player_buttons.Y),int(enemyplayer.player_buttons.B),int(enemyplayer.player_buttons.X),int(enemyplayer.player_buttons.A),int(enemyplayer.player_buttons.L),int(enemyplayer.player_buttons.R)]),2),
            
        ]

        """
            
            Predicting the Button Number and Decoding it into Binary of Length 10

        """
        newcommand = self.loadmodel(torch.tensor(objects, dtype=torch.float32))
        newcommand = format(int(newcommand.item()), '010b')
        #print(newcommand)


        """"
        
        Setting up the Buttons to be pressed

        """
        self.buttn.up = newcommand[0]=="1"
        self.buttn.down = newcommand[1]=="1"
        self.buttn.right = newcommand[2]=="1"
        self.buttn.left = newcommand[3]=="1"
        self.buttn.Y = newcommand[4]=="1"
        self.buttn.B = newcommand[5]=="1"
        self.buttn.X = newcommand[6]=="1"
        self.buttn.A = newcommand[7]=="1"
        self.buttn.L = newcommand[8]=="1"
        self.buttn.R = newcommand[9]=="1"

        """
            
        Finalize the Buttons and add to command object

        """
        #print(self.buttn.object_to_dict())
        if (player=='2'):
            self.my_command.player2_buttons=self.buttn
        elif (player=='1'):
            self.my_command.player_buttons=self.buttn


        """
        
        Send the Command Back to the Server

        """
        return self.my_command