#!/usr/bin/python3
"""Programm zum steuern einer  LED-Beleuchtung.

Die LED-Stripes sind in 3 getrennte Bereiche aufgeteilt.
Gesteuert wird die Beleuchtung der Bar über einen Raspberry Pi 3+.
Wir verwenden ein Touch-Display für die Ein- und Ausgabe.

Dies ist ein Gemeinschaftsprojekt des Jugendclub Grünberg.
Stand 22.05.2022 / Programmversion 2.0"""

import tkinter as tk

# breite und höhe des Displays in Pixeln
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT = 320
# Abstand der Elemente zueinander und zum Rand
DISTANCE = 8
# breite und höhe für Buttons, Labels und co.
WIDTH = (DISPLAY_WIDTH - DISTANCE) // 8
HEIGHT = DISPLAY_HEIGHT // 10
# Hintergrundfarbe
BG_COLOR = "#000000"
# Schriftfarbe
FG_COLOR = "#00FF00"

font_list = ("Times 15 bold", "Times 13","Times 48 bold", "Times 32")
color_list = ['#FF0000' , '#FFFF00' , '#FF8000' , '#FF0080' ,
                    '#00FF00' , '#00FFFF' , '#00FF80' , '#80FF00' ,
                    '#0000FF' , '#FF00FF' , '#0080FF' , '#8000FF' ,
                    '#FFFFFF', '#000000']
# color_list: [0]=rot, [4]=grün, [8]=blau, [12]=weiß, [13]=schwarz
history_list = [0]


class main_win():
    """Hauptbereich mit den Steuerelementen.
    
    Hier wird das TK-window erstellt,
    - zwischen den einzelnen Fenstern gewechselt
    - Vollbildmodus an/aus geschaltet
    - die Kopfzeile eingefügt"""
    
    def __init__(self):
        self.window = tk.Tk()                                           # Hauptfenster erstellen
        self.window.attributes('-fullscreen', True)     #Vollbildmodus
        self.fullScreenState = True
        self.window.bind("<F11>",self.toggleFullScreen)
        self.window.bind("<Escape>",self.toggleFullScreen)
        self._frame = None
        self.head_frame()
        self.switch_frame(frame_main)
        self.window.mainloop()
        
    def toggleFullScreen(self,  event):                     # Vollbild an/aus schalten
        self.fullScreenState = not self.fullScreenState
        self.window.attributes("-fullscreen", self.fullScreenState)
        
    def switch_frame(self,  Frame_Class):               # Seite wechseln
        New_Frame = Frame_Class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = New_Frame
        self._frame.place(x = 0, 
                                     y = HEIGHT + 2 * DISTANCE,
                                     width = DISPLAY_WIDTH,
                                     height = DISPLAY_HEIGHT - HEIGHT - 2 * DISTANCE)

    def head_frame(self):                                       # Kopfzeile mit Überschrift, Zurück-Button und Einstellungs-Button
        tk.Frame(bg = BG_COLOR
                        ).place(width = DISPLAY_WIDTH,
                                    height = HEIGHT + 2 * DISTANCE)
        tk.Label(bg = BG_COLOR,
                    fg = FG_COLOR,
                    font = font_list[0],
                    text = "Bar Jugendclub Grünberg"
                    ).place(x = DISTANCE,
                                y = DISTANCE,
                                width = DISPLAY_WIDTH - 2 * DISTANCE,
                                height = HEIGHT + DISTANCE)
        tk.Button(bg = "#000000",
                        fg = "#FF0000",
                        font = font_list[0],
                        text = "<-",
                        command = lambda: self.back_but()
                        ).place(x = DISPLAY_WIDTH - WIDTH - DISTANCE,
                                    y = DISTANCE,
                                    width = WIDTH,
                                    height = HEIGHT + DISTANCE)
        tk.Button(bg = BG_COLOR,
                        fg = FG_COLOR,
                        borderwidth = 0,
                        highlightthickness = 0,
                        relief = "flat",
                        command = lambda: self.switch_frame(frame_config)
                        ).place(x = 0,
                                    y = 0,
                                    width = HEIGHT,
                                    height = HEIGHT)

    def back_but(self):                                     # eine Seite zurück springen
        if history_list[-1] > 0:
            history_list.pop()
            Back = history_list[len(history_list)-1]
            if Back == 0:
                self.switch_frame(frame_main)
            elif Back == 1:
                self.switch_frame(frame_select_color)
            elif Back == 2:
                self.switch_frame(frame_select_area)
            elif Back == 3:
                self.switch_frame(frame_select_mode)
            elif Back == 4:
                self.switch_frame(frame_set_color)
            elif Back == 5:
                self.switch_frame(frame_set_flash)
            #elif Back == 6:
            #	self.switch_frame(frame_set_switch)


class frame_main(tk.Frame):
    """Startseite/Hauptfenster.
    
    Auf dieser Seite kann der Nutzer auswählen:
    - ob er alles in einer Farbe haben möchte,
    - nur einzelne Bereiche ändern will oder
    - die Farbe wechseln/blinken lassen will"""

    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        tk.Label(self,
                      text = "Beleuchtungssteuerung",
                      font = font_list[1],
                      bg = BG_COLOR,
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                  y = DISTANCE,
                                  width = DISPLAY_WIDTH - 2 * DISTANCE,
                                  height = HEIGHT)
        tk.Button(self,
                        text = "Einfarbig",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_color)
                        ).place(x = DISTANCE,
                                    y = HEIGHT + 2 *DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self,
                        text = "Mehrfarbig",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_area)
                        ).place(x = DISTANCE,
                                    y = 3 * HEIGHT + 3 * DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self,
                        text = "Farbwechsel",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_mode)
                        ).place(x = DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * DISTANCE,
                                    height = 2 * HEIGHT)
		

class led_color_control():
    """Hier entsteht die Steuerung der LED's.
    
    In diesem Bereich werden die LED's angesteuert"""
    
    x=1


class frame_select_color(tk.Frame):
    """Farbwahlfenster.
   
  Hier kann man voreingestellte farben auszuwählen"""
  
    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 1:
            history_list.append(1)
        tk.Label(self,
                      text = "Farbe wählen",
                      font = font_list[1],
                      bg = BG_COLOR,
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                   y = DISTANCE,
                                   width = DISPLAY_WIDTH - 2 * DISTANCE,
                                   height = HEIGHT)
        for i, Color in enumerate(color_list):
            column, row = divmod(i, 4)
            tk.Button(bg = Color
                            ).place(x = row * 2 * WIDTH + DISTANCE,
                                        y = (column) * (2 * HEIGHT - DISTANCE) + 2 * HEIGHT + 4 * DISTANCE ,
                                        width = 2 * WIDTH - DISTANCE,
                                        height = 2 * HEIGHT - 2 * DISTANCE)
        tk.Button(text = "individuell",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_set_color)
                        ).place(x = 4 * WIDTH +  DISTANCE,
                                    y = 3 * (2 * HEIGHT - DISTANCE) + 2 * HEIGHT + 4 * DISTANCE,
                                    width = 4 * WIDTH - DISTANCE,
                                    height = 2 * HEIGHT - 2 * DISTANCE)


class frame_select_area(tk.Frame):
    """Bereichwahlfenster.
   
   um einen oder mehrere Bereiche auszuwählen"""

    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 2:
            history_list.append(2)
        c1 = tk.IntVar()
        c2 = tk.IntVar()
        c3 = tk.IntVar()
        tk.Label(self,
                      text = "Bereich wählen",
                      font = font_list[1],
                      bg = BG_COLOR,
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                   y = DISTANCE,
                                   width = DISPLAY_WIDTH - 2 * DISTANCE,
                                   height = HEIGHT)
        tk.Checkbutton(self,
                                 text = "Schrank",
                                 font = font_list[1],
                                 bg = BG_COLOR,
                                 fg = FG_COLOR,
                                 selectcolor = BG_COLOR,
                                 anchor = "w",
                                 variable = c1
                                 ).place(x = DISTANCE,
                                             y = HEIGHT + 2 * DISTANCE,
                                             width = 6 * WIDTH - 2 * DISTANCE,
                                             height = 2 * HEIGHT)
        tk.Checkbutton(self,
                                  text = "Bar oben",
                                  font = font_list[1],
                                  bg = BG_COLOR,
                                  fg = FG_COLOR,
                                  selectcolor = BG_COLOR,
                                  anchor = "w",
                                  variable = c2
                                  ).place(x = DISTANCE,
                                              y = 3 * HEIGHT + 3 * DISTANCE,
                                              width = 6 * WIDTH - 2 * DISTANCE,
                                              height = 2 * HEIGHT)
        tk.Checkbutton(self,
                                  text = "Bar unten",
                                  font = font_list[1],
                                  bg = BG_COLOR,
                                  fg = FG_COLOR,
                                  selectcolor = BG_COLOR,
                                  anchor = "w",
                                  variable = c3
                                  ).place(x = DISTANCE,
                                              y = 5 * HEIGHT + 4 * DISTANCE,
                                              width = 6 * WIDTH - 2 * DISTANCE,
                                              height = 2 * HEIGHT)

        def forward():
            if c1.get() + c2.get() + c3.get() == 0:
                TL = tk.Toplevel(width = DISPLAY_WIDTH - 50,
                                 height = DISPLAY_HEIGHT - 50,
                                 bg = color_list[0])
                tk.Label(master = TL,
                         font = font_list[2],
                         bg = color_list[0],
                         fg = color_list[12],
                         text = "STOP!").pack()
                tk.Label(master = TL,
                         text = " mindestens einen ",
                         font = font_list[3],
                         bg = color_list[0],
                         fg = color_list[13]).pack()
                tk.Label(master = TL,
                         text = "Bereich auswählen!!!",
                         font = font_list[3],
                         bg = color_list[0],
                         fg = color_list[13]).pack()
            else:
                z = 3 in history_list
                if z == 1:
                    master.switch_frame(frame_set_flash)
                else:
                    master.switch_frame(frame_select_color)
        tk.Button(text = "WEITER",
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = forward
                        ).place(x = DISPLAY_WIDTH - 2 * WIDTH - DISTANCE,
                                    y = 6 * HEIGHT + 6 * DISTANCE,
                                    width = 2 * WIDTH,
                                    height = 2 * HEIGHT)


class frame_select_mode(tk.Frame):
    """Farbwechselfenster.
    
    Hier kann man auswählen:
    - LED's blinken lassen,
    - LED's blitzen lassen oder
    - langsam die Farbe wechseln lassen."""

    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 3:
            history_list.append(3)
        tk.Label(self,
                      text = "Modus auswählen",
                      font = font_list[1],
                      bg = BG_COLOR,
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                   y = DISTANCE,
                                   width = DISPLAY_WIDTH - 2 * DISTANCE,
                                   height = HEIGHT)
        tk.Button(self,
                        text = "blinken",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_area)
                        ).place(x = DISTANCE,
                                    y = HEIGHT + 2 * DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * WIDTH - DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self,
                        text = "wechseln",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR
                        ).place(x = DISTANCE,
                                    y = 3 * HEIGHT + 3 * DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * WIDTH - DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self,
                        text = "blitzen",
                        font = font_list[1],
                        bg = BG_COLOR,
                        fg = FG_COLOR
                        ).place(x = DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    width = DISPLAY_WIDTH - 2 * WIDTH - DISTANCE,
                                    height = 2 * HEIGHT)


class frame_set_color(tk.Frame):
    """Farbeinstellungsfenster.
   
    - zum einstellen der Farben über TK-Scale"""
    
    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 4:
            history_list.append(4)
        tk.Label(self,
                      text = "Farbe einstellen",
                      font = font_list[1],
                      fg = FG_COLOR, 
                      bg = BG_COLOR
                      ).place(x = DISTANCE,
                                  y = DISTANCE,
                                  width = DISPLAY_WIDTH - 2 * DISTANCE,
                                  height = HEIGHT)
# Rot einstellen
        Fader_Red = tk.Scale(self,
                                           from_ = 255,
                                           to = 0,
                                           bg = color_list[0],
                                           troughcolor = color_list[13], 
                                           tickinterval = 50, 
                                           sliderlength = 50)
		#Fader_Red.set(Red)
        Fader_Red.place(x = DISTANCE,
                                   y = HEIGHT + 2 * DISTANCE,
                                   width = 2 * WIDTH - DISTANCE,
                                   height = DISPLAY_HEIGHT - 2 * HEIGHT - 5 * DISTANCE)
# Grün einstellen
        Fader_Green = tk.Scale(self,
                                           from_ = 255,
                                           to = 0,
                                           bg = color_list[4],
                                           troughcolor = color_list[13], 
                                           tickinterval = 50, 
                                           sliderlength = 50)
		#Fader_Green.set(Green)
        Fader_Green.place(x = 2 * WIDTH +DISTANCE,
                          y = HEIGHT + 2 * DISTANCE,
                          width = 2 * WIDTH - DISTANCE,
                          height = DISPLAY_HEIGHT - 2 * HEIGHT - 5 * DISTANCE)
# Blau einstellen
        Fader_Blue = tk.Scale(self,
                                           from_ = 255,
                                           to = 0,
                                           bg = color_list[8],
                                           troughcolor = color_list[13], 
                                           tickinterval = 50, 
                                           sliderlength = 50)
		#Fader_Blue.set(Blue)
        Fader_Blue.place(x = 4 * WIDTH + DISTANCE,
                         y = HEIGHT + 2 * DISTANCE,
                         width = 2 * WIDTH - DISTANCE,
                         height = DISPLAY_HEIGHT - 2 * HEIGHT - 5 * DISTANCE)
# Helligkeit einstellen
        Fader_Light = tk.Scale(self,
                                           from_ = 255,
                                           to = 0,
                                           bg = color_list[12],
                                           troughcolor = color_list[13], 
                                           tickinterval = 50, 
                                           sliderlength = 50)
		#Fader_Light.set(Hell)
        Fader_Light.place(x = 6 * WIDTH + DISTANCE,
                          y= HEIGHT + 2 * DISTANCE,
                          width = 2 * WIDTH  - DISTANCE,
                          height = DISPLAY_HEIGHT - 2 * HEIGHT - 5 * DISTANCE)


class frame_set_flash(tk.Frame):
    """"""

    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 5:
            history_list.append(5)
        self.Time = tk.IntVar(value=1)
        tk.Label(self,
                      text = "Farbwechseleinstellungen",
                      font = font_list[1],
                      bg = BG_COLOR, 
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                   y = DISTANCE,
                                   width = DISPLAY_WIDTH - 2 * DISTANCE,
                                   height = HEIGHT)
        tk.Label(self,
                      text = "Farbe 1", 
                      bg = BG_COLOR,
                      fg = FG_COLOR,
                      ).place(x = DISTANCE,
                                  y = HEIGHT + 2 * DISTANCE,
                                  height = 2 * HEIGHT,
                                  width = 3 * WIDTH)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_color)
                        ).place(x = 3 * WIDTH + 2 * DISTANCE,
                                    y = HEIGHT + 2 * DISTANCE,
                                    height = 2 * HEIGHT,
                                    width = 3 * WIDTH + 2 * DISTANCE)
        tk.Label(self,
                      text = "Farbe 2", 
                      bg = BG_COLOR,
                      fg = FG_COLOR,
                      ).place(x = DISTANCE,
                                  y = 3 * HEIGHT + 3 * DISTANCE,
                                  height = 2 * HEIGHT,
                                  width = 3 * WIDTH)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        command = lambda: master.switch_frame(frame_select_color)
                        ).place(x = 3 * WIDTH + 2 * DISTANCE,
                                    y = 3 * HEIGHT + 3 * DISTANCE,
                                    height = 2 * HEIGHT,
                                    width = 3 * WIDTH + 2 * DISTANCE)
        tk.Label(self,
                      bg = BG_COLOR,
                      fg = FG_COLOR,
                      text = "Zeit in s"
                      ).place(x = DISTANCE,
                                  y = 5 * HEIGHT + 4 * DISTANCE,
                                  height = 2 * HEIGHT,
                                  width = 3 * WIDTH)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        text = "<",
                        command = self.decrease
                        ).place(x = 3 * WIDTH + 2 * DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    height = 2 * HEIGHT,
                                    width = WIDTH)
        tk.Label(self,
                      bg = BG_COLOR,
                      fg = FG_COLOR,
                      textvariable = self.Time
                      ).place(x = 4 * WIDTH + 3 * DISTANCE,
                                  y = 5 * HEIGHT + 4 * DISTANCE,
                                  height = 2 * HEIGHT,
                                  width = WIDTH)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        text = ">",
                        command = self.increase
                        ).place(x = 5 * WIDTH + 4 * DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    height = 2 * HEIGHT,
                                    width = WIDTH)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = BG_COLOR,
                        text = "start"
                        ).place(x = DISPLAY_WIDTH - WIDTH - 2 * DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    height = 2 * HEIGHT,
                                    width = WIDTH + DISTANCE)
		
    def increase(self):
        if self.Time.get() < 60:
            self.Time.set(self.Time.get() + 1)

    def decrease(self):
        if self.Time.get()>1:
            self.Time.set(self.Time.get() - 1)


class frame_config(tk.Frame):
    """Einstellungen.
    
    Ein verstecktes Fenster um Einstellungen vorzunehmen.
    - Vollbildmodus an/aus
    - Hintergrundfarbe (geplant)
    - Schriftfarbe (geplant)"""

    def __init__(self, master):
        tk.Frame.__init__(self, bg = BG_COLOR)
        if history_list[-1] != 99:
            history_list.append(99)
        tk.Label(self,
                      text = "Einstellungen",
                      font = font_list[1],
                      bg = BG_COLOR, 
                      fg = FG_COLOR
                      ).place(x = DISTANCE,
                                   y = DISTANCE,
                                   width = DISPLAY_WIDTH - 2 * DISTANCE,
                                   height = HEIGHT)
        tk.Button(self,
                        bg = BG_COLOR,
                        fg = FG_COLOR,
                        font = font_list[1],
                        text = "Vollbild ein/aus",
                        command = lambda: master.toggleFullScreen(master.fullScreenState)
                        ).place(x = DISTANCE,
                                    y = HEIGHT + 2 * DISTANCE,
                                    width = DISPLAY_WIDTH / 2 - 1.5 * DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self, 
                        bg = BG_COLOR, 
                        fg = FG_COLOR, 
                        font = font_list[1], 
                        text = "Hintergundfarbe"
                        ).place(x = DISTANCE,
                                    y = 3 * HEIGHT + 3 * DISTANCE,
                                    width = DISPLAY_WIDTH / 2 - 1.5 * DISTANCE,
                                    height = 2 * HEIGHT)
        tk.Button(self, 
                        bg = BG_COLOR, 
                        fg = FG_COLOR, 
                        font = font_list[1], 
                        text = "Schriftfarbe"
                        ).place(x = DISTANCE,
                                    y = 5 * HEIGHT + 4 * DISTANCE,
                                    width = DISPLAY_WIDTH / 2 - 1.5 * DISTANCE,
                                    height = 2 * HEIGHT)


if __name__ == '__main__':
	app = main_win()
