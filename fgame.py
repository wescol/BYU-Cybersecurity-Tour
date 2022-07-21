#!/usr/bin/env python

"""
FGameEngine 1.0
Game Engine for pygame
    * sprite with float position (frame rate independant)
    * random (frame rate independant)
    * GUI with Screen handling, adaptation from GAMEENGINE 1.3 by Andy Harris, 2006

Build with :
    Python 2.5.2
    Pygame 1.8.1

Build with :
    Python 2.5.2
    Pygame 1.8.0
    py2app 0.4.2

See Source.rtf for licence and usage
"""

#Import Modules
import os, pygame, random
import time,sys
from pygame.locals import *
from configobj import *

kDefaultLanguage=0
kDefaultMaxFrameRate=0

kEffectLayer=90
kFrontLayer=99

if sys.platform=='darwin':
    import Carbon.File, Carbon.Folder, Carbon.Folders
    import MacOS

""" FGameEngine 1.0
    Pierre-Alain Dorange, 2008
"""

class FScreen():
    """
        FScreen class
        handle a screen related to a FGame instance
        to the main job, with the vent driven loop, see start()
        
        can handle a game screen and game menus (simple GUI)
    """
    
    def __init__(self, game, name):
        if game==None:
            print "No FGame instance defined, can't create screen"

        self.game=game
        self.game.screen=self
        self.name=name
        
        self.clock = pygame.time.Clock()
        self.gameClock=0
        
        # Prepare background (black)
        self.background=pygame.Surface(self.game.display.get_size())
        self.background.fill((0, 0, 0))
        self.game.display.blit(self.background, (0, 0))
        
        #sprites handle
        self.clear_sprites()
        
        #widgets handle
        self.currentButton=None
        self.userChoice=""
        self.clear_widgets()
        
        #set clipping region if necessary
        zone=(self.game.display.get_width(), self.game.display.get_height())
        self.set_offset((0, 0), zone)
        
    def set_offset(self, offset, zone):
        self.offset=offset
        self.activeZone=zone
        pygame.display.get_surface().set_clip((self.offset[0], self.offset[1]), (self.activeZone[0], self.activeZone[1]))
        
    def clear_sprites(self):
        #empty sprites group
        self.allSprites=pygame.sprite.LayeredUpdates()
        
    def clear_widgets(self):
        #empty widgets group
        self.allWidgets=[]
                
    def do_one_frame(self):
        self.gameClock=self.clock.tick(self.game.maxFrameRate)
            
        #update the game
        self.update()

        #prepare direct rects (what we need to update on screen)
        if self.refreshBackground:
            #full redraw
            self.show()
            self.refreshBackground=False
        else:
            #update only necessary part of the screen (thanks to LayeredUpdates)
            self.allSprites.clear(self.game.display, self.background)
            self.allSprites.update()
            dirtyrects=self.allSprites.draw(self.game.display)
            pygame.display.update(dirtyrects)
         
    def show(self):
        """ sets up the sprite groups
            begins the main loop and do a whole screen refresh
        """      
        self.game.display.blit(self.background, (0, 0))
        self.allSprites.clear(self.game.display, self.background)
        self.allSprites.update()
        self.allSprites.draw(self.game.display)
        
        pygame.display.flip()
        
    def show_dirty(self):
        self.allSprites.clear(self.game.display, self.background)
        self.allSprites.update()
        dirtyrects=self.allSprites.draw(self.game.display)
        pygame.display.update(dirtyrects)
        

    def do_events(self, event):
        """ overwrite this method to add your own events.
            works like normal event handling, passes event
            object
        """
        pass
        
    def update(self):
        """ happens once per frame, after event parsing.
            Overwrite to add your own code, esp event handling
            that doesn't require event obj. (pygame.key.get_pressed, 
            pygame.mouse.get_pos, etc)
            Also a great place for collision detection
        """
        pass

    def set_background(self, bckimg, coordinates=(0, 0)):
        if bckimg==None:
            self.background.fill((0, 0, 0))
        else:
            self.background.blit(bckimg, (coordinates[0]+self.offset[0], coordinates[1]+self.offset[1]))
        self.refreshBackground=True

    def get_objects(self, typeName):
        l=[]
        for o in self.allSprites:
            try:
                if o.type==typeName:
                    l.append(o)
            except:
                pass
        return l

    def get_object(self, name):
        l=[]
        for o in self.allSprites:
            try:
                if o.name==name:
                    return o
            except:
                pass
        return None
        
    def get_clock(self):
        return self.gameClock
            
    def get_sprites(self):
        return self.allSprites

    def stop(self):
        """stops the loop"""
        self.keepGoing=False
        self.abort=True
        pygame.display.get_surface().set_clip(None)

class FGame(object):
    """ 
        FGame is the main class for a game
        create and switch from FScreen to FScreen
        handle global data
    """
    
    def __init__(self, fullscreen, width, height):
        #Initialize Everything
        pygame.init()
        
        # Screen
        os.environ['SDL_VIDEO_CENTERED'] = '1'  #Center the windows
        self.display=pygame.display.set_mode((width, height))
        if (fullscreen):
            self.display=toggle_fullscreen()
            pygame.mouse.set_visible(0)
        else:
            pygame.mouse.set_visible(1)
        pygame.display.set_caption('fgame for pygame')
        
        self.width=width
        self.height=height
        self.screen=None
        self.pref=None
        self.maxFrameRate=kDefaultMaxFrameRate
        self.language=kDefaultLanguage
        self.dataPath=""
        self.imagePath=""
        self.soundPath=""
        self.fontPath=""
    
    def set_caption(self, title):
        """ set's the scene's title text """
        pygame.display.set_caption(title)
        
    def load_widgets(self, fileName):
        try:
            self.widgets=ConfigObj(make_path((self.dataPath,fileName)), file_error=True, raise_errors=True)
            
        except ParseError,e:
            print 'Loading Widget : ParseError\n\t%s' % e.message
        except IOError:
            print 'Loading Widget : IOError, file %s do not exist' % fileName
        except DuplicateError,e:
            print 'Loading Widget : DuplicateError, duplicate keyword\n\t%s' % e.message
        except KeyError,k:
            print 'Loading Widget : KeyError, key (%s) do not exist' % k
        except:
            print 'Loading Widget : error loading data'
            print sys.exc_info()
            raise
            
    def get_widget(self, name):
        if self.widgets==None:
            print "can't get_widget, call load_widgets first"
            return None
        
        try:
            section=self.widgets[name]
            
            type=section['type']
            
            if type=="String":
                english=section['english']
                french=section['french']
                german=section['german']
                
                string=String()
                string.set_text([english, french, german])
                
                return string
                
            elif type=="StringList":
                english=section['english']
                french=section['french']
                german=section['german']
                
                strings=StringList()
                strings.set_text([english, french, german])
                
                return strings
            
            elif type=="Label":
                try:
                    font=section['font']
                except:
                    font=None
                try:
                    fsize=section.as_int('fsize')
                except:
                    fsize=10
                try:
                    margin=section.as_intList('margin')
                except:
                    margin=(0,0)
                try:
                    color=section.as_intList('color')
                except:
                    color=Color('white')
                try:
                    size=section.as_intList('size')
                except:
                    size=(0,0)
                try:
                    text=section['text']
                except:
                    text='****'
                position=section.as_intList('position')
                
                label=Label(self, font, fsize)
                label.name=name
                label.fgColor=color
                label.set_position(position)
                label.set_margin(margin)
                label.set_text(text[self.language])
                label.register(self.screen.allSprites, kFrontLayer)
                
                return label
                
            elif type=="Button":
                try:
                    font=section['font']
                except:
                    font=None
                try:
                    fsize=section.as_int('fsize')
                except:
                    fsize=10
                try:
                    margin=section.as_intList('margin')
                except:
                    margin=(0,0)
                try:
                    color=section.as_intList('color')
                except:
                    color=Color('white')
                try:
                    text=section['text']
                except:
                    text='****'
                try:
                    bcolor=section.as_intList('bcolor')
                except:
                    bcolor=Color('black')
                try:
                    size=section.as_intList('size')
                except:
                    size=(0,0)
                try:
                    bmode=section['bmode']
                except:
                    bmode='background'
                position=section.as_intList('position')
                action=section['action']
                
                button=Button(self, font, fsize)
                button.name=name
                button.fgColor=color
                button.bgColor=bcolor
                button.set_position(position)
                button.set_margin(margin)
                button.set_size(size)
                button.set_background_mode(bmode)
                button.set_text(text[self.language])
                button.action=action
                button.register(self.screen.allSprites, kFrontLayer)
                
                return button
                
            elif type=="NumScroller":
                try:
                    font=section['font']
                except:
                    font=None
                try:
                    fsize=section.as_int('fsize')
                except:
                    fsize=10
                try:
                    margin=section.as_intList('margin')
                except:
                    margin=(0,0)
                try:
                    color=section.as_intList('color')
                except:
                    color=Color('white')
                try:
                    bcolor=section.as_intList('bcolor')
                except:
                    bcolor=Color('black')
                try:
                    size=section.as_intList('size')
                except:
                    size=(0,0)
                try:
                    bmode=section['bmode']
                except:
                    bmode='background'
                position=section.as_intList('position')
                value=section.as_floatList('value')
                format=section['format']
                action=section['action']
                
                nscroller=NumScroller(self, font, fsize)
                nscroller.name=name
                nscroller.fgColor=color
                nscroller.bgColor=bcolor
                nscroller.set_position(position)
                nscroller.set_margin(margin)
                nscroller.set_size(size)
                nscroller.set_background_mode(bmode)
                nscroller.set_format(format[self.language])
                nscroller.set_values(value[0], value[0], value[1])
                nscroller.action=action
                nscroller.register(self.screen.allSprites, kFrontLayer)
                
                return nscroller
                
            elif type=="ListScroller":
                try:
                    font=section['font']
                except:
                    font=None
                try:
                    fsize=section.as_int('fsize')
                except:
                    fsize=10
                try:
                    margin=section.as_intList('margin')
                except:
                    margin=(0,0)
                try:
                    color=section.as_intList('color')
                except:
                    color=Color('white')
                try:
                    bcolor=section.as_intList('bcolor')
                except:
                    bcolor=Color('black')
                try:
                    size=section.as_intList('size')
                except:
                    size=(0,0)
                try:
                    bmode=section['bmode']
                except:
                    bmode='background'
                position=section.as_intList('position')
                list=section['list']
                format=section['format']
                action=section['action']
                
                lscroller=ListScroller(self, font, fsize)
                lscroller.name=name
                lscroller.fgColor=color
                lscroller.bgColor=bcolor
                lscroller.set_position(position)
                lscroller.set_margin(margin)
                lscroller.set_size(size)
                lscroller.set_background_mode(bmode)
                lscroller.set_list(list)
                lscroller.set_format(format[self.language])
                lscroller.action=action
                lscroller.register(self.screen.allSprites, kFrontLayer)
                
                return lscroller
                
            elif type=="bar":
                try:
                    color=section.as_intList('color')
                except:
                    color=Color('white')
                try:
                    bcolor=section.as_intList('bcolor')
                except:
                    bcolor=Color('black')
                try:
                    size=section.as_intList('size')
                except:
                    size=(0,0)
                position=section.as_intList('position')
                values=section.as_floatList('values')

                bar=FBarWidget(self)
                bar.name=name
                bar.fgColor=color
                bar.bgColor=bcolor
                bar.set_position(position)
                bar.set_size(size)
                bar.set_value(values[0])
                bar.set_max_value(values[1])
                bar.register(self.screen.allSprites, kFrontLayer)
                
            else:
                print "unknow widget type (%s) for %s" % (type,name)
                return None
                
        except KeyError:
            print "unknow widget %s"% name
            return None
        
    def show(self):
        if self.screen==None:
            print "No screen defined for this game, can't display."
        self.screen.show()
        
    def show_dirty(self):
        self.screen.show_dirty()
        
    def start(self,audioVolume=1.0, musicVolume=1.0):
        if self.screen==None:
            print "No screen defined for this game, can't start."
            
        """ sets up the sprite groups
            begins the main loop
        """
        
        self.display.blit(self.screen.background, (0, 0))
        self.screen.refreshBackground=True
        
        self.screen.gameClock=self.screen.clock.tick(self.maxFrameRate)
        self.screen.keepGoing = True
        self.screen.pause=False
        self.screen.abort=False
        self.screen.audioVolume=audioVolume
        self.screen.musicVolume=musicVolume

        while self.screen.keepGoing:
            if self.screen.pause:  #handle pause
                self.screen.clock.tick(self.maxFrameRate)
                self.screen.gameClock=0
            else:   #handle standard clock
                self.screen.gameClock=self.screen.clock.tick(self.maxFrameRate)
            
            for event in pygame.event.get():    #handle basic events
                if event.type == pygame.QUIT:
                    self.stop()
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        self.stop()
                self.do_events(event)   #handle other events
            
            #update the game
            self.update()

            #prepare direct rects (what we need to update on screen)
            if self.screen.refreshBackground:
                #full redraw
                self.screen.show()
                self.screen.refreshBackground=False
            else:
                #update only necessary part of the screen (thanks to LayeredUpdates)
                self.screen.show_dirty()
                
    def stop(self):
        """stops the loop"""
        self.screen.stop()
                        
    def update(self):
        self.screen.update()

    def do_events(self, event):
        self.screen.do_events(event)
        
    def get_clock(self):
        return self.screen.gameClock
            
    def get_sprites(self):
        if self.screen==None:
            return None
        else:
            return self.screen.get_sprites()
            
    def load_image(self, name, colorkey=None, path=None):
        """ load and create an image from ressources """
        if path==None:
            path=self.imagePath
        fullname=make_path((self.dataPath, path, name))
        try:
            image = pygame.image.load(fullname)
            if image.get_alpha() is None:
                image = image.convert()
                if colorkey is not None:
                    if colorkey is -1:
                        colorkey = image.get_at((0, 0))
                    image.set_colorkey(colorkey, RLEACCEL)
            else:
                image = image.convert_alpha()
        except pygame.error, message:
            print 'Cannot load image:', fullname
            raise SystemExit, message
    
        return image
    
    def load_sound(self, name):
        """ load and create a sound from ressources """
        class NoneSound:
            def play(self):
                pass
            
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname=make_path((self.dataPath, self.soundPath,name))
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print 'Cannot load sound:', fullname
            raise SystemExit, message
        return sound
    
    def load_font(self, fontName='None', fontSize=10):
        """ load a TTF font """
        if fontName=='None' or fontName=='' or fontName==None:
            fontPath=None
        else:
            fontPath=make_path((self.dataPath, self.fontPath, fontName))
        font=None
        try:
            font=pygame.font.Font(fontPath, fontSize)
        except IOError,msg:
            print msg," :: ",fontPath
        except:    
            print "Unexpected error:", sys.exc_info()[0]
            raise
        return font

class FBasicSprite(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self) #call inherited pygame's Sprite initializer
        self.game=game
        self.type=""
        self.name=""
        self.group=[]
        self.image=None
        self.rect=Rect(0, 0, 0, 0)
        self._x=0.0
        self._y=0.0
        
    def register(self, group, layer=0):
        group.add(self, layer=layer)
        self.group.append(group)
        
    def unregister(self,group):
        group.remove(self)
        self.group.remove(group)
        
    def set_image(self, image):
        self.image=image
        self.rect=image.get_rect()
        self.rect.left=int(self._x+self.game.screen.offset[0]+0.5)
        self.rect.top=int(self._y+self.game.screen.offset[1]+0.5)

    def set_pos(self, pos):
        """ set float position : maintain a synchronous integer position for the rect 
            warning : setting a int position can cause bug at high frame rate, use wisely """
        self._x=float(pos[0])
        self._y=float(pos[1])
        self.rect.left=int(self._x+self.game.screen.offset[0]+0.5)
        self.rect.top=int(self._y+self.game.screen.offset[1]+0.5)
        
    def get_pos(self):
        return (self._x, self._y)
        
    def get_rect(self):
        return self.rect.move(-self.game.screen.offset[0], -self.game.screen.offset[1])
        
class FSprite(FBasicSprite):
    """ (based on pygame Sprite class)
        Handle Sprite with float position and frame rate
        Assure a constant speed with no fixed frame rate
        Frame rate is associate to Game : gameClock, express milliseconds for current frame

        Also handle the life, hit and death with explosions (see Explosion and SmallExplosion class)

        x,y : float position (top,left)
        damage : damage done when collide with something
        life : life point, killed when 0
        hitScore : when hit, add this to score
        killScore : when killed, add this to score
        explosionWhenHit : do the sprite explode when hit (small explosion)
        explosionWhenKilled : do the sprite explode when killed (big explosion)
        type : its model in string value
    """
    
    def __init__(self, game):
        FBasicSprite.__init__(self, game) #call inherited pygame's Sprite initializer
        self.type="sprite"
        self.name=""
        self.life=1.0
        self.lifeMax=1.0
        self.damage=0.0
        self._hitScore=0
        self._killScore=0
        self._scoreObject=None
        self._explosionWhenKilled=False
        self._killImages=None
        self._killSound=None
        self._killAnimRate=None
        self._killGroup=None
        self._explosionWhenHit=False
        self._hitImages=None
        self._hitSound=None
        self._hitAnimRate=None
        self._hitGroup=None
        
    def update(self):
        """ happens once per frame, after event parsing.
            Overwrite to add your own code, esp event handling
            that doesn't require event obj. (pygame.key.get_pressed, pygame.mouse.get_pos, etc)
            Also a great place for collision detection
        """
        pass

    def fmove(self, speedVector, clk):
        """ move the sprite with float parameter (dx,dy) and according to clock (clk)
            Frame-rate independant move """
        self._x+=float(speedVector[0]*clk)
        self._y+=float(speedVector[1]*clk)
        self.rect.left=int(self._x+self.game.screen.offset[0]+0.5)
        self.rect.top=int(self._y+self.game.screen.offset[1]+0.5)

    def pmove(self, vector):
        """ move the sprite with float parameter (dx,dy) with no clock synchronous
            Frame-rate dependant move """
        self._x+=vector[0]
        self._y+=vector[1]
        self.rect.left=int(self._x+self.game.screen.offset[0]+0.5)
        self.rect.top=int(self._y+self.game.screen.offset[1]+0.5)

    def fpmove(self, speedVector, clk, vector):
        """ move the sprite with float parameter (dx,dy) and according to clock (clk)
            + fixed offset
            a mix of dependant and indeppendant Frame-rate (for optimization) """
        self._x+=float(speedVector[0]*clk)+vector[0]
        self._y+=float(speedVector[1]*clk)+vector[1]
        self.rect.left=int(self._x+self.game.screen.offset[0]+0.5)
        self.rect.top=int(self._y+self.game.screen.offset[1]+0.5)
        
    def got_damage(self, value):
        self.life-=value
        if self.life>self.lifeMax:
            self.life=self.lifeMax

    def life_max(self):
        if self.life==self.lifeMax:
            return True
        else:
            return False

    def set_score(self, hit, kill, score=None):
        """ define scores parameter for the sprite :
                hit : score when hit
                kill : score hen killed
                score : value added to the score """
        self._hitScore=hit
        self._killScore=kill
        self._scoreObject=score
        
    def set_explosion_mode(self, explode=False, images=None, rate=None, sound=None):
        """ define the explosion behaviour for this sprite
                explode : True/False, explode or not when killed
                images : images list to animated the explosion
                rate : animation rate
                sound : sound when exploding """
        self._explosionWhenKilled=explode
        self._killImages=images
        self._killSound=sound
        self._killAnimRate=rate
        
    def set_hit_mode(self, explode=None, images=None, rate=None, sound=None):
        """ define the hit behaviour for this sprite
                hit : True/False, feedback when hit
                images : images list to animated the hit
                rate : animation rate
                sound : sound when exploding """
        self._explosionWhenHit=explode
        self._hitImages=images
        self._hitSound=sound
        self._hitAnimRate=rate
        
    def hit(self, sprite):
        """ when the sprite is hit by another sprite :
                adjust life according to the damage hit
                handle explosions, death and score
        """
        score=0
        if sprite==None:
            self.life=0.0
        else:
            self.got_damage(sprite.damage)
        if self.life<=0.0:  # if the sprite dead
            if self._explosionWhenKilled:
                explosion=FAnimatedSprite(self.game)
                explosion.set_images(self._killImages, self._killAnimRate)
                explosion.set_sound(self._killSound)
                explosion.register(self.game.get_sprites(), kEffectLayer)
                explosion.do_anim(self.rect)
            if self._killScore>0:
                score=self._killScore
            self.life=0.0
            self.kill()
        else:   # if the sprite is just hurt (or no-harm)
            if self._explosionWhenHit:
                explosion=FAnimatedSprite(self.game)
                explosion.set_images(self._hitImages, self._hitAnimRate)
                explosion.set_sound(self._hitSound)
                explosion.register(self.game.get_sprites(), kEffectLayer)
                explosion.do_anim(sprite.rect)
            if self._hitScore>0:
                score=self._hitScore
        if score>0: # adjust the game score (and show points) if necessary
            if self._scoreObject!=None:
                self._scoreObject.add_score(score)
        return score

class FSpriteWithSpeed(FSprite):
    """ FSprite with basic speed handling """
    def __init__(self, game):
        FSprite.__init__(self, game) #call Sprite initializer
        self.speed=(0.0,0.0)
        
    def update(self):
        if self.group.len()>0:
            self.move(self.speed,self.game.get_clock())
            
class FAnimatedSprite(FBasicSprite):
    """ Simple animated Sprite : 
        don't move, just be animated according to game speed (frame-rate independant) """
    
    def __init__(self, game):
        FBasicSprite.__init__(self, game) #call Sprite intializer
        self.animImage=0
        self.images=None
        self.image=None
        self.sound=None
        self.type="animated"

    def set_images(self, images, animRate):
        """ define the image list and the animation rate """
        self.animImage=0
        self.images=images
        FBasicSprite.set_image(self, get_from_list(self.images, self.animImage))
        self.animRate=animRate
        self.animClk=0.0
        self.animNext=self.animRate

    def set_sound(self, sound):
        self.sound=sound

    def do_anim(self, pos):
        """ just start the animation process """
        if self.sound!=None:
            self.sound.set_volume(self.game.screen.audioVolume)
            self.sound.play()
        if self.images!=None:
            self.rect.centerx=pos.centerx
            self.rect.centery=pos.centery
            self.register(self.game.get_sprites(), kEffectLayer)
        
    def update(self):
        self.animClk+=self.game.get_clock()
        if self.animClk>self.animNext:
            self.animImage+=1
            self.animNext+=self.animRate
        if self.animImage>=len(self.images):    # if animation done, kill ourself
            self.kill()
        else:
            self.image=get_from_list(self.images,self.animImage)
            
class String():
    def __init__(self):
        self.type="String"
        self.name=""
        self.string=[]
        
    def set_text(self, strings):
        self.string=strings
        
    def get_text(self, lang):
        if lang<len(self.string):
            return self.string[lang]
        else:
            return self.string[-1]
            
class StringList():
    def __init__(self):
        self.type="StringList"
        self.name=""
        self.string=[]
        
    def set_text(self, strings):
        self.string=strings
        
    def get_text(self, lang):
        if lang<len(self.string):
            return self.string[lang]
        else:
            return self.string[-1]

class BasicLabel(FBasicSprite):
    """ a basic label for label and multi-label classes
        properties: 
            font: font to use
            text: text to display
            fgColor: foreground color
            bgColor: background color
            lox,locy: position of label's center
            width,height: (width, height) of label
            marginx,marginy : margin over text when width,height not specified
    """
    
    def __init__(self, game, fontName="None", fontSize=20):
        FBasicSprite.__init__(self, game)
        self.font = game.load_font(fontName, fontSize)
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.locx=0
        self.locy=0
        self.posMode="left"
        self.width=0
        self.height=0
        self.marginx=0
        self.marginy=0
        self.backmode="nobackground"
        self.area=pygame.display.get_surface().get_rect()
        self.changed=True
        self.interactive=False
        self.action=""

    def set_color(self, color):
        if self.fgColor!=color:
            self.fgColor=color
            self.changed=True

    def set_background_color(self, color):
        if self.bgColor!=color:
            self.bgColor=color
            self.backmode="background"
            self.changed=True

    def set_background_mode(self, mode):
        if self.backmode!=mode:
            self.backmode=mode
            self.changed=True

    def set_position(self, location, mode="left"):
        self.locx=int(location[0]+self.game.screen.offset[0])
        self.locy=int(location[1]+self.game.screen.offset[1])
        self.rect=Rect((self.locx, self.locy), (self.width, self.height))
        self.posMode=mode
        self.changed=True

    def set_size(self,size=(0,0)):
        self.width=size[0]
        self.height=size[1]
        self.rect=Rect((self.locx, self.locy), (self.width, self.height))
        self.changed=True

    def set_margin(self,margin=(0,0)):
        self.marginx=margin[0]
        self.marginy=margin[1]
        self.changed=True

class FBarWidget(BasicLabel):
    def __init__(self, game):
        BasicLabel.__init__(self, game)
        self.image=None
        self.rect=None
        self._value=0
        self._maxValue=0
        self.type="bar"
    
    def set_value(self, value):
        self._value=value
        self.changed=True
        
    def change_value(self, value):
        self._value+=value
        if self._value>self._maxValue:
            self._value;self._maxValue
        self.changed=True
        
    def get_value(self):
        return self._value

    def set_max_value(self, value):
        self._maxValue=value
        self.changed=True

    def set_size(self, size):
        self.image=pygame.Surface((size[0], size[1]))
        BasicLabel.set_size(self, size)
        
    def update(self):
        if self.changed:
            value=self._value*self.image.get_width()/self._maxValue
            self.image.fill(self.bgColor)
            if self.posMode=="left":
                self.image.fill(self.fgColor, (0, 0, value, self.image.get_height()))
            else:
                self.image.fill(self.fgColor, (self.image.get_width()-value, 0, self.image.get_width(), self.image.get_height()))
            self.changed=False

class Label(BasicLabel):
    """ a basic label 
        properties: 
            text: text to display
    """
    
    def __init__(self, game, fontName="None", fontSize=20):
        BasicLabel.__init__(self, game, fontName, fontSize)
        self.text = ""
        self.changed=True
        self.type="label"

    def set_text(self, text):
        if self.text!=text:
            self.text=text
            self.changed=True

    def get_text(self):
       return self.text
            
    def set_text_from_widget(self, name):
        if self.game==None:
            print "widget %s has no game linked", self.name
            return
        try:
            section=self.game.widgets[name]
            text=section['text']
            self.set_text(text[self.game.language])
        except:    
            print "Unexpected error:", sys.exc_info()[0]
            raise

    def update(self):
        if self.changed:
            if self.backmode=="nobackground":   # no background : simply render font in the image
                self.image=self.font.render(self.text, True, self.fgColor)
            else:   # background : render font in a surface then in the image
                s=self.font.size(self.text)
                if self.width==0:  #auto dimension if necessary
                    width=s[0]+2*self.marginx
                else:
                    width=self.width
                if self.height==0:  #auto dimension if necessary
                    height=s[1]+2*self.marginy
                else:
                    height=self.height
                self.image = pygame.Surface((width, height))
                self.image.fill(self.bgColor)
                fontSurface=self.font.render(self.text, True, self.fgColor, self.bgColor)
                self.image.blit(fontSurface, ((self.image.get_width()-fontSurface.get_width())/2, (self.image.get_height()-fontSurface.get_height())/2))
            #adjust block position on screen
            self.rect=self.image.get_rect()
            if self.posMode=="left":
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.left=self.locx
            elif self.posMode=="right":
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.right=self.locx
            else:   # center align
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.centerx=self.locx
            self.rect.centery=self.locy
            self.changed=False

class KeyIn(Label):
    """ KeyIn class :
        handle user feedback to enter a string (ie. name when got a best score 
        Very basic, need to be enhanced
    """
        
    def __init__(self, game, fontName="None", fontSize=20):
        Label.__init__(self, game, fontName, fontSize)
        self.blinkRate=300
        self.blinkClock=0
        self.blinkState=True
        self.keyInText=""
        self.beforeText=""
        self.afterText=""
        self.text=""
        self.type="keyin"

    def set_keytext(self, text):
        self.keyInText=text

    def set_aftertext(self, text):
        self.afterText=text

    def key(self, k):
        if k==K_BACKSPACE:  #backspace : erase lasr character
            self.keyInText=self.keyInText[:-1]
        else:
            if k in range(128): #add new character if valid
                self.keyInText+=chr(k)

    def get_keytext(self):
        return self.keyInText

    def update(self):
        self.blinkClock+=self.game.get_clock()
        if self.blinkClock>self.blinkRate:
            self.blinkState=not self.blinkState
            self.blinkClock=0
            self.changed=True

        if self.changed:
            if self.blinkState:
                t=self.beforeText+self.keyInText+"_"+self.afterText
            else:
                t=self.beforeText+self.keyInText+" "+self.afterText
            Label.set_text(self,t)
        Label.update(self)

class Button(Label):
    """ a button based on the label 
        same properties as label +
        active: True if user is clicking on sprite
                False if user is not currently clicking
        clicked: True when user releases mouse over a 
                 currently active button
    """

    def __init__(self, game, fontName="None", fontSize=20):
        Label.__init__(self, game, fontName, fontSize)
        self.active=False
        self.clicked=False
        self.bgColor=(0xCC, 0xCC, 0xCC)
        self.interactive=True
        self.type="button"
    
    def update(self):
        self.clicked = False
        Label.update(self)

class NumScroller(Button):
    """ like a button, but has a numeric value that 
        can be decremented by clicking on left half
        and incremented by clicking on right half.
        new atributes:
            value: the scroller's numeric value
            minValue: minimum value
            maxValue: maximum value
            increment: How much is added or subtracted
            format: format of string interpolation
    """
    
    def __init__(self, game, fontName="None", fontSize=20):
        Button.__init__(self, game, fontName, fontSize)
        self.set_values(0.0, 50.0, 100.0)
        self.format="<<  %.2f  >>"
        self.interactive=True
        self.type="numscroller"
        
    def update(self):
        self.text= self.format % self.value
        Button.update(self)

    def set_values(self, minValue, value, maxValue, inc=0.0):
        self.minValue=minValue
        self.value=value
        self.maxValue=maxValue
        if inc==0.0:
            self.increment = (self.maxValue-self.minValue)/10.0
        else:
            self.increment = inc
        self.changed=True

    def set_value(self, value):
        self.value=value
        self.changed=True

    def set_format(self, format):
        if self.format!=format:
            self.format=format
            self.changed=True
            
    def set_format_from_widget(self, name):
        if self.game==None:
            print "widget %s has no game",self.name
            return
        section=self.game.widgets[name]
        format=section['format']
        self.set_format(format[self.game.language])

    def do_increment(self):
        self.value += self.increment
        if self.value > self.maxValue:
            self.value = self.maxValue
        self.changed=True

    def do_decrement(self):
        self.value -= self.increment
        if self.value < self.minValue:
            self.value = self.minValue
        self.changed=True

class ListScroller(Button):
    """ like a button, but has a str list value that 
        can be decremented by clicking on left half
        and incremented by clicking on right half.
        new atributes:
            value: the scroller's numeric value (index value)
            list: string list
            format: format of string interpolation
    """
    
    def __init__(self, game, fontName="None", fontSize=20):
        Button.__init__(self, game, fontName, fontSize)
        self.list=[]
        self.format="<<  %s  >>"
        self.value=0
        self.interactive=True
        self.type="listscroller"
        
    def update(self):
        self.text=self.format % self.list[self.value]
        Button.update(self)

    def set_list(self,alist):
        self.list=alist
        self.changed=True

    def set_format(self, format):
        self.format=format
        self.changed=True
            
    def set_format_from_widget(self, name):
        if self.game==None:
            print "widget %s has no game", self.name
            return
        section=self.game.widgets[name]
        format=section['format']
        self.set_format(format[self.game.language])

    def set_value(self, value):
        if type(value) is bool:
            if value:
                self.value=1
            else:
                self.value=0
        else:
            self.value=value
        if self.value<0:
            self.value=len(self.list)-1
        if self.value>=len(self.list):
            self.value=0
        self.changed=True

    def do_increment(self):
        self.value+=1
        if self.value>=len(self.list):
            self.value=0
        self.changed=True

    def do_decrement(self):
        self.value-=1
        if self.value<0:
            self.value=len(self.list)-1
        self.changed=True

class MultiLabel(BasicLabel):
    """ a multi-lines label (for text)
        properties: 
            textLines: list of text to display
    """
        
    def __init__(self, game, fontName="None", fontSize=20):
        BasicLabel.__init__(self, game, fontName, fontSize)
        self.textLines=[]
        self.lineHeight=0
        self.type="multilabel"

    def set_text_lines(self, texts):
        if self.textLines!=texts:
            self.textLines=texts
            self.changed=True

    def set_line_height(self, height):
        self.lineHeight=height
        
    def update(self):
        if self.changed:
            if self.backmode=="nobackground":   # no background : simply render font in the image
                self.image=self.font.render(self.textLines, True, self.fgColor)
            else:   # background : render font in a surface then in the image
                width=0
                height=0  
                for l in self.textLines:
                    s=self.font.size(l)
                    if s[0]>width:
                        width=s[0]
                    if self.lineHeight==0:
                        height+=s[1]+2
                    else:
                        height+=self.lineHeight
                if self.width==0:  #auto dimension if necessary
                    width+=2*self.marginx
                else:
                    width=self.width+2*self.marginx
                if self.height==0:  #auto dimension if necessary
                    height+=2*self.marginy
                else:
                    height=self.height+2*self.marginy
                self.image=pygame.Surface((width, height))
                self.image.fill(self.bgColor)
                y=self.marginy
                for l in self.textLines:
                    s=self.font.size(l)
                    fontSurface=self.font.render(l, True, self.fgColor, self.bgColor)
                    if self.posMode=="left":
                        x=self.marginx
                    elif self.posMode=="right":
                        x=self.image.get_width()-s[0]-self.marginx
                    else:
                        x=(self.image.get_width()-s[0])/2
                    self.image.blit(fontSurface, (x, y))
                    if self.lineHeight==0:
                        y+=s[1]+2
                    else:
                        y+=self.lineHeight
                    
            #adjust block position on screen
            self.rect=self.image.get_rect()
            if self.posMode=="left":
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.left=self.locx
            elif self.posMode=="right":
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.right=self.locx
            else:        
                if self.locx==0:
                    self.rect.centerx=self.area.width/2
                else:
                    self.rect.centerx=self.locx
            self.rect.centery=self.locy
            self.changed=False
        
class FRandom():
    """ Random class
        used to handle random according to frame rate """
    
    def __init__(self, rate, minDelay=0):
        """ init the random with a rate and a minimum delay
            rate (seconds) : chance=1/rate per seconds
            mindelay (seconds) : time between two chance """
        self.rate=rate          
        self.mindelay=minDelay  
        self.previous=0.0

    def set_rate(self, rate, minDelay=0):
        self.rate=rate          
        self.mindelay=minDelay          

    def get_chance(self, clk):
        """ throw the dice :  get a random according to parameters
            clk parameter is game clock (milliseconds) """
        if not self.mindelay==0:
            now=time.time()
            if now-self.previous<self.mindelay:
                return False

        b=random.random()<0.001*clk/self.rate
        if not self.mindelay==0 and b:
            self.previous=now

        return b

def toggle_fullscreen():
    """ Toggle to fullscreen from pygame CookBook """
    screen=pygame.display.get_surface()
    tmp=screen.convert()
    caption=pygame.display.get_caption()
    cursor=pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
    w=screen.get_width()
    h=screen.get_height()
    flags=screen.get_flags()
    bits=screen.get_bitsize()
    
    pygame.display.quit() 
    pygame.display.init()
   
    screen=pygame.display.set_mode((w, h), flags^FULLSCREEN, bits)
    screen.blit(tmp, (0, 0))
    pygame.display.set_caption(*caption)
 
    pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
    pygame.mouse.set_cursor(*cursor)  # Duoas 16-04-2007
    
    return screen
    
def make_path(items):
    """ make a path to file with the list of folders """
    path=''
    for i in items:
        path=os.path.join(path, i)
    return path

def get_from_list(list, index=0):
    """ get an item from a list, if index greater than size, return the last one """
    if index>=len(list):
        return list[-1]
    else:
        return list[index]

def version_translate(versionStr):
    """ convert a version string (ie 1.0, 2.0.1, 2.0a4, 1.4b2) into 
        a sortable string, so python can easy compare 2 versions """
        
    resultStr=""
    for c in versionStr:
        if c=="a":
            resultStr+='#'
        elif c=="b":
            resultStr+='$'
        elif c=="f":
            resultStr+='%'
        elif c in ['.','0','1','2','3','4','5','6','7','8','9']:
            resultStr+=c
    completion='.'
    for i in range(len(resultStr), 10):
        resultStr+=completion
        if completion=='.':
            completion='0'
        else:
            completion='.'
        
    return resultStr
    
def version_compare(v1, v2):
    """ Compare 2 versions using version_translate() """
    v1t=version_translate(v1)
    v2t=version_translate(v2)
    if v1t>v2t:
        return +1
    elif v1t<v2t:
        return -1
    else:
        return 0
        
def sign(x):
    if x>0:
        return +1.0
    elif x<0:
        return -1.0
    else:
        return 0.0
