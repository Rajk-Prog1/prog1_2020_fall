import sys
import pygame
#import pygame_cards
from pygame_cards import card_holder, enums, card

def PlaceHolder(pakli,screen):
    if len(pakli.cards) == 0:
        hely = (pakli.pos[0], pakli.pos[1],card_holder.CardsHolder.card_json["size"][0],card_holder.CardsHolder.card_json["size"][1])
        pygame.draw.rect(screen,(255,255,255),hely,1,5)

class Asztal(card_holder.CardsHolder):
    def render (self,screen):
        PlaceHolder(self,screen)
    
    def FlipCard(self):
        if len(self.cards) > 0 and self.cards[-1].back_up:
            self.cards[-1].flip()

    def fogadkartyat(self, kartya_):
        if len(self.cards) == 0:
            return kartya_.rank == enums.Rank.king
        elif len(self.cards) > 0:
            if self.cards[-1].suit == 0 or self.cards[-1].suit == 1:
                return (kartya_.suit == 2 and kartya_.rank == self.cards[-1].rank - 1) or (kartya_.suit == 3 and kartya_.rank == self.cards[-1].rank - 1)
            else:
                return (kartya_.suit == 0 and kartya_.rank == self.cards[-1].rank - 1) or (kartya_.suit == 1 and kartya_.rank == self.cards[-1].rank - 1)
        elif self.cards[-1].rank == enums.Rank.two:
            if self.cards[-1].suit == 0 or self.cards[-1].suit == 1:
                return (kartya_.suit == 2 and kartya_.rank == enums.Rank.ace) or (kartya_.suit == 3 and kartya_.rank == enums.Rank.ace)
            else:
                return (kartya_.suit == 0 and kartya_.rank == enums.Rank.ace) or (kartya_.suit == 1 and kartya_.rank == enums.Rank.ace)

class Oszlop(card_holder.CardsHolder):
    def render (self,screen):
        PlaceHolder(self,screen)

    def fogadkartyat(self, kartya_):
        if len(self.cards) == 0:
            return kartya_.rank == enums.Rank.ace
        elif len(self.cards) == 1:
            return self.cards[-1].suit == kartya_.suit and kartya_.rank == enums.Rank.two
        else:
            return self.cards[-1].suit == kartya_.suit and kartya_.rank == self.cards[-1].rank + 1

class Purgatory(card_holder.CardsHolder):
    def render_all(self,screen):
        pass

class Kez(card_holder.CardsHolder):
    def add_card(self, card_,on_top = False):
        if isinstance(card_, card.Card):
            if on_top:
                self.cards.append(card_)
            else:
                self.cards.insert(0, card_)
    
    def render(self,screen):
        if len(self.cards) > 0:
            self.pos = self.cards[0].get_sprite().pos
            self.update_position(self.offset)
            _ = screen
    
    

    pass