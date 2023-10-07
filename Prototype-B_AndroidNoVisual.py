#Same as Prototype-A but run in android for receiving feedback
#Use swipe and tap because it wouldn't be that hard
#Monotone color for good contrast
#Resolution of 1080x2220 full screen both horizontal and vertical

from random import shuffle, randint #Use to shuffle the characters for players and randomize a theme
from math import sqrt
from time import time #Use to detect the different to the time some function run
from kivy.app import App #Use to operate the app overall
from kivy.lang import Builder #Use to import .kv file for GUI works
from kivy.uix.widget import Widget #Use to create and control widgets
from kivy.uix.image import Image #Use to create images
from kivy.graphics import Color, Rectangle #Customization for canvases
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen #Use to define screens related modules for .kv file to play with
from kivy.uix.screenmanager import FadeTransition as Fade #Import screen switching transitions
from kivy.uix.screenmanager import NoTransition as No #Import screen switching transitions
from kivy.uix.screenmanager import SlideTransition as Slide #Import screen switching transitions
from kivy.core.window import Window #Use to resize to specific resolution
from kivy.utils import platform #Use to detect the platform
from kivy.clock import Clock #Use to delay functions
from kivy.properties import StringProperty, ListProperty, NumericProperty #Use to stay update with the datas
import ctypes #Use to mimic the home button's behavior

#GUI elements
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scatterlayout import ScatterLayout #Use to rotate widgets for landscape display
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

#test window size to real phone resolution
Window.size = (1080/4,2220/4) if platform != 'android' else Window.size

def deep_copy(original_list): #Use to copy nested lists
    if isinstance(original_list, list):
        return [deep_copy(item) for item in original_list]
    else:
        return original_list

def spin_wheel(pl): #Use to return randomized characters to players
    players_list = deep_copy(pl)
    copied_character_list = [x[1] for x in players_list] #Create a new list contains character names

    attempt = 1
    max_attempts = 500 #Set max attempts trying to shuffle the names
    while True: #Keep shuffling until it meets requirement
        if attempt >= max_attempts or [False for j in range(len(players_list))] == [players_list[k][1] == copied_character_list[k] for k in range(len(players_list))]:
            break #If reaches max_attempts then break the loop
            #Else if every names are mismatched from the original, then break the loop
        shuffle(copied_character_list) #Shuffle the order of the list
        attempt += 1 #Count the attempts
    for i in range(len(players_list)): #Set the shuffled names to the original lists
        players_list[i][1] = copied_character_list[i]
        
    
    return players_list #Return the list back to the funcion caller

def size_to(x,y,object=Window): #Use to calculate the size in ratio of any widget(object)
    return (object.width*x,object.height*y)

def land_size_to(x,y,object=Window): #Landscape version
    return (object.height*x,object.width*y)

def pos_to(x,y,size,object=Window): #Use to calculate the pos in ratio of any widget(object)
    if object != Window:
        return ((object.x)-size[0]/2-(object.size[0]*(0.5-x)),(object.y)-size[1]/2+(object.size[1]*(0.5-y)))
    else:
        return ((object.width/2)-size[0]/2-(object.width*(0.5-x)),(object.height/2)-size[1]/2+(object.height*(0.5-y)))

def land_pos_to(x,y,size,object=Window): #Landscape version
    if object != Window:
        return ((-object.x)-size[1]/2-(object.size[1]*(0.5-x)),(Window.width/2+object.y)-size[0]/2+(object.size[0]*(0.5-y)))
    else:
        return ((object.width/2)-size[0]/2-(object.height*(0.5-x)),(object.height/2)-size[1]/2+(object.width*(0.5-y)))



class menu_screen(Screen):
    pass #pass because we've already inherited the attributes from Screen module

class howtoplay_screen(Screen):
    pass #pass because we've already inherited the attributes from Screen module

class gameinit_screen(Screen):
    pass #pass because we've already inherited the attributes from Screen module

class screen_manager(ScreenManager): #define a screen manager to be call
    pass #pass because we've already inherited the attributes from ScreenManager module



Builder.load_file("Prototype-B_AndroidNoVisual.kv") #Import .kv file for a design



sm = screen_manager() #Call the manager prior, Making sure it will use the same manager
default_timer = 60 #Set global countdown timer
swipe_threshold = 300 #Set the global swipe threashold for easier management
compliments = ["Good job!","Nice guess!","Impressive!","Congratulation!","Wowie!","Perfectly done!"] #When a player won the game
cheer_ups = ["Better luck next time!","You did your best!","You've tried so hard","That was so close!","So far so good!","That was hard!"] #When a player failed the game



class mainApp(App): #A class with attributes to operate the app overall
    theme = StringProperty() #StringProperty use to be an updating text variables
    player_list = ListProperty() #StringProperty use to be an updating list variables
    timer = NumericProperty(default_timer) #Set up the timer

    def reset(self): #Getting the app ready
        self.enable_return = True #Enable tapping return button
        self.default_theme = ["Wild animals", "Anime", "Famous Thais", "Our friends"][randint(0,3)] #Get a random theme
        self.theme = self.default_theme #Initial the theme as the default theme
        self.enable_ans = False #Initial the "Anonymous names suggestion"
        self.player_screen = [] #Use to contain the screens to insert names and characters for each player
        self.player_list = [] #Reset players' datas
        self.current_timer_label = None
        sm.screen_history = ["menu"] #Setup the list for screens history
        sm.clear_widgets() #Clear the screens out
        sm.add_widget(menu_screen()) #Add the screen to the ScreenManager
        sm.add_widget(howtoplay_screen())
        sm.add_widget(gameinit_screen())
        sm.current = "menu"
        sm.transition = Fade(duration=0.2)

    def build(self): #Build up the GUI
        self.title = "Who Am I" #Set the title of the app
        Window.bind(on_keyboard=self.navigation_bar)
        self.reset() #Setup necessary values to the default values

        sm.bind(current_screen=self.check_screen) #Define the event listener when the screen change
        return sm

    def minimize(self): #mimic the home button's behavior
        if platform == 'android':
            try:
                #For Android, Use ctypes to call the X11 window manager to minimize the window
                root_window = self._app_window
                window_id = root_window.get_native_window()
                xlib = ctypes.cdll.LoadLibrary("libX11.so.6") #Call the library
                atom = xlib.XInternAtom(xlib.XOpenDisplay(0), "_NET_ACTIVE_WINDOW", 0)
                xlib.XChangeProperty(xlib.XOpenDisplay(0), window_id, atom, xlib.XA_WINDOW, 32, 
                                     ctypes.c_prop_mode_replace, ctypes.pointer(ctypes.c_ulong(0)), 1) #Change something, ready to close
                xlib.XCloseDisplay(xlib.XOpenDisplay(0)) #Close the window
            except Exception as err:
                print(f"Error minimizing app: {err}") #Can't minimize the app
        else:
            #For other platforms, simply exit the app
            self.stop()

    def navigation_bar(self,window,key,*args):
        if key == 27 and self.enable_return: #27 refer to back button in android and enable to tap return button
            sm.transition = Fade(duration=0.2) #Select the transition
            if sm.current[:6] != "player":
                sm.current = sm.screen_history[-2] if len(sm.screen_history) > 1 else self.minimize() #If it isn't a menu, then go back
            else:
                sm.current = sm.current[:6]+str(int(sm.current[6:])-1) if int(sm.current[6:])-1 > 0 else sm.screen_history[-2]
            return True #return True for stopping the propagation

    def check_screen(self,manager,screen,*args):
        lastest = sm.screen_history[-2] if len(sm.screen_history) > 1 else "menu" #Check the lastest screen visited

        if screen == None: #This case only happen when the app is stopped
            return True #Break the function when the app is closed but still fire the event
        
        if lastest == screen.name: #Went back to previous screen
            sm.screen_history.remove(sm.screen_history[-1]) #Step backward in the history
        else: #Went to a new screen
            sm.screen_history.append(screen.name) #Put more history screen

        #Additional processes
        if screen.name == "gameinit":
            for screen_name in self.player_screen: #Clear the screen from screen manager
                sm.remove_widget(sm.get_screen(screen_name))
            self.player_screen = [] #Reset the list whenever go back or just reached out this screen
            self.player_list = []

        if screen.name[:6] == "player": #Switched to any player init screen
            if not screen.ids.next.disabled and not screen.ids.start.disabled: #If it isn't already disable (prevent too many blindfold layers)
                #screen.ids.player_name_input.disabled = True #Disable the TextInput
                #screen.ids.character_name_input.disabled = True #Disable the TextInput
                screen.ids.next.disabled = True #Disable the real button
                screen.ids.start.disabled = True #Disable the real button
                screen.ids.player_name_input.disabled = True #Disable the input
                screen.ids.character_name_input.disabled = True #Disable the input

                #Create the blindfold canvas and button
                layout = BoxLayout(orientation='vertical',
                                vertical_align='top',
                                size_hint=(None,None),
                                size=(Window.width,Window.height))
                with layout.canvas.before:
                    Color(0.14,0.14,0.14,1)
                    Rectangle(pos=layout.pos,size=layout.size)
                screen.add_widget(layout) #Add the layout to the screen

                player_name_lbl = Label(text=screen.name.capitalize()[:6]+" "+screen.name[6:],
                                        size_hint=(None, None),
                                        size=(Window.width*0.4, Window.height*0.05),
                                        pos_hint={"center_x":0.5,"center_y":1-0.4},
                                        text_size=(layout.width, None),
                                        font_size=Window.height*0.05,
                                        bold=True,
                                        valign="middle",
                                        halign="center"
                                        )
                screen.add_widget(player_name_lbl) #Add the layout to the screen

                btn_layout_1 = BoxLayout(orientation='vertical',
                                         vertical_align='top',
                                         size_hint=(None,None),
                                         size=(Window.width*0.6,Window.height*0.1),
                                         pos_hint={"center_x":0.5,"center_y":1-0.5}
                                         )
                screen.add_widget(btn_layout_1)

                edit_button = Button(text="Begin Editing",
                                     size_hint=(None, None),
                                     size=(Window.width*0.55, Window.height*0.08),
                                     pos_hint={"center_x":0.5},
                                     font_size=Window.height*0.04,
                                     valign="middle",
                                     halign="center",
                                     color=(0.14,0.14,0.14,1),
                                     background_color=(0.93,0.93,0.93,1),
                                     background_normal=""
                                     )
                btn_layout_1.add_widget(edit_button)

                btn_layout_2 = BoxLayout(orientation='horizontal',
                                         size_hint=(None,None),
                                         size=(Window.width*0.5+Window.height*0.01,Window.height*0.1), #Add spacing
                                         pos_hint={"center_x":0.5,"center_y":1-0.6},
                                         spacing=Window.height*0.01
                                )
                screen.add_widget(btn_layout_2)
                
                next_button = Button(text="Next",
                                    size_hint=(None, None),
                                    size=(Window.width*0.25, Window.height*0.08),
                                    font_size=Window.height*0.036,
                                    valign="middle",
                                    halign="center",
                                    color=(0.14,0.14,0.14,1),
                                    background_color=(0.93,0.93,0.93,1),
                                    background_normal="")
                btn_layout_2.add_widget(next_button)

                start_button = Button(text="Start",
                                    size_hint=(None, None),
                                    size=(Window.width*0.25, Window.height*0.08),
                                    font_size=Window.height*0.036,
                                    valign="middle",
                                    halign="center",
                                    color=(0.14,0.14,0.14,1),
                                    background_color=(0.93,0.93,0.93,1),
                                    background_normal="")
                btn_layout_2.add_widget(start_button)

                screen.add_widget(self.get_return_button()) #Put return button on the top layer

                #Bind functions to the buttons
                def begin_edit(instance):
                    screen.remove_widget(layout)
                    screen.remove_widget(player_name_lbl)
                    screen.remove_widget(btn_layout_1)
                    screen.remove_widget(btn_layout_2)
                    screen.ids.player_name_input.disabled = False #Enable the TextInput
                    screen.ids.character_name_input.disabled = False #Enable the TextInput
                    screen.ids.next.disabled = False #Enable the real button
                    screen.ids.start.disabled = False #Enable the real button
                edit_button.bind(on_release=begin_edit)

                next_button.bind(on_release=lambda x: self.change_player_screen(int(screen.name[6:])))
                
                start_button.disabled = False if len(self.player_screen) > 1 else True #Only enable when there are atleast 1 player
                try:
                    next_button.disabled = False if self.player_screen[int(screen.name[6:])] else True #Only enable when next player is existed
                except:
                    next_button.disabled = True #When index is out of range

                start_button.bind(on_release=self.on_game_start)

    def start_timer(self,lbl,callback_fnct):
        self.timer = default_timer #Reset the time
        self.current_timer_label = lbl
        Animation.cancel_all(self)  #Stop any current animations
        self.anim = Animation(timer=0, duration=self.timer)
        self.anim.bind(on_complete=callback_fnct)
        self.anim.start(self)

    def on_timer(self, instance, value): #Fire when 'timer' value changed
        try: #There's an error detecting the label
            self.current_timer_label.text = str(round(value,1))
        except:
            self.timer = default_timer #Reset the timer

    def show_scorelines(self, result_list):
        score_screen = Screen(name="scorelines")
        sm.add_widget(score_screen)
        sm.transition = Fade(duration=0.2)
        sm.current = score_screen.name
        score_screen.size_hint = (None, None)
        score_screen.size = Window.size
        score_screen.pos = (0, 0)
        with score_screen.canvas.before:
            Color(0.082, 0.082, 0.082, 1)
            Rectangle(pos=score_screen.pos, size=score_screen.size)

        #Rotate widgets with ScatterLayout
        screen_layout = ScatterLayout(do_rotation=False,
                                     do_scale=False,
                                     do_translation=False,
                                     rotation=270,
                                     pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                     size_hint=(None, None),
                                     size=Window.size
                                     )
        score_screen.add_widget(screen_layout)

        screen_layout.add_widget(Label(text=f"Scorelines",
                                       size_hint=(None, None),
                                       size=land_size_to(1,0.2),
                                       pos=land_pos_to(0.5,0.11,land_size_to(1,0.2)),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.048,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )

        border_layout = BoxLayout(orientation='vertical',
                                   vertical_align='top',
                                   size_hint=(None, None),
                                   size=land_size_to(0.874, 0.593),
                                   pos=land_pos_to(0.5, 0.464, land_size_to(0.874, 0.593))
                                   )
        with border_layout.canvas.before:
            Color(0.93, 0.93, 0.93, 1)
            Rectangle(pos=border_layout.pos, size=border_layout.size)
        screen_layout.add_widget(border_layout)

        header_layout = BoxLayout(orientation='horizontal',
                                   size_hint=(None, None),
                                   size=size_to(1, 0.1, border_layout),
                                   pos=land_pos_to(0.5, 0.05, land_size_to(1, 0.1, border_layout))
                                   )
        border_layout.add_widget(header_layout)

        header_layout.add_widget(Label(text="Players",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )
        
        header_layout.add_widget(Label(text="Characters",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )
        
        header_layout.add_widget(Label(text="Character by",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )
        
        header_layout.add_widget(Label(text="Results",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )
        
        header_layout.add_widget(Label(text="Attempts left",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )
        
        header_layout.add_widget(Label(text="Time used",
                                       size_hint=(None, None),
                                       size=size_to(1/6,1,header_layout),
                                       text_size=(score_screen.width, None),
                                       font_size=Window.height*0.021,
                                       bold=True,
                                       color=(0,0,0,1),
                                       valign="middle",
                                       halign="center"
                                       )
                                 )

        scroll = ScrollView(size_hint=(None, None),
                            size=size_to(1, 0.9, border_layout)
                            )
        border_layout.add_widget(scroll)

        grid = GridLayout(cols=6,
                          spacing=border_layout.height*0.02,
                          size_hint=(None, None),
                          size=size_to(1, 0.1*len(result_list), scroll)
                          )
        
        scroll.add_widget(grid)
        #Add datas to the scroll view
        for player_data in result_list:
            for data in player_data:
                grid.add_widget(Label(text="-" if player_data.index(data) == 2 and self.enable_ans else "Failed" if data == "fail" else "Won" if data == "win" else "Time out" if data == "timeout" else str(data),
                                     size_hint_y=None,
                                     height=size_to(1,0.1,border_layout)[1],
                                     text_size=(grid.width, None),
                                     font_size=Window.height*0.021,
                                     color=(0.082,0.082,0.082,1),
                                     valign="middle",
                                     halign="center"
                                      )
                                )

        ok_button = Button(text="Ok",
                          size_hint=(None, None),
                          size=land_size_to(0.167, 0.158),
                          pos=land_pos_to(0.5, 0.872, land_size_to(0.167, 0.158)),
                          font_size=Window.height*0.04,
                          valign="middle",
                          halign="center",
                          color=(0,0,0,1),
                          background_color=(0.93,0.93,0.93,1),
                          background_normal="")
        screen_layout.add_widget(ok_button)
        ok_button.bind(on_release=lambda x: self.reset())

    def on_game_start(self,instance):
        if (sm.get_screen(self.player_screen[-1]).ids.player_name_input.text != "" and sm.get_screen(self.player_screen[-1]).ids.character_name_input.text != "") or len(self.player_list) > 1:
            self.enable_return = False #Disable return buttons while in game
            #Save change for the last screen
            self.player_list[-1][0] = sm.get_screen(self.player_screen[-1]).ids.player_name_input.text
            self.player_list[-1][1] = sm.get_screen(self.player_screen[-1]).ids.character_name_input.text
            for player_data in self.player_list: #Clear the blank player
                if player_data[0] == "" or player_data[1] == "":
                    self.player_list.remove(player_data)

            ## MAIN GAME SYSTEM ##
            playing_player_list = spin_wheel(self.player_list)
            def next_player(index): #Call from the button
                player_data = playing_player_list[index]
                p_name = player_data[0]
                p_char = player_data[1]
                p_screen = Screen(name=p_name)
                sm.add_widget(p_screen)
                sm.transition = Slide(duration=0.2,direction='left')
                sm.current = p_screen.name
                p_screen.size_hint = (None, None)
                p_screen.size = Window.size
                p_screen.pos = (0,0)
                with p_screen.canvas.before:
                    Color(0.082,0.082,0.082,1)
                    Rectangle(pos=p_screen.pos,size=p_screen.size)

                #Rotate widgets with ScatterLayout
                screen_layout = ScatterLayout(do_rotation=False,
                                             do_scale=False,
                                             do_translation=False,
                                             rotation=270,
                                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             size_hint=(None, None),
                                             size=Window.size
                                       )
                p_screen.add_widget(screen_layout)


                layout = BoxLayout(orientation='vertical',
                                   vertical_align='top',
                                   size_hint=(None, None),
                                   size=land_size_to(1,0.9),
                                   pos=pos_to(0.5,0.5,land_size_to(1,0.9)),
                                   spacing=p_screen.height*0.139*0.05
                                   )
                screen_layout.add_widget(layout)

                layout.add_widget(Label(text="", #Space filler
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,layout),
                                       pos_hint={"center_x":0.5},
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.05,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )

                layout.add_widget(Label(text="It's",
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,layout),
                                       pos_hint={"center_x":0.5},
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.05,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                
                layout.add_widget(Label(text=f"> {p_name} <",
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,layout),
                                       pos_hint={"center_x":0.5},
                                       text_size=(None, None), #Put None on the width will make it single=line
                                       font_size=Window.height*0.054,
                                       bold=True,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                
                layout.add_widget(Label(text="Turn",
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,layout),
                                       pos_hint={"center_x":0.5},
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.05,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                
                layout.add_widget(Label(text="Put device on your head, Tap the screen when ready.",
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,layout),
                                       pos_hint={"center_x":0.5},
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.032,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )

                def start_game(instance, touch): #After tap the screen
                    if instance.collide_point(*touch.pos):
                        instance.unbind(on_touch_down=start_game) #Prevent overlaping between function
                        screen_layout.remove_widget(layout) #Remove the previous display
                        
                        self.life_list = []
                        for i in range(3): #3 max attempts to answer
                            life = Image(source="assets/cross_disabled.png",
                                        allow_stretch=True,
                                        keep_ratio=True,
                                        size_hint=(None, None),
                                        size=land_size_to(0.095,0.193),
                                        pos=land_pos_to(0.867,0.217+i*(0.5-0.217),land_size_to(0.095,0.193),screen_layout),
                                        )
                            self.life_list.append(life)
                            screen_layout.add_widget(life)

                        screen_layout.add_widget(Label(text=f"{p_name} is",
                                       size_hint=(None, None),
                                       size=land_size_to(1,0.2),
                                       pos=land_pos_to(0.5,0.217,land_size_to(1,0.2)),
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.05,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                        
                        character_box = BoxLayout(orientation='vertical',
                                                 vertical_align='top',
                                                 size_hint=(None, None),
                                                 size=land_size_to(0.449,0.247),
                                                 pos=land_pos_to(0.5,0.5,land_size_to(0.449,0.247))
                                                 )
                        with character_box.canvas.before:
                            Color(0,0,0,1)
                            Rectangle(pos=character_box.pos,size=character_box.size)
                        screen_layout.add_widget(character_box)

                        character_box.add_widget(Label(text=f"{p_char}",
                                       size_hint=(None, None),
                                       size=size_to(1,1,character_box),
                                       pos=land_pos_to(0.5,0.5,size_to(1,1,character_box)),
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.054,
                                       bold=True,
                                       valign="middle",
                                       halign="center"
                                       )
                                       )
                        
                        screen_layout.add_widget(Label(text="CORRECT : SWIPE",
                                       size_hint=(None, None),
                                       size=land_size_to(1,0.15),
                                       pos=land_pos_to(0.5,0.75,land_size_to(1,0.15)),
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.032,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                        
                        screen_layout.add_widget(Label(text="WRONG : TAP",
                                       size_hint=(None, None),
                                       size=land_size_to(1,0.15),
                                       pos=land_pos_to(0.5,0.85,land_size_to(1,0.15)),
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.032,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )

                        timer_label = Label(text=str(round(self.timer)),
                                       size_hint=(None, None),
                                       size=land_size_to(0.2,0.3),
                                       pos=land_pos_to(0.138,0.5,land_size_to(0.2,0.3)),
                                       text_size=(layout.width, None),
                                       font_size=Window.height*0.072,
                                       valign="middle",
                                       halign="center"
                                       )
                        screen_layout.add_widget(timer_label)

                        ###########################MAIN FINALIZER
                        def finish_game(result):
                            #Unbind to prevent bouncing
                            p_screen.unbind(on_touch_move=swipe_screen)
                            p_screen.unbind(on_touch_down=down_screen)
                            p_screen.unbind(on_touch_up=up_screen)
                            #Stop the timer
                            Animation.cancel_all(self)
                            result_layout = BoxLayout(orientation='vertical',
                                   vertical_align='top',
                                   size_hint=(None, None),
                                   size=land_size_to(1,1),
                                   pos=pos_to(0.5,0.5,land_size_to(1,1))
                                   )
                            with result_layout.canvas.before:
                                #Use green if won, else red
                                color = Color(0,0.72,0,1) if result == "win" else Color(0.75,0,0,1)
                                Rectangle(pos=result_layout.pos,size=result_layout.size)
                            screen_layout.add_widget(result_layout)

                            result_layout.add_widget(Label(text=compliments[randint(0,len(compliments)-1)] if result == "win" else cheer_ups[randint(0,len(cheer_ups)-1)],
                                       size_hint=(None, None),
                                       size=size_to(1,0.4,result_layout),
                                       pos=land_pos_to(0.5,0.5,size_to(1,0.4,result_layout)),
                                       text_size=(result_layout.width, None),
                                       font_size=Window.height*0.078,
                                       bold=True,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )

                            result_layout.add_widget(Label(text=f"You were \" {p_char} \"" if result != "timeout" else f"Time's out and you were \" {p_char} \"" ,
                                       size_hint=(None, None),
                                       size=size_to(1,0.2,result_layout),
                                       pos=land_pos_to(0.5,0.5,size_to(1,0.2,result_layout)),
                                       text_size=(result_layout.width, None),
                                       font_size=Window.height*0.048,
                                       valign="middle",
                                       halign="center"
                                       )
                                  )
                            
                            result_layout.add_widget(Label(text="", #Space filler
                                       size_hint=(None, None),
                                       size=size_to(1,0.1,result_layout)
                                       )
                                  )

                            #Set the result, life(s) left, and time used back to player list
                            owner = [o[0] for o in self.player_list if o[1] == p_char][0] #Find who suggested the character
                            playing_player_list[index] = [p_name,p_char,owner,result,len([life for life in self.life_list if life.source == "assets/cross_disabled.png"]),round(default_timer-self.timer,1)]
                        
                            if index >= len(playing_player_list)-1:
                                Clock.schedule_once(lambda x: self.show_scorelines(playing_player_list), 4) #Delay 4 seconds before the end
                            else:
                                Clock.schedule_once(lambda x: next_player(index+1), 4) #Delay 4 seconds before next player

                        self.start_timer(timer_label,lambda x,y: finish_game("timeout")) #Using x,y because it says it need 2 positional arguments

                        def swipe_screen(instance, touch): #Detecting if there's any touch
                            if sqrt(touch.dx**2 + touch.dy**2) >= swipe_threshold: #If the touch move more than the threshold
                                #Swipe
                                finish_game("win")

                        self.distance = () #Setting up the variable to contain values
                        self.dt = 0 #Set up the variable to check the different of time
                        def down_screen(instance, touch):
                            self.dt = time()
                            self.distance = touch.pos #Record the position for a comparison


                        def up_screen(instance, touch):
                            try: #In case it didn't update the value
                                self.dt = time() - self.dt #Final time - Initial time
                                self.distance = sqrt((touch.pos[0]-self.distance[0])**2 + (touch.pos[1]-self.distance[1])**2)
                                if self.distance <= 10 and self.dt <= 0.5: #Didn't move too far and stay too long
                                    for l in range(len(self.life_list)):
                                        life = self.life_list[l]
                                        if life.source == "assets/cross_disabled.png" and l < len(self.life_list)-1:
                                            life.source = "assets/cross_enabled.png"
                                            break
                                        elif life.source == "assets/cross_disabled.png":
                                            life.source = "assets/cross_enabled.png"
                                            finish_game("fail")

                                self.distance = 0 #Reset the distance
                                self.dt = 0 #reset the different of time
                            except:
                                pass

                        p_screen.bind(on_touch_move=swipe_screen)
                        p_screen.bind(on_touch_down=down_screen)
                        p_screen.bind(on_touch_up=up_screen)

                p_screen.bind(on_touch_down=start_game)

            next_player(0) #Start from first player

    def on_game_init(self, selected_theme, ans_status, *args):
        self.enable_ans = ans_status
        self.theme = selected_theme if selected_theme != "" else self.default_theme #Set the StringProperty value to be shown on the label
        self.change_player_screen(0) #Enter player initialize phase

    def get_return_button(self,*args):
        return_button = Button(text="<",
                               size_hint=(None, None),
                               size=(Window.height*0.05, Window.height*0.05),
                               pos_hint={"center_x":(1-0.943)+(0.05/2),"center_y":1-(0.125)+(0.139/4)},
                               font_size=Window.height*0.06,
                               valign="middle",
                               halign="center",
                               color=(0.14,0.14,0.14,1),
                               background_color=(0.93,0.93,0.93,1),
                               background_normal="")
        def return_back(instance): #Only use to bind to on_release event
            sm.transition = Fade(duration=0.2)
            if sm.current[:6] != "player":
                sm.current = sm.screen_history[-2]
            else:
                sm.current = sm.current[:6]+str(int(sm.current[6:])-1) if int(sm.current[6:])-1 > 0 else sm.screen_history[-2]
            
        return_button.bind(on_release=return_back)
        return return_button

    def create_player_screen(self,*args):
        index = len(self.player_screen) #No need to +1
        self.player_list.append(["",""]) #Append datas to be customized
        i_screen = Screen(name=f"player{index+1}") #Create the screen class with name
        sm.add_widget(i_screen) #Add to screen manager
        self.player_screen.append(i_screen.name) #Add to player screen list for operation
        with i_screen.canvas.before:
            Color(0.082,0.082,0.082,1)
            Rectangle(pos=pos_to(0.5,0.5,Window.size),size=Window.size)

        layout_header = BoxLayout(orientation='vertical',
                                  size_hint=(None,None),
                                  size=size_to(0.943,0.139),
                                  #pos=((Window.width/2)*(1-0.943),(Window.height/2)*(1-0.139)+(Window.height*(0.5-0.125)))
                                  pos=pos_to(0.5,0.125,size_to(0.943,0.139))
                                  )
        with layout_header.canvas.before:
            Color(0.93,0.93,0.93,1)
            Rectangle(pos=layout_header.pos,size=layout_header.size)
        i_screen.add_widget(layout_header)

        layout_header.add_widget(Label(text=f"Player {index+1}",
                                       font_size=Window.height*0.06,
                                       color=(0,0,0,1),
                                       bold=True
                                       )
                                )
        layout_header.add_widget(Label(text="", #Space filler
                                       size_hint=(None, None),
                                       size=size_to(1,0.05,layout_header)
                                       )
                                )


        layout_player_name = BoxLayout(orientation='vertical',
                                       vertical_align='top',
                                       size_hint=(None,None),
                                       size=size_to(0.73,0.139),
                                       pos=pos_to(0.5,0.3,size_to(0.73,0.139)),
                                       spacing=i_screen.height*0.139*0.05
                                       )
        with layout_player_name.canvas.before:
            Color(0.929,0.929,0.929,1)
            Rectangle(pos=layout_player_name.pos,size=layout_player_name.size)
        i_screen.add_widget(layout_player_name)

        player_name_head = Label(text="\"YOUR\" name",
                                 text_size=(layout_player_name.width*1, None),
                                 font_size=Window.height*0.04,
                                 color=(0.14,0.14,0.14,1),
                                 size_hint=(None, None),
                                 size=(layout_player_name.width*1, layout_player_name.height*0.4),
                                 valign="middle",
                                 halign="center"
                                 )
        layout_player_name.add_widget(player_name_head)

        player_name_inp = TextInput(input_type='text',
                                    multiline=False, #Disable multiline
                                    hint_text="NOT character name", #Placeholder text
                                    input_filter=None, #Character limit set to none
                                    write_tab=False, #Stop focus when pressing Enter or tapping outside
                                    use_bubble=True, #Enable text manipulation
                                    valign="middle", #Align the text to the middle, Vertically
                                    halign="center", #Align the text to the center, Horizontally
                                    size_hint=(None, None),
                                    size=(layout_player_name.width*0.9, layout_player_name.height*0.4),
                                    pos_hint={"center_x":0.5},
                                    font_size=Window.height*0.032,
                                    foreground_color=(1,1,1,1),
                                    background_color=(0,0,0,1)
                                    )
        layout_player_name.add_widget(player_name_inp)

        layout_player_name.add_widget(Label(text="", #Space filler
                                            size_hint=(None, None),
                                            size=(layout_player_name.width*1, layout_player_name.height*0.1)
                                            )
                                      )

        i_screen.ids.player_name_input = player_name_inp
        

        layout_character_name = BoxLayout(orientation='vertical',
                                       vertical_align='top',
                                       size_hint=(None,None),
                                       size=(Window.width*0.73,Window.height*0.198),
                                       pos=((Window.width/2)*(1-0.73),(Window.height/2)*(1-0.198)+(Window.height*(0.5-0.503))),
                                       spacing=i_screen.height*0.139*0.05
                                       )
        with layout_character_name.canvas.before:
            Color(0.929,0.929,0.929,1)
            Rectangle(pos=layout_character_name.pos,size=layout_character_name.size)
        i_screen.add_widget(layout_character_name)

        character_name_head = Label(text="\"CHARACTER\" name",
                                 text_size=(layout_character_name.width*1, None),
                                 font_size=Window.height*0.036,
                                 color=(0.14,0.14,0.14,1),
                                 size_hint=(None, None),
                                 size=(layout_character_name.width*1, layout_character_name.height*0.28),
                                 valign="middle",
                                 halign="center"
                                 )
        layout_character_name.add_widget(character_name_head)

        character_name_theme = Label(text=f"Theme : {self.theme}",
                                 text_size=(layout_character_name.width*1, None),
                                 font_size=Window.height*0.028,
                                 color=(0.14,0.14,0.14,1),
                                 size_hint=(None, None),
                                 size=(layout_character_name.width*1, layout_character_name.height*0.22),
                                 valign="middle",
                                 halign="center"
                                 )
        layout_character_name.add_widget(character_name_theme)

        layout_character_name.add_widget(Label(text="", #Space filler
                                            size_hint=(None, None),
                                            size=(layout_character_name.width*1, layout_character_name.height*0.03)
                                            )
                                      )

        character_name_inp = TextInput(input_type='text',
                                    multiline=False, #Disable multiline
                                    hint_text="Regard the theme", #Placeholder text
                                    input_filter=None, #Character limit set to none
                                    write_tab=False, #Stop focus when pressing Enter or tapping outside
                                    use_bubble=True, #Enable text manipulation
                                    valign="middle", #Align the text to the middle, Vertically
                                    halign="center", #Align the text to the center, Horizontally
                                    size_hint=(None, None),
                                    size=(layout_character_name.width*0.9, layout_character_name.height*0.31),
                                    pos_hint={"center_x":0.5},
                                    font_size=Window.height*0.032,
                                    foreground_color=(1,1,1,1),
                                    background_color=(0,0,0,1)
                                    )
        layout_character_name.add_widget(character_name_inp)
        i_screen.ids.character_name_input = character_name_inp

        layout_character_name.add_widget(Label(text="", #Space filler
                                            size_hint=(None, None),
                                            size=(layout_character_name.width*1, layout_character_name.height*0.06)
                                            )
                                      )


        btn_layout = BoxLayout(orientation='horizontal',
                                size_hint=(None,None),
                                size=((Window.width*0.278*2)+Window.height*0.05,Window.height*0.075), #Add spacing
                                pos_hint={"center_x":0.5,"center_y":1-0.691},
                                spacing=Window.height*0.05)
        i_screen.add_widget(btn_layout)
                
        next_button = Button(text="Next",
                                    size_hint=(None, None),
                                    size=(Window.width*0.278, Window.height*0.075),
                                    font_size=Window.height*0.040,
                                    valign="middle",
                                    halign="center",
                                    color=(0.14,0.14,0.14,1),
                                    background_color=(0.93,0.93,0.93,1),
                                    background_normal="")
        btn_layout.add_widget(next_button)

        start_button = Button(text="Start",
                                    size_hint=(None, None),
                                    size=(Window.width*0.278, Window.height*0.075),
                                    font_size=Window.height*0.040,
                                    valign="middle",
                                    halign="center",
                                    color=(0.14,0.14,0.14,1),
                                    background_color=(0.93,0.93,0.93,1),
                                    background_normal="")
        btn_layout.add_widget(start_button)

        next_button.bind(on_release=lambda x: self.change_player_screen(index+1)) #change the screen when hit
        i_screen.ids.next = next_button

        start_button.bind(on_release=self.on_game_start)
        i_screen.ids.start = start_button

        return i_screen #return the screen back to append it to the screen manager

    def change_player_screen(self,index,*args): #Customize specific player by indexes in player_screen
        sm.transition = No() #Select the transition
        try: #Try finding the screen first. If not found, then create new screen (Just in case they went back to edit their data and went back)
            current_screen = self.player_screen[index]
            sm.current = current_screen
        except: #Else if index is out of range
            if index > 0:
                previous_screen = self.player_screen[index-1]
                #Check if the player has inserted the data yet
                if sm.get_screen(previous_screen).ids.player_name_input.text != "" and sm.get_screen(previous_screen).ids.character_name_input.text != "":
                    new_screen = self.create_player_screen()
                    sm.current = new_screen.name
            else: #If it's the first player, skip checking
                new_screen = self.create_player_screen()
                sm.current = new_screen.name

        if index > 0:
            #Try save changes for previous player
            previous_screen = self.player_screen[index-1]
            self.player_list[index-1][0] = sm.get_screen(previous_screen).ids.player_name_input.text
            self.player_list[index-1][1] = sm.get_screen(previous_screen).ids.character_name_input.text



if __name__ == "__main__": #If the main file is running then
    root = mainApp()
    root.run() #Run the App class