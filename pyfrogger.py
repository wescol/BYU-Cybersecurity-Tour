#!/usr/bin/env python

"""
FGame sample test based on classic Frogger

Build with :
    Python 2.5.4
    Pygame 1.9.1
    FGame

Code is under licence BSD

Copyright (c) 2009, Pierre-Alain Dorange
All rights reserved.
"""

# Import Python Modules
import os
import random
#import datetime
#import time
import math

# Import local modules
from configobj import *
import pygame
from pygame.locals import *

# Import source
from fgame import *

kScreenWidth=768
kScreenHeight=512
kObjectLayer=2
kFrogLayer=3
kOverLayer=10

kPlayWidth=448
kPlayHeight=512
kPlayYLife=482
kPlayXHome=19
kPlayYHome=62
kPlayDXHome=96
kPlayHomeWidth=26
kPLayHomeHeight=36
kPlayYCar=[418,388,358,322,294]
kPlayYRiver=[229,198,166,133,102]
kPlayTimeLoc=(176,496)
kPlayTimeSize=(208,16)
kPlayYHomeLimit=96
kPlayYRiverLimit=248
kPlayFrog=(224.0,485.0)
kPlayCellSize=(32.0,32.0)
kPlayTimer=60.0

kPlayFPSLoc=(0,5)
kMenuFPSLoc=(5,10)

kKillDuration=2000
kGameOverDuration=3000
kNextLevelDuration=1000
kTurtleAnimeRate=500
kTurtleDiveAnimeRate=1500
kHomeBonusDuration=5000

kFlyBonusRate=5.0
kFlyBonusDelay=5.0
kCrocodileBonusRate=10.0
kCrocodileBonusDelay=5.0

kScoreHome=50
kScoreHomeFly=200
kScoreLevel=1000
kScoreUp=10
kScoreTime=10

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# Classes for our game objects

class FrogSprite(FSprite):
    """ FrogSprite : basic class for Frog (player) """
    
    def __init__(self,game):
        FSprite.__init__(self,game)
        self.set_speed((0.0,0.0))
        
    def set_speed(self,speed):
        self.speed=speed
        
    def get_speed(self):
        return self.speed
        
class Frog(FrogSprite):
    """ Frogr : the player sprite """
    
    def __init__(self,game):
        FrogSprite.__init__(self,game)
        self.image=game.frogImg[0]
        self.rect=self.image.get_rect()
        self.jumpSpeed=0.2
        self.moving=False
        self.direction=0
        self.attachTo=None
        self.set_speed((0.0,0.0))
        self.life=1.0
        self.lifeMax=1.0
        self.initial()
        self.register(game.get_sprites(),kFrogLayer)
        
    def initial(self):
        self.upMax=kPlayFrog[1]-kPlayCellSize[1]
        self.set_pos(kPlayFrog)
        self.move_request((0,-1))
        self.game.screen.time.set_value(kPlayTimer)
    
    def attach(self,object):
        self.attachTo=object
    
    def move_request(self,vector):
        #determine destination after the move
        (x,y)=self.get_pos()
        x+=kPlayCellSize[0]*vector[0]
        y+=kPlayCellSize[1]*vector[1]
        
        #check destination is possible : not out of screen and not a home frogged
        canMove=True
        if x+self.rect.width<0.0 or x+self.rect.width>kPlayWidth:
            canMove=False
        if y+self.rect.height<0.0 or y+self.rect.height>kPlayHeight:
            canMove=False
        if y<kPlayYHomeLimit:
            r=Rect((x,y),(self.rect.width,self.rect.height))
            index=r.collidelist(self.game.homes)
            if index>0:
                canMove=not isinstance(self.game.homeFrogged[index],Frog)
            
        #if move possible, start the moving animation
        if canMove:
             self.moving=True
             self.movingDst=(x,y)   #store destination
             self.set_speed((self.jumpSpeed*vector[0],self.jumpSpeed*vector[1]))
             #determine direction and apply to sprite image
             if vector[1]>0.0:
                 self.direction=180
             else:
                 self.direction=0
             if vector[0]<0.0:
                 self.direction=90
             if vector[0]>0.0:
                 self.direction=270
             self.set_image()

    def update(self):
        (x,y)=self.get_pos()
        if self.moving:    # moving animation
            d0=math.hypot(self.movingDst[0]-x,self.movingDst[1]-y)
            self.fmove(self.speed,self.game.get_clock())
            (x,y)=self.get_pos()
            d=math.hypot(self.movingDst[0]-x,self.movingDst[1]-y)
            if d>d0:    #if we reach the destination, stop moving animation
                self.set_pos(self.movingDst)
                self.moving=False
                self.attach(None)
                self.set_speed((0.0,0.0))
                self.set_image()
        else:
            if y<self.upMax:
                self.upMax=y
                self.game.score.add_score(kScoreUp)
                
        if self.attachTo!=None:    # if attached to a river object, do animation
            self.fmove(self.attachTo.speed,self.game.get_clock())
            (x,y)=self.get_pos()
            dx=0.5*self.rect.width
            if x<-dx or x+self.rect.width>kPlayWidth+dx:
                self.hit(self.attachTo)
                
        #Check collision with the frog
        (x,y)=self.get_pos()
        if y<kPlayYHomeLimit:    # home zone
            r=self.get_rect()
            index=r.collidelist(self.game.homes)
            if index<0:
                print "miss home at %.0f,%.0f" % self.get_pos()
                for i in self.game.homes:
                    print "\thome (%d,%d)-(%d,%d)" % (i.left,i.top,i.right,i.bottom)
                self.hit(None)
            else:
                target=self.game.homeFrogged[index]
                if target==None or isinstance(target,HomeFly):
                    self.game.homeBonus=0
                    self.game.homeFrogged[index]=HomeFrog(self.game,self.game.homes[index])
                    self.game.frogged+=1
                    self.initial()
                    if target==None:
                        score=kScoreHome
                        print "hit home %d (total %d)" % (index,self.game.frogged)
                    else:
                        score=kScoreHomeFly+kScoreHome
                        print "hit home %d with fly bonus (total %d)" % (index,self.game.frogged)
                    score+=+kScoreTime*self.game.screen.time.get_value()
                    self.game.score.add_score(score)
                    if self.game.frogged==5:
                        self.game.nextLevel=True
                        self.game.score.add_score(kScoreLevel)
                elif isinstance(target,HomeCrocodile):
                    self.hit(None)
                    print "hit home %d with crocodile" % index
                elif isinstance(target,Frog):
                    print "hit home %d allready frogged : error" % index
        elif y<kPlayYRiverLimit:    # river zone
            r=pygame.sprite.spritecollide(self,self.game.rivers,False)
            if len(r)==0:
                print "fall in river at %.0f,%.0f" % self.get_pos()
                self.hit(None)
            elif isinstance(r[0],Turtle) and r[0].dive:
                print "turtle dive at %.0f,%.0f" % self.get_pos()
                self.hit(None)
            else:
                self.attach(r[0])
        else:     # road zone
            for car in pygame.sprite.spritecollide(self,self.game.cars,False):
                print "hit by a car at %.0f,%.0f" % self.get_pos()
                self.hit(car)

    def set_image(self):
        if self.moving:
            index=1
        else:
            index=0
        self.image=pygame.transform.rotate(self.game.frogImg[index].copy(),self.direction)

    def hit(self,sprite):
        FSprite.hit(self,sprite)
        
        if self.life<=0.0:  # if dead
            frog=DeadFrog(self.game,self.get_pos())

class DeadFrog(FSprite):
    """ Frogger dead : do not moved """
    
    def __init__(self,game,location):
        FSprite.__init__(self,game)
        self.image=game.frogImg[2]
        self.rect=self.image.get_rect()
        self.set_pos(location)
        self.duration=0
        self.register(game.get_sprites(),kFrogLayer)

    def update(self):
        self.duration+=self.game.get_clock()
        if self.duration>kKillDuration:
            self.kill()
        
class HomeFrog(FSprite):
    """ Frogger reach home : do not move """
    
    def __init__(self,game,rect):
        FSprite.__init__(self,game)
        self.image=game.frogImg[0]
        self.rect=self.image.get_rect()
        self.set_pos((rect.left+(rect.width-self.rect.width)/2,rect.top+(rect.height-self.rect.height)/2))
        self.register(game.get_sprites(),kFrogLayer)
        
class HomeFly(FSprite):
    """ Fly in frogger's home : gave bonsu if catch """
    
    def __init__(self,game,rect):
        FSprite.__init__(self,game)
        self.image=game.bonusImg[0]
        self.rect=self.image.get_rect()
        self.set_pos((rect.left+(rect.width-self.rect.width)/2,rect.top+(rect.height-self.rect.height)/2))
        self.register(game.get_sprites(),kFrogLayer)
        self.duration=0

    def update(self):
        self.duration+=self.game.get_clock()
        if self.duration>kHomeBonusDuration:
            if self in self.game.homeFrogged:
                index=self.game.homeFrogged.index(self)
                self.game.homeFrogged[index]=None
                print "remove fly at %d" % index
            else:
                print "remove fly, no index found"
            self.kill()
        
class HomeCrocodile(FSprite):
    """ Crocodile in frogger's home : dead is touched """
    
    def __init__(self,game,rect):
        FSprite.__init__(self,game)
        self.image=game.bonusImg[1]
        self.rect=self.image.get_rect()
        self.set_pos((rect.left+(rect.width-self.rect.width)/2,rect.top+(rect.height-self.rect.height)/2))
        self.register(game.get_sprites(),kFrogLayer)
        self.duration=0

    def update(self):
        self.duration+=self.game.get_clock()
        if self.duration>kHomeBonusDuration:
            if self in self.game.homeFrogged:
                index=self.game.homeFrogged.index(self)
                self.game.homeFrogged[index]=None
                print "remove crocodile at %d" % index
            else:
                print "remove crocodile, no index found"
            self.kill()

class LifeFrog(FSprite):
    """ Life symbol for the player :display at the bottom of the screen """
    
    def __init__(self,game):
        FSprite.__init__(self,game)
        self.image=game.frogImg[3]
        self.rect=self.image.get_rect()
        self.set_pos((0,kPlayYLife))
        self.register(game.get_sprites(),kFrogLayer)
        
class ScrollingSprite(FrogSprite):
    """ Basic class for cars and woods : sprite that scrol horizontally throught screen """
    
    def __init__(self,game):
        FrogSprite.__init__(self,game)
        self.animIndex=0
        self.animFrame=0
        self.animRate=0
        self.animClk=0
        self.set_speed((0.0,0.0))
        
        self.register(game.get_sprites(),kObjectLayer)
        
    def set_anim_sequence(self,sequence):
        self.animSequence=sequence
        self.animIndex=0
        self.animFrame=self.animSequence[self.animIndex][0]
        self.animRate=self.animSequence[self.animIndex][1]
        self.image=self.images[self.animFrame]
        
    def update(self):
        # move the scrolling sprite
        self.fmove(self.speed,self.game.get_clock()) 
        # do the edge dance : move sprite from side to side when offscreen
        (x,y)=self.get_pos()
        (xSpeed,ySpeed)=self.get_speed()
        if xSpeed<0 and x+self.rect.width<0.0:
            self.set_pos((x+kPlayWidth+self.rect.width,y))
        if xSpeed>0 and x>kPlayWidth:
            self.set_pos((x-kPlayWidth-self.rect.width,y))
        # if animate, do the anim dance
        if self.animRate>0:
            self.animClk+=self.game.get_clock()
            if self.animClk>self.animRate:
                self.animClk-=self.animRate
                self.animIndex+=1
                if self.animIndex>=len(self.animSequence):
                    self.animIndex=0
                self.animFrame=self.animSequence[self.animIndex][0]
                self.animRate=self.animSequence[self.animIndex][1]
                self.image=self.images[self.animFrame]

class Car(ScrollingSprite):
    """ Cars : cross the road 
        kill the frog is hit """
    def __init__(self,game,index):
        ScrollingSprite.__init__(self,game)
        self.images=game.carImg
        self.set_anim_sequence([(index,0)])
        self.rect=self.image.get_rect()
        self.damage=1.0

class Log(ScrollingSprite):
    """ Logs : wood cross the river
        transport the frog in the river """
    def __init__(self,game,index):
        ScrollingSprite.__init__(self,game)
        self.images=game.riverImg
        self.set_anim_sequence([(index,0)])
        self.rect=self.image.get_rect()
        self.damage=1.0

class Turtle(ScrollingSprite):
    """ Turtle are specail wood's log that sometime dive into water """
    def __init__(self,game,index):
        ScrollingSprite.__init__(self,game)
        self.baseIndex=index
        self.images=game.riverImg
        self.set_can_dive(False)
        self.image=self.images[self.animIndex]
        self.rect=self.image.get_rect()
        self.damage=1.0
        self.dive=False
    
    def set_can_dive(self,canDive=False):
        self.canDive=canDive
        if self.canDive:
            self.set_anim_sequence([(self.baseIndex,kTurtleAnimeRate),(self.baseIndex+1,kTurtleAnimeRate),(self.baseIndex,kTurtleAnimeRate),(self.baseIndex+1,kTurtleAnimeRate),(self.baseIndex+2,kTurtleAnimeRate),(self.baseIndex+3,kTurtleAnimeRate),(self.baseIndex+4,kTurtleAnimeRate),(self.baseIndex+3,kTurtleAnimeRate),(self.baseIndex+2,kTurtleAnimeRate)])
        else:        
            self.set_anim_sequence([(self.baseIndex,kTurtleAnimeRate),(self.baseIndex+1,kTurtleAnimeRate)])
            
    def update(self):
        ScrollingSprite.update(self)
        if self.canDive:
            self.dive=(self.animIndex==6)
    
class Score(Label):
    """ Handle player's score and display it on screen
        derivate from FGame's Label"""
    
    def __init__(self,game,highScore):
        Label.__init__(self,game,"emulogic.ttf",12)
        self.set_color((255,255,255))
        self.set_position((100,20))
        self.value=0
        self.hiScore=highScore
        self.modified=True
        
        self.register(game.get_sprites(),kFrontLayer)

    def update(self):
        if self.changed:
            self.set_text("%05d" % self.value)
        Label.update(self)

    def add_score(self,v):
        self.value+=v
        self.changed=True
        self.hiScore.compare_score(self.value)

class HighScore(Label):
    """ Handle high score and display it on screen
        derivate from GameEngine Label"""
    
    def __init__(self,game,):
        Label.__init__(self,game,"emulogic.ttf",12)
        self.set_color((255,255,255))
        self.set_position((220,20))
        self.value=0
        self.modified=True
        
        self.register(game.get_sprites(),kFrontLayer)

    def update(self):
        if self.changed:
            self.set_text("%05d" % self.value)
        Label.update(self)

    def compare_score(self,v):
        if v>self.value:
            self.value=v
            self.changed=True

class SampleGame(FGame):
    """ the game main class """

    def __init__(self,fullScreen,width=kScreenWidth,height=kScreenHeight):
        FGame.__init__(self,fullScreen,width,height)

        self.showFPS=False
        self.fps=None
    
    def new_screen(self,name):
        self.mode=name
        
        if name=="menu":
            screen=MenuScreen(self,name)
        elif name=="option":
            screen=OptionScreen(self,name)
        elif name=="play":
            screen=PlayScreen(self,name)
        else:
            self.screen=None
            print "error, screen %s do not exist"  

    def update(self):
        self.fps.set_text("FPS: %.0f" % self.screen.clock.get_fps())
            
        FGame.update(self)
        
    def load_data(self):
        self.backImage=self.load_image("background.png")
        carFile=["car-1.png","car-2.png","car-3.png","car-4.png","car-5.png"]
        self.carImg=[]
        for f in carFile:
            self.carImg.append(self.load_image(f))
        riverFile=["turtle-1A.png","turtle-1B.png","turtle-1C.png","turtle-1D.png","turtle-1E.png","log-1.png","log-3.png","turtle-2A.png","turtle-2B.png","turtle-2C.png","turtle-2D.png","turtle-2E.png","log-2.png"]
        self.riverImg=[]
        for f in riverFile:
            self.riverImg.append(self.load_image(f))
        frogFile=["frog.png","frog-jump.png","frog-dead.png","frog-life.png"]
        self.frogImg=[]
        for f in frogFile:
            self.frogImg.append(self.load_image(f))
        bonusFile=["fly-home.png","crocodile-home.png"]
        self.bonusImg=[]
        for f in bonusFile:
            self.bonusImg.append(self.load_image(f))

class GenericMenuScreen(FScreen):
    """ base screen class for the game """
    
    def __init__(self,game,name,withCredits=False):
        FScreen.__init__(self,game,name)
        
        game.fps=game.get_widget('fps')
        game.fps.set_position(kMenuFPSLoc)
        game.get_widget('title')
        game.get_widget('subtitle')
        game.get_widget('copyright')

        self.allWidgets=[]            
        self.currentButton=None

        pygame.mouse.set_visible(1)

        
    def update(self):
        FScreen.update(self)
        
        for button in self.allWidgets:
            if button.interactive:
                if self.currentButton==button:
                    button.set_color((255,237,0))
                    button.set_background_color((151, 190, 13))
                else:
                    button.set_color((77,77,77))
                    button.set_background_color((204, 204, 204))
                    
    def do_events(self,event):
        FScreen.do_events(self,event)
        
        playMoveBeep=False
        playValidBeep=False
        # HandleKey events
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE: # quit the current screen (return to previous one)
                self.game.userChoice="quit"
                playValidBeep=True
                self.game.stop()
            elif event.key==K_DOWN or event.key==K_2: # down arrow : select next button
                if self.currentButton:
                    if self.currentButton.interactive:
                        index=self.allWidgets.index(self.currentButton)
                        index+=+1
                        if index>=len(self.allWidgets):
                            index=0
                        b=self.allWidgets[index]
                        while not b.interactive:
                            index+=1
                            if index>=len(self.allWidgets):
                                index=0
                            b=self.allWidgets[index]
                        self.currentButton=b
                        playMoveBeep=True
            elif event.key==K_UP or event.key==K_8:   # up arrow : select prevouis button      
                if self.currentButton:
                    if self.currentButton.interactive:
                        index=self.allWidgets.index(self.currentButton)
                        index-=1
                        if index<0:
                            index=len(self.allWidgets)-1
                        b=self.allWidgets[index]
                        while not b.interactive:
                            index-=1
                            if index<0:
                                index=len(self.allWidgets)-1
                            b=self.allWidgets[index]
                        self.currentButton=b
                        playMoveBeep=True
            elif event.key==K_RIGHT or event.key==K_6:    # right arrow : increment current option/button
                if self.currentButton:
                    if self.currentButton.type=='numscroller' or self.currentButton.type=='listscroller':
                        self.currentButton.do_increment()
                        playMoveBeep=True
            elif event.key==K_LEFT or event.key==K_4: # left arrow : decrement current option/button
                if self.currentButton:
                    if self.currentButton.type=='numscroller' or self.currentButton.type=='listscroller':
                        self.currentButton.do_decrement()
                        playMoveBeep=True
            elif event.key==K_RETURN:   # ENTER : active current button
                if self.currentButton:
                    self.game.userChoice=self.currentButton.action
                    playValidBeep=True
                    self.game.stop()
            else:   # any other key : handle the keyin special label, if any
                kList=self.get_objects("keyin")
                if (len(kList)>0):
                    for k in kList:
                        k.key(event.key)
                elif event.key==K_f:    # F : display frame-rate on screen
                    self.game.showFPS=not self.game.showFPS
                else:
                    print "no keyin object to handle this key"
                    
        #mouse handling
        if event.type==MOUSEBUTTONDOWN:
            for button in self.allWidgets:
                if button.interactive:
                    if button.rect.collidepoint(event.pos):
                        button.active = True
                        if self.currentButton!=button:
                            self.currentButton=button
                            playMoveBeep=True
        if event.type==MOUSEBUTTONUP:
            for button in self.allWidgets:
                if button.interactive and button==self.currentButton:
                    button.active=False
                    if button.rect.collidepoint(event.pos):
                        button.clicked = True
                        self.game.userChoice=button.action
                        playValidBeep=True
                        if button.type=="button":
                            self.game.stop()
                        # for scroller, check click position to do the scroll
                        if button.type=='numscroller' or button.type=='listscroller':
                            if event.pos[0]<button.rect.centerx-button.rect.width/6:
                                button.do_decrement()
                            if event.pos[0]>button.rect.centerx+button.rect.width/6:
                                button.do_increment()
                    
class MenuScreen(GenericMenuScreen):
    """ main menu screen """
    
    def __init__(self,game,name):
        GenericMenuScreen.__init__(self,game,name,True)

        # create buttons
        playButton=game.get_widget('bplay')
        optionButton=game.get_widget('boption')
        quitButton=game.get_widget('bmainquit')

        self.set_background(None)
        self.allWidgets=[playButton,optionButton,quitButton]            
        self.currentButton=playButton
                    
class OptionScreen(GenericMenuScreen):
    """ option screen """
    
    def __init__(self,game,name):
        GenericMenuScreen.__init__(self,game,name)
        
        # create buttons
        quitButton=game.get_widget('blowquit')

        self.set_background(None)
        self.allWidgets=[quitButton]            
        self.currentButton=quitButton
        
    def do_events(self,event):
        GenericMenuScreen.do_events(self,event)
                    
class PlayScreen(FScreen):
    """ play screen ; the game """
    
    def __init__(self,game,name):
        FScreen.__init__(self,game,name)
        
        # center the game view at the center of the computer screen
        self.set_offset(((kScreenWidth-kPlayWidth)/2,(kScreenHeight-kPlayHeight)/2),(kPlayWidth,kPlayHeight))
        self.set_background(game.backImage)
            
        self.frogLife=2
        self.gameOver=0
        self.dead=0
        self.level=0
        self.game.nextLevel=False
        self.nextLevelTime=0
        
        # sprites lists by genre
        self.game.cars=[]
        self.game.rivers=[]
        self.game.homeFrogged=[]
                
        #Create sprites            
        game.fps=game.get_widget('fps')
        game.fps.set_position(kPlayFPSLoc)
        game.get_widget('plabel')
        game.get_widget('hilabel')

        self.gameOverWidget=game.get_widget("gametext")        
        game.hiScore=HighScore(game)
        game.score=Score(game,game.hiScore)
                        
        self.time=FBarWidget(game)
        self.time.set_position(kPlayTimeLoc,"right")
        self.time.set_size(kPlayTimeSize)
        self.time.set_color((0,255,0))
        self.time.set_background_color((0,0,0))
        self.time.set_value(kPlayTimer)
        self.time.set_max_value(kPlayTimer)
        self.time.register(game.get_sprites(),kFrogLayer)
        
        self.bonusFly=FRandom(kFlyBonusRate,kFlyBonusDelay)
        self.bonusCrocodile=FRandom(kCrocodileBonusRate,kCrocodileBonusDelay)
        self.create_life()
        self.create_frog()

        self.new_level()
            
        self.allWidgets=[]            
        self.currentButton=None

        pygame.mouse.set_visible(0)
    
    def new_level(self):
        """ prepare for a new level """
        
        self.level+=1
        self.create_home()
        self.create_road()
        self.create_river()
        self.nextLevelTime=0
        self.game.nextLevel=0
        
    def create_frog(self):
        """ create the player itself """
        
        self.frog=Frog(self.game)

    def create_life(self):
        """ create life sprite : small frogger icons """
        
        self.life=[]
        for i in range(self.frogLife):
            self.life.append(LifeFrog(self.game))
        self.update_life(0)
            
    def update_life(self,value):
        """ update player's life when changed """
        
        self.frogLife+=value
        for i in self.life:
            i.kill()
        self.life=[]
        x=1
        for i in range(self.frogLife):
            l=LifeFrog(self.game)
            l.set_pos((x,kPlayYLife))
            x+=l.rect.width+3.0
            self.life.append(l)
        
    def create_home(self):
        """ create te frogger's home : the goal for the player """
        
        self.game.frogged=0
        for f in self.game.homeFrogged:
            if f!=None:
                f.kill()
        self.game.homeFrogged=[]
        self.game.homes=[]
        self.game.homeBonus=[]
        (x,y)=(kPlayXHome,kPlayYHome)
        (w,h)=(kPlayHomeWidth,kPLayHomeHeight)
        for i in range(5):
            self.game.homes.append(Rect((x,y),(w,h)))
            self.game.homeFrogged.append(None)
            self.game.homeBonus.append(0)
            x+=kPlayDXHome
            
    def create_road(self):
        """ create the road's sprites : cars """
        
        # 1st : kill them all
        for c in self.game.cars:
            c.kill()
        self.game.cars=[]
        
        # 2nd : create
        x=0.0
        y=kPlayYCar[0]
        for i in range(2):
            car=Car(self.game,0)
            car.set_speed((-0.010,0.0))
            car.set_pos((x,y))
            self.game.cars.append(car)
            x+=144.0
        x=20.0
        y=kPlayYCar[1]
        for i in range(3):
            car=Car(self.game,1)
            car.set_speed((0.011,0.0))
            car.set_pos((x,y))
            self.game.cars.append(car)
            x+=128.0
        x=40.0
        y=kPlayYCar[2]
        for i in range(3):
            car=Car(self.game,2)
            car.set_speed((-0.016,0.0))
            car.set_pos((x,y))
            self.game.cars.append(car)
            x+=128.0
        x=60.0
        y=kPlayYCar[3]
        for i in range(1):
            car=Car(self.game,3)
            car.set_speed((0.010,0.0))
            car.set_pos((x,y))
            self.game.cars.append(car)
            x+=128.0
        x=80.0
        y=kPlayYCar[4]
        for i in range(2):
            car=Car(self.game,4)
            car.set_speed((-0.035,0.0))
            car.set_pos((x,y))
            self.game.cars.append(car)
            x+=176.0

    def create_river(self):
        """ create the rivers sprites : logs and turtles """
        
        # 1st : kill them all
        for r in self.game.rivers:
            r.kill()
        self.game.rivers=[]
        
        # 2nd : create
        x=0.0
        y=kPlayYRiver[0]
        for i in range(4):
            river=Turtle(self.game,0)
            river.set_can_dive(i==0)
            river.set_speed((-0.035,0.0))
            river.set_pos((x,y))
            self.game.rivers.append(river)
            x+=128.0
        x=20.0
        y=kPlayYRiver[1]
        for i in range(3):
            river=Log(self.game,5)
            river.set_speed((0.035,0.0))
            river.set_pos((x,y))
            self.game.rivers.append(river)
            x+=192.0
        x=40.0
        y=kPlayYRiver[2]
        for i in range(2):
            river=Log(self.game,6)
            river.set_speed((-0.065,0.0))
            river.set_pos((x,y))
            self.game.rivers.append(river)
            x+=256.0
        x=60.0
        y=kPlayYRiver[3]
        for i in range(4):
            river=Turtle(self.game,7)
            river.set_can_dive(i==3)
            river.set_speed((0.034,0.0))
            river.set_pos((x,y))
            self.game.rivers.append(river)
            x+=112.0
        x=80.0
        y=kPlayYRiver[4]
        for i in range(3):
            river=Log(self.game,12)
            river.set_speed((-0.035,0.0))
            river.set_pos((x,y))
            self.game.rivers.append(river)
            x+=176.0

    def update(self):
        """ handle updates : text display, sprites interactions... """
        
        FScreen.update(self)
             
        #handle level
        if self.game.nextLevel:
            self.game.screen.gameOverWidget.set_text('TIME %d' % int(self.time.get_value()))
            self.nextLevelTime+=self.game.get_clock()
            if self.nextLevelTime>kNextLevelDuration:
                self.new_level()
        else:   #handle timer
            self.time.change_value(-0.001*self.game.get_clock())
            timeRemaining=self.time.get_value()
            if timeRemaining<=0.0:
                self.frog.hit(None)

        #handle home bonus
        if self.bonusFly.get_chance(self.game.get_clock()):
            index=int(5*random.random())
            if self.game.homeFrogged[index]==None:
                self.game.homeFrogged[index]=HomeFly(self.game,self.game.homes[index])
                print "fly at %d" % index
            else:
                print "fly at %d impossible" % index
        
        if self.bonusCrocodile.get_chance(self.game.get_clock()):
            index=int(5*random.random())
            if self.game.homeFrogged[index]==None:
                self.game.homeFrogged[index]=HomeCrocodile(self.game,self.game.homes[index])
                print ("crocodile at %d" % index)
            else:
                print ("crocodile at %d impossible" % index)
        
        #handle frog's death
        if not self.frog.alive():
            if self.dead==0:
                self.update_life(-1)
            self.dead+=self.game.get_clock()
            if self.dead>kKillDuration:
                self.dead=0
                if self.frogLife>=0:    # create a new frog ?
                    self.create_frog()
        if self.frogLife<0:
            self.game.screen.gameOverWidget.set_text('GAME OVER')
            self.gameOver+=self.game.get_clock()
            self.keepGoing=(self.gameOver<kGameOverDuration)

    def do_events(self,event):
        """ Handle events in game
            player keyboard or mouse are handled in Player class, for direct input """
            
        FScreen.do_events(self,event)
        
        if event.type==KEYDOWN:
            if event.key==K_LEFT or event.key==K_4:
                 self.frog.move_request((-1,0))
            if event.key==K_RIGHT or event.key==K_6:
                 self.frog.move_request((+1,0))
            if event.key==K_UP or event.key==K_8:
                 self.frog.move_request((0,-1))
            if event.key==K_DOWN or event.key==K_2:
                 self.frog.move_request((0,+1))
       
def main():
    print ("-- Sample FGame log --------------------------")
    
    # create the game container
    game=SampleGame(False)
    game.set_caption('FGame')
        
    # Read 'widget.ini' to build the widget tree
    game.dataPath="data"
    game.load_widgets('widget.ini')
    
    game.load_data()
    
    # do the game (menu and fork to other mode depending on user choice
    # mode : name of the current screen
    # userchoice : what's the user choic for the next screen (will became mode)
    terminate=False
    game.userChoice="menu"
    while not terminate:
        if game.userChoice=="menu":
            game.new_screen("menu")
            game.start()
        elif game.userChoice=="option":
            game.new_screen("option")
            game.start()
            game.userChoice="menu"
        elif game.userChoice=="play":
            game.new_screen("play")
            game.start()
            game.userChoice="menu"
        elif game.userChoice=="quit":
            terminate=True

    pygame.quit()

#this calls the 'main' function when this script is executed
if __name__ == '__main__': 
    main()
