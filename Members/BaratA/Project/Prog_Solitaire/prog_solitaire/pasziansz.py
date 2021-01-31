#from _typeshed import NoneType
import os

import pygame
import osztalyok
#import eger
# Import other modules from pygame_cards if needed.
from pygame_cards import game_app, controller, enums, card_holder, deck, card


class MyGameController(controller.Controller):
    """ Main class that controls game logic and handles user events.

        Following methods are mandatory for all classes that derive from Controller:
            - build_objects()
            - start_game()
            - process_mouse_events()

        Also these methods are not mandatory, but it can be helpful to define them:
            - execute_game()
            - restart_game()
            - cleanup()

        These methods are called from higher level GameApp class.
        See details about each method below.
        Other auxiliary methods can be added if needed and called from the mandatory methods.
    """

    def build_objects(self):
        """ Create permanent game objects (deck of cards, players etc.) and GUI elements
            in this method. This method is executed during creation of GameApp object.
        """
        setattr(deck.Deck, "render", osztalyok.PlaceHolder)
        #setattr(card_holder.CardsHolder, "render", osztalyok.PlaceHolder)
        #setattr()

        talon_pos = self.settings_json["talon"]["position"]
        talon_offset = self.settings_json["talon"]["offset"]
        atlapos = self.settings_json["atlapoz"]["position"]
        atlapoffset = self.settings_json["atlapoz"]["offset"]
        asztal_pos = self.settings_json["asztal"]["position"]
        asztal_offset = self.settings_json["asztal"]["offset"]
        asztal_inner_offset = self.settings_json["asztal"]["inner_offset"]
        oszlop_pos = self.settings_json["oszlop"]["position"]
        oszlop_offset = self.settings_json["oszlop"]["offset"]
        oszlop_inner_offset = self.settings_json["oszlop"]["inner_offset"]
        
        self.custom_dict["talon"] = deck.Deck(enums.DeckType.full, talon_pos, talon_offset, None)
        self.custom_dict["atlapoz"] = card_holder.CardsHolder(atlapos,atlapoffset,enums.GrabPolicy.can_single_grab)
        self.custom_dict["pro"] = osztalyok.Asztal()
        self.custom_dict["asztal"] = []
        self.custom_dict["oszlop"] = []
        self.custom_dict["purgatory"] = osztalyok.Purgatory()
        self.custom_dict["kez"] = osztalyok.Kez((0, 0), asztal_inner_offset)
        self.custom_dict["elozmeny"] = None
        

        for i in range(1,8):
            asztal = osztalyok.Asztal(asztal_pos, asztal_inner_offset, enums.GrabPolicy.can_multi_grab)
            asztal_pos = asztal_pos[0] + asztal_offset[0], asztal_pos[1] + asztal_offset[1]
            self.add_rendered_object(asztal)
            self.custom_dict["asztal"].append(asztal)

        suits = ["pikk","coeur","treff","karo"]

        for i in range(4):
            oszlop = osztalyok.Oszlop(oszlop_pos,oszlop_inner_offset)
            oszlop_pos = oszlop_pos[0] + oszlop_offset[0], oszlop_pos[1] + oszlop_offset[1]
            self.add_rendered_object(oszlop)
            self.custom_dict["oszlop"].append(oszlop)#,[suits[i]]))
            

        self.add_rendered_object(self.custom_dict["talon"])
        self.add_rendered_object(self.custom_dict["atlapoz"])
        self.add_rendered_object(self.custom_dict["purgatory"])
        self.add_rendered_object(self.custom_dict["kez"])

        pass

    def start_game(self):
        """ Put game initialization code here. For example: dealing of cards,
            initialization of game timer etc. This method is triggered by GameApp.execute().
        """
        self.custom_dict["talon"].shuffle()
        for asztalszam in range(1,8):
            for kartyaszam in range(asztalszam):
                kartya_ = self.custom_dict["talon"].pop_top_card()
                if kartyaszam == asztalszam - 1:
                    kartya_.flip()

                self.custom_dict["asztal"][asztalszam-1].add_card(kartya_)
        pass

    def process_mouse_event(self, pos, down, double_click):
        """ Put code that handles mouse events here. For example: grab card from a deck
            on mouse down event, drop card to a pile on mouse up event etc.
            This method is called every time mouse event is detected.
            :param pos: tuple with mouse coordinates (x, y)
            :param down: boolean, True for mouse down event, False for mouse up event
            :param double_click: boolean, True if it's a double click event
        """
        if down:

            if self.custom_dict["talon"].is_clicked(pos):
                kartya_ = self.custom_dict["talon"].pop_top_card()
                if kartya_ is not None:
                    self.custom_dict["atlapoz"].add_card(kartya_)
                    kartya_.flip()
                elif kartya_ is None:
                    if len(self.custom_dict["talon"].cards) == 0:
                        if len(self.custom_dict["atlapoz"].cards) == 0:
                            return
                        else:
                            self.custom_dict["atlapoz"].move_all_cards(self.custom_dict["talon"])
                            return

            elif self.custom_dict["atlapoz"].is_clicked(pos):
                kartyak = self.custom_dict["atlapoz"].try_grab_card(pos)
                if kartyak is not None:
                    for kartya_ in kartyak:
                        self.custom_dict["kez"].add_card(kartya_)
                    self.custom_dict["elozmeny"] = self.custom_dict["atlapoz"]

            else:
                mpos = pygame.mouse.get_pos()
                asztalcount = 0
                if len(self.custom_dict["kez"].cards) == 0:
                    for asztal in self.custom_dict["asztal"]:
                        kartyak = asztal.try_grab_card(pos)
                        if kartyak is not None:
                            for kartya_ in kartyak:
                                self.custom_dict["kez"].add_card(kartya_)
                            self.custom_dict["elozmeny"] = asztal
                            break

                
        
        if not down:
            mpos = pygame.mouse.get_pos()
            asztalcount = 0

            if len(self.custom_dict["kez"].cards) == 0:
                if (220 <= mpos[1] <= 510) and (18 <= mpos[0] <= 1228):
                        for asztal in self.custom_dict["asztal"]:
                            if asztal.pos[0] <= mpos[0] <= asztal.pos[0] + 130 and asztal.pos[1] + (asztalcount * 20) <= mpos[1] <= asztal.pos[1] + 170 + (asztalcount * 20): 
                                kartya_ = asztal.try_grab_card(mpos) 
                                if kartya_ == None:
                                    try:
                                        if asztal.cards[-1].back_up:
                                            asztal.cards[-1].flip()
                                    except:
                                        None
                            asztalcount += 1

            elif len(self.custom_dict["kez"].cards) != 0:                
                if (220 <= mpos[1] <= 510) and (18 <= mpos[0] <= 1228):
                    for asztal in self.custom_dict["asztal"]:
                        if asztal.pos[0] <= mpos[0] <= asztal.pos[0] + 130 + (asztalcount * 20) and asztal.pos[1] + (asztalcount * 20) <= mpos[1] <= asztal.pos[1] + 170 + (asztalcount * 20): 
                            if asztal.fogadkartyat(self.custom_dict["kez"].cards[0]) == True:
                                while len(self.custom_dict["kez"].cards) != 0:
                                    asztal.add_card(self.custom_dict["kez"].pop_bottom_card())

                            
                        asztalcount += 1
                
                
                else:
                    for oszlop in self.custom_dict["oszlop"]:
                        if oszlop.pos[0] <= mpos[0] <= oszlop.pos[0] + 200 and 0 <= mpos[1] <= oszlop.pos[1] + 170:
                            if ((oszlop.fogadkartyat(self.custom_dict["kez"].cards[0]) == True) and (oszlop.check_collide(self.custom_dict["kez"].cards[0]) == True)):
                                oszlop.add_card(self.custom_dict["kez"].pop_card(False))
                                


                if len(self.custom_dict["kez"].cards) != 0:
                    for i in self.custom_dict["kez"].cards:
                        kartya_ = self.custom_dict["kez"].pop_bottom_card()
                        self.custom_dict["elozmeny"].add_card(kartya_)
            
            if self.custom_dict["elozmeny"] is not None:
                if len(self.custom_dict["kez"].cards) != 0:
                    for i in self.custom_dict["kez"].cards:
                        kartya_ = self.custom_dict["kez"].pop_bottom_card()
                        self.custom_dict["elozmeny"].add_card(kartya_)
            

            # x: 18 y: 220
            

        pass

    def MouseDrag(self, pos):
       for i in self.rendered_objects:
            kartya_ = i.try_grab_card(pos)
            if kartya_ is None:
                break
            else:
                for j in kartya_:
                    self.custom_dict["kez"].add_card(kartya_)
            self.custom_dict["elozmeny"] = i 
            
    
    def gyozelem(self):
        telioszlop = 0
        for oszlop in self.custom_dict["oszlop"]:
            if len(oszlop.cards) == 13:
                telioszlop += 1
        if telioszlop == 4:
            print("Nyertél!")


    def restart_game(self):
        """ Put code that cleans up any current game progress and starts the game from scratch.
            start_game() method can be called here to avoid code duplication. For example,
            This method can be used after game over or as a handler of "Restart" button.
        """
        pass

    def execute_game(self):
        """ This method is called in an endless loop started by GameApp.execute().
        IMPORTANT: do not put any "heavy" computations in this method!
        It is executed frequently in an endless loop during the app runtime,
        so any "heavy" code will slow down the performance.
        If you don't need to check something at every moment of the game, do not define this method.
        
        Possible things to do in this method:
             - Check game state conditions (game over, win etc.)
             - Run bot (virtual player) actions
             - Check timers etc.
        """
        

        pass

    def cleanup(self):
        """ Called when user closes the app.
            Add destruction of all objects, storing of game progress to a file etc. to this method.
        """
        pygame.quit()
        pass


def main():
    """ Entry point of the application. """

    # JSON files contains game settings like window size, position of game and gui elements etc.
    # Necessary fields are "window", "card" and "gui" - they are added to settings.json
    # in this example. Feel free to add any custom fields to that file, they will be accessible
    # via "self.settings_json" attribute of your class derived from controller.Controller.
    # See how custom fields from JSON are used in mygame_examples.py
    json_path = os.path.join(os.getcwd(), 'settings.json')

    # Create an instance of GameApp and pass a path to setting json file
    # and an instance of custom Controller object.
    # This will initialize the game, build_objects() from Controller will be called at this step.
    solitaire_app = game_app.GameApp(json_path=json_path, game_controller=MyGameController())

    # Start executing the game. This will call start_game() from Controller,
    # then will be calling execute_game() in an endless loop.
    solitaire_app.execute()

if __name__ == '__main__':
    main()
