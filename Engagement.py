from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.base import runTouchApp
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox

from AppKit import NSApplication, NSApp, NSWindow, NSApplicationActivateIgnoringOtherApps, NSWindowCollectionBehavior, NSFloatingWindowLevel, NSNormalWindowLevel

import calendar
import pandas as pd
import time
from datetime import datetime
import os
import matplotlib.pyplot as plt
import requests
import shutil

class MyScreen(Screen):
    pass

class EngagementApp(App):
    def __init__(self) -> None:
        super().__init__()
        self.status = None
        self.df = pd.DataFrame(columns=['Time', 'Status'])
        self.className = ""
        self.live = False
        self.keep_status_on_top = False
        self.keep_status_only_on_top = False
        self.pause_second_click = False
        self.first_start_click = True
        self.break_time = 0
        self.total_break_time = 0
    
    def on_top(self, instance):
        self.keep_status_on_top = True
        self.keep_status_only_on_top = False
        self.keep_on_topButton.background_color = [2, 2, 2, 1]
        self.not_on_topButton.background_color = [1, 1, 1, 1]
        self.keep_status_on_topButton.background_color = [1, 1, 1, 1]

    def not_on_top(self, instance):
        self.keep_status_on_top = False
        self.keep_status_only_on_top = False
        self.keep_on_topButton.background_color = [1, 1, 1, 1]
        self.not_on_topButton.background_color = [2, 2, 2, 1]
        self.keep_status_on_topButton.background_color = [1, 1, 1, 1]


    def status_on_top(self, instance):
        self.keep_status_only_on_top = True
        self.keep_status_on_top = False
        self.keep_on_topButton.background_color = [1, 1, 1, 1]
        self.not_on_topButton.background_color = [1, 1, 1, 1]
        self.keep_status_on_topButton.background_color = [2, 2, 2, 1]


    def on_green_press(self, instance):
        if self.live:
            self.status = 'Green'
            self.green_button[self.pos].background_color = [0,2,0,1]
            self.yellow_button[self.pos].background_color = [1, 1, 0, 1]
            self.red_button[self.pos].background_color = [1, 0, 0, 1]
            self.purple_button[self.pos].background_color = [0.8, 0.4, 1, 1]
            self.white_button[self.pos].background_color = [1, 1, 1, 1]

    def on_yellow_press(self, instance):
        if self.live:
            self.green_button[self.pos].background_color = [0,1,0,1]
            self.yellow_button[self.pos].background_color = [2, 2, 0, 1]
            self.red_button[self.pos].background_color = [1, 0, 0, 1]
            self.purple_button[self.pos].background_color = [0.8, 0.4, 1, 1]
            self.white_button[self.pos].background_color = [1, 1, 1, 1]

            self.status = 'Yellow'

    def on_red_press(self, instance):
        if self.live:
            self.green_button[self.pos].background_color = [0,1,0,1]
            self.yellow_button[self.pos].background_color =[1, 1, 0, 1]
            self.red_button[self.pos].background_color =[2, 0, 0, 1]
            self.purple_button[self.pos].background_color = [0.8, 0.4, 1, 1]
            self.white_button[self.pos].background_color = [1, 1, 1, 1]

            self.status = 'Red'

    def on_white_press(self, instance):
        if self.live:
            self.green_button[self.pos].background_color = [0,1,0,1]
            self.yellow_button[self.pos].background_color =[1, 1, 0, 1]
            self.red_button[self.pos].background_color =[1, 0, 0, 1]
            self.purple_button[self.pos].background_color = [0.8, 0.4, 1, 1]
            self.white_button[self.pos].background_color = [2, 2, 2, 1]

            self.status = 'White'

    def on_purple_press(self, instance):
        if self.live:
            self.green_button[self.pos].background_color = [0,1,0,1]
            self.yellow_button[self.pos].background_color =[1, 1, 0, 1]
            self.red_button[self.pos].background_color =[1, 0, 0, 1]
            self.purple_button[self.pos].background_color = [1.6, 0.8, 2, 1]
            self.white_button[self.pos].background_color = [1, 1, 1, 1]

            self.status = 'Purple'

    def on_add_drop_press(self, isntance):
        # Define a callback function to handle the user's input
        def on_submit(instance):
            class_name = text_input.text

            if class_name == "OTHER":
                print("Invalid input: You can't drop this class!")
                return

            print('User entered class name:', class_name)
            folder_path = os.path.join(".","Engagement Data", "Current Class Data", class_name)
            new_folder_path = os.path.join(".", "Engagement Data", "Archived Data")
            self.main_screen.clear_widgets()
            if os.path.exists(folder_path):
                print("Dropping class:", class_name)
                full_path = new_folder_path + "/" + class_name
                if os.path.exists(full_path):
                    i = 1
                    while os.path.exists(f"{full_path}_copy{i}"):
                        i += 1
                    full_path = f"{full_path}_copy{i}"
                shutil.move(folder_path, full_path)
                print("Moved class from Current Class Data to Archived Data")
            else:
                os.makedirs(folder_path)
                print("Created class:", class_name)
            
            popup.dismiss()
            EngagementApp().run()
            EngagementApp().build()

        # Create a TextInput widget to get the user's input
        text_input = TextInput(text='', multiline=False, font_size = 50, hint_text = "Enter class name here...")

        # Create a Popup widget to display the TextInput
        popup = Popup(title='Enter a class name to add or drop', content=text_input,
                      size_hint=(None, None), size=(800, 200))

        # Bind the callback function to the TextInput's on_text_validate event
        text_input.bind(on_text_validate=on_submit)

        # Open the Popup widget
        popup.open()
        
    def on_start_press(self, instance):
        # if self.live:
        #     return
        
        if self.pause_second_click:
            self.pause_second_click = False
            self.total_break_time += self.break_time
            self.back_button[self.pos].text = "END"
            print("Unpause!!")
            return
        
        if (not self.pause_second_click) and (not self.first_start_click):
            self.pause_second_click = True
            self.break_begin_time = time.time()
            self.start_button[self.pos].text = "PAUSED"
            print("PAUSE!!")
            return

        self.first_start_click = False

        self.green_button[self.pos].background_color = [0,2,0,1]

        self.start_button[self.pos].text = "In Class"
        self.back_button[self.pos].text = "END"

        self.live = True
        self.df = pd.DataFrame(columns=['Time', 'Status'])
        self.start_time = time.time()
        self.status = 'Green'
        self.thisDataClass = self.currentClass
        print("Welcome to: " + self.thisDataClass)
        print()
        self.event = Clock.schedule_interval(self.update_df, 0.1)

        if self.keep_status_only_on_top:
            self.on_top_event = Clock.schedule_interval(self.update_quick,0.1)

    def on_settings_confirm(self, instance):
        if self.keep_status_on_top:
            self.on_top_event = Clock.schedule_interval(self.update_quick,0.1)
        else:
            print("CANCEL")
            if hasattr(self, 'on_top_event'):
                print("NO NEED")
                self.on_top_event.cancel()
            window = NSApp.windows()[-1]
            window.setLevel_(NSNormalWindowLevel)
    
    def on_back_press(self, instance):
        self.first_start_click = True
        
        if not self.live:
            print("You didn't start this class")
            return

        print("All done!")

        # Reset buttons
        self.green_button[self.pos].background_color = [0,1,0,1]
        self.yellow_button[self.pos].background_color =[1, 1, 0, 1]
        self.red_button[self.pos].background_color =[1, 0, 0, 1]
        self.purple_button[self.pos].background_color = [0.8, 0.4, 1, 1]
        self.white_button[self.pos].background_color = [1, 1, 1, 1]

        self.start_button[self.pos].text = "START"
        self.back_button[self.pos].text = "BACK"

        # No longer live
        self.live = False
        self.event.cancel()
        if self.keep_status_only_on_top:
            self.on_top_event.cancel()
            window = NSApp.windows()[-1]
            window.setLevel_(NSNormalWindowLevel)

        Window.borderless = False
        # Create the "Elapsed Time" column by taking the difference of the "Time" column
        self.df["Elapsed Time"] = self.df["Time"].diff()

        # Fill the first row of the "Elapsed Time" column with the first value of the "Time" column
        self.df["Elapsed Time"].fillna(self.df["Time"], inplace=True)
        #self.df["Elapsed Time"] -= self.df["Time"].iloc[0]

        def Collapse_DF(df):
            collapsed_df = df.groupby("Status")["Elapsed Time"].sum().reset_index()
            # Calculate the total elapsed time
            total_elapsed_time = collapsed_df["Elapsed Time"].sum()

            # Calculate the percentage of the total elapsed time for each status value
            collapsed_df["Percentage"] = (collapsed_df["Elapsed Time"] / total_elapsed_time * 100).round(1)
            return collapsed_df

        # Get the current date and time
        now = datetime.now()

        # Check if folder already exists
        folder_path = "./Engagement Data/Current Class Data/" + self.thisDataClass + "/Lecture " + now.strftime("%m-%d")
        overall_folder_path = "./Engagement Data/Current Class Data/" + self.thisDataClass
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        collapsed_df = Collapse_DF(self.df)
        
        collapsed_df.to_csv(folder_path + "/Stats.csv", index=False)
        self.df.to_csv(folder_path + "/RAW data" + ".csv", index=False)

        if not os.path.exists(overall_folder_path + "/Overall_stats" + ".csv"):
            self.df.to_csv(overall_folder_path + "/Overall_stats" + ".csv", index=False)
            overall_collapsed = Collapse_DF(self.df)
        else:
            old_data = pd.read_csv(overall_folder_path + "/Overall_stats" + ".csv")
            #updated_df = old_data.append(self.df, ignore_index=True)
            updated_df = pd.concat([old_data, self.df], ignore_index=True)
            updated_df.to_csv(overall_folder_path + "/Overall_stats" + ".csv", index=False)
            overall_collapsed = Collapse_DF(updated_df)


        def CreatePieChart(df, overall, path):
            # Convert the total time from seconds to minutes and seconds
            total_time = int(df['Elapsed Time'].sum())
            minutes = total_time // 60
            seconds = total_time % 60
            total_time_str = f"{minutes} min {seconds} sec"

            # Create a pie chart using the grouped data
            fig, ax = plt.subplots()
            ax.pie(df['Elapsed Time'], labels = df['Status'], colors = df['Status'], autopct=lambda pct: "{:.1f}%\n({:.1f} min)".format(pct, pct/100 * sum(df['Elapsed Time'])/60), startangle=90, wedgeprops = {'linewidth': 1, 'edgecolor': 'black'})

            if overall:
                # Add a title and legend to the chart
                ax.set_title('Total Lecture Time: ' + total_time_str)
                ax.legend(title='Status', loc='center left', bbox_to_anchor=(1, 0.5))
                plt.savefig(path + '/Overall Pie Chart' + '.png')
            else:
                # Add a title and legend to the chart
                ax.set_title('Lecture Time: ' + total_time_str)
                ax.legend(title='Status', loc='center left', bbox_to_anchor=(1, 0.5))
                plt.savefig(path + '/Pie Chart' + '.png')
            plt.show()

        CreatePieChart(collapsed_df, False, folder_path)
        CreatePieChart(overall_collapsed, True, overall_folder_path)

        # Add a point for 0 and Green
        # Create a new row with "Green" status and time 0
        new_row = {"Time": 0, "Status": "Green"}

        # Add the new row to the beginning of the DataFrame
        self.df = pd.concat([pd.DataFrame([new_row]), self.df], ignore_index=True)

        ### CREATE TIME PLOT ###
        # Generate sample data for sleep cycles
        t = self.df["Time"]

        # Get the minimum and maximum values for the x-axis
        xmin = self.df["Time"].min()
        xmax = self.df["Time"].max()

        # set values for colors
        mapping = {'White': 0, 'Red': 1, 'Yellow': 2, 'Green': 3, 'Purple': 4}
        engage_status = self.df['Status'].map(mapping)

        # Create a figure and two subplots
        # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 8), sharex=True)
        fig, ax1 = plt.subplots(figsize=(10, 8))


        # Set the x-axis limits
        ax1.set_xlim([0, xmax])

        # Plot the sleep cycle data on the top subplot
        ax1.plot(t, engage_status, color='#007aff')
        ax1.fill_between(t, engage_status, color='#007aff', alpha=0.2)
        ax1.set_ylim([-0.5, 4.5])
        ax1.set_yticks([0, 1, 2, 3, 4])
        ax1.set_yticklabels(['White', 'Red', 'Yellow', 'Green', 'Purple'])
        ax1.grid(color='#c7c7cc', linewidth=0.5, linestyle='-')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.tick_params(axis='y', length=0, width=0, labelsize=14)

        # Add labels to the x-axis and y-axes
        plt.xlabel('Time', fontsize=16)
        ax1.set_ylabel('Engagement Status', fontsize=16)
        #ax2.set_ylabel('Duration', fontsize=16)

        # Add a title to the figure
        plt.suptitle('Engagment Analysis', fontsize=20)

        plt.savefig(folder_path + '/Time Plot' + '.png')
        plt.show()

    def update_quick(self, dt):
        window = NSApp.windows()[-1]
        window.orderFrontRegardless()
        window.setLevel_(NSFloatingWindowLevel)

    def update_df(self, dt):
        if self.pause_second_click:
            self.break_time = time.time() - self.break_begin_time

        if not self.pause_second_click:
            elapsed_time = time.time() - self.start_time - self.total_break_time
            #self.df = self.df.append({'Time': elapsed_time, 'Status': self.status}, ignore_index=True)
            # Create a new DataFrame with the row data
            new_data = pd.DataFrame({'Time': [elapsed_time], 'Status': [self.status]})
            # Concatenate the new DataFrame with the existing DataFrame
            self.df = pd.concat([self.df, new_data], ignore_index=True)
            rounded_time = round(elapsed_time)
            elapsed_min = rounded_time//60
            elapsed_sec = rounded_time%60
            if elapsed_sec < 10:
                elapsed_sec = "0" + str(elapsed_sec)
            if elapsed_time < 1:
                self.start_button[self.pos].text = "In Class"
                self.label[self.pos].text = "Welcome!"
            else:
                self.start_button[self.pos].text = str(elapsed_min) + ":" + str(elapsed_sec)
                self.label[self.pos].text = self.currentClass

    def GetClassStats(self):
        # Initialize an empty list to store the data
        data = []
        data_dir = "./Engagement Data/Current Class Data"
        # Loop through each class folder
        for class_name in self.classes:
            class_dir = os.path.join(data_dir, class_name)
            for lecture_name in os.listdir(class_dir):
                if lecture_name.startswith("Lecture"):
                    # Extract the last 5 characters of the lecture folder name
                    date_str = lecture_name[-5:]
                
                    # Parse the date string into a datetime object
                    date_obj = datetime.strptime(date_str, "%m-%d")
                    
                    # Get the month and day values
                    month = date_obj.strftime("%B")
                    day = date_obj.day
                    
                    # Append the data to the list
                    data.append({
                        "Class": class_name,
                        "Date": date_obj,
                        "Month": month,
                        "Day": day
                    })
        # Create a dataframe from the data
        df = pd.DataFrame(data)
        return df

    def build(self):

        # Create a ScreenManager to manage multiple screens
        screen_manager = ScreenManager()
        # Create the main screen with a BoxLayout to hold the content
        self.main_screen = Screen(name='main')

        # Initial Size
        Window.size = (dp(250), dp(400))
        Window.top = 0  # sets the top coordinate of the window to 100 pixels
        Window.left = 0  # sets the left coordinate of the window to 100 pixels

        # Check for first time!
        first_time_dir = "./Engagement Data"
        dir_path = "./Engagement Data/Current Class Data"
        archive_path = "./Engagement Data/Archived Data"
        first_time = not os.path.exists(first_time_dir)
        if first_time:
            os.makedirs(first_time_dir)
            os.makedirs(dir_path)
            os.makedirs(os.path.join(dir_path,"OTHER"))
            os.makedirs(archive_path)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        # if first_time:
        #     popup_title = 'Welcome to the Engagement App!'
        #     popup = Popup(title=popup_title, size_hint=(None, None), size=(900, 500), auto_dismiss=False)

        #     instruction_text = "- Use the Add/Drop button to add or drop classes.\n- If you are dropping a class, it must be written exactly how it appears on the screen.\n- The stats button doesn't work yet, sorry!\n- To start a class, click on it, and then press start! Results will be saved in the Engagement Data folder.\n- The buttons can be glitchy right after adding/dropping a class. You can click on a class and then click back after addding/dropping and everything should then be fine!"
        #     popup_content = Label(text='\n\nInstructions:\n'+instruction_text, halign='left', valign="top", text_size = (800,500))

        #     popup.content=popup_content
        #     # Create the popup with the label as its content
        #     #popup = Popup(title=popup_title, content=popup_content, size_hint=(None, None), size=(900, 500), auto_dismiss=False)
        #     popup.open()


        layout = BoxLayout(orientation='vertical', spacing = 20, padding = 20)
        label = Label(text='Engagement', font_size=dp(60), halign='center', size_hint = (1, None), height = dp(160))

        layout.add_widget(label)
            
        # Get class names
        path = './Engagement Data/Current Class Data'
        classes = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        self.classes = sorted(classes, key=lambda x: (x == 'OTHER', x))

        button_colors = ['#ffbe0b', '#fb5607', '#ff006e', '#8338ec', '#3a86ff', '#00b4d8', '#00d1b2', '#8bc34a', '#cddc39', '#ffc107', '#ff5722', '#795548', '#9e9e9e', '#607d8b', '#455a64']
        a = 0
        for i in self.classes:
            button = Button(text=i, font_size=50, halign='center', background_color = button_colors[a]) 
            class_name = i
            button.bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, class_name))
            layout.add_widget(button)
            a += 1
        
        button_layout = BoxLayout(spacing=20, size_hint = (1, None), height = "80dp")
        add_drop_button = Button(text='Add/Drop', font_size=40, size_hint=(0.5, 1), on_press=self.on_add_drop_press)
        #add_drop_button.bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, "main"))

        settings_button = Button(text='Settings', font_size=40, size_hint=(0.5, 1))
        settings_button.bind(on_press=lambda _, class_name="Settings": self.show_class_screen(screen_manager, "Settings"))

        button_layout.add_widget(add_drop_button)
        button_layout.add_widget(settings_button)
        layout.add_widget(button_layout)

        # Add the main layout to the main screen and add it to the screen manager
        self.main_screen.add_widget(layout)
        screen_manager.add_widget(self.main_screen)

        # Create a separate screen for each class
        self.label = []
        
        self.green_button = []
        self.yellow_button = []
        self.red_button = []
        self.white_button = []
        self.purple_button = []

        self.start_button = []
        self.back_button = []

        for i,cla in enumerate(self.classes):
            class_name = cla
            class_screen = Screen(name=class_name)
            class_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

            # Add class label
            self.label.append(Label(text=class_name, font_size=30, halign='center', size_hint=(1, 0.3)))
            class_layout.add_widget(self.label[i])

            # Add the five buttons
            buttons_layout = BoxLayout(orientation='horizontal', spacing=10, padding=2)

            focus_layout = BoxLayout(orientation='vertical', spacing=10, padding=2)
            NO_focus_layout = BoxLayout(orientation='vertical', spacing=10, padding=2)

            self.green_button.append(Button(text='', font_size=20, height=50, background_color=[0, 1, 0, 1], on_press=self.on_green_press))
            self.yellow_button.append(Button(text='', font_size=20, height=50, background_color=[1, 1, 0, 1], on_press=self.on_yellow_press))
            self.red_button.append(Button(text='', font_size=20, height=50, background_color=[1, 0, 0, 1], on_press=self.on_red_press))
            self.white_button.append(Button(text='', font_size=20, height=50, background_color=[1, 1, 1, 1], on_press=self.on_white_press))
            self.purple_button.append(Button(text='', font_size=20, height=50, background_color=[0.8, 0.4, 1, 1], on_press=self.on_purple_press))


            focus_layout.add_widget(self.green_button[i])
            focus_layout.add_widget(self.yellow_button[i])
            focus_layout.add_widget(self.red_button[i])
            NO_focus_layout.add_widget(self.white_button[i])
            NO_focus_layout.add_widget(self.purple_button[i])

            buttons_layout.add_widget(focus_layout)
            buttons_layout.add_widget(NO_focus_layout)

            class_layout.add_widget(buttons_layout)
            
            Start_Stop_layout = BoxLayout(orientation='horizontal', spacing=10, padding=2, size_hint = (1, 0.3))
            
            # Add a Start button
            self.start_button.append(Button(text='START', size_hint=(0.7, 1), font_size=25, halign='center', pos_hint={"center_x": 0.5}, on_press=self.on_start_press))
            Start_Stop_layout.add_widget(self.start_button[i])

            # Back button
            self.back_button.append(Button(text="<---", font_size=20, size_hint=(0.3, 1), halign='center',on_press=self.on_back_press))
            self.back_button[i].bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, "main"))
            Start_Stop_layout.add_widget(self.back_button[i])
            

            class_layout.add_widget(Start_Stop_layout)


            # Add to app
            class_screen.add_widget(class_layout)
            screen_manager.add_widget(class_screen)

        # Settings screen
        settings_screen = Screen(name="Settings")
        settings_layout = BoxLayout(orientation = "vertical", spacing = 20, padding = 50)
        title_settings = Label(text="SETTINGS", font_size=100)
        self.keep_on_topButton = Button(text="Keep the window on top", font_size=50, on_press=self.on_top, background_color=[1, 1, 1, 1])
        self.keep_status_on_topButton = Button(text="Only keep window\n on top in session",halign = "center", font_size=50, on_press=self.status_on_top, background_color=[1, 1, 1, 1])
        self.not_on_topButton = Button(text="Don't keep on top", font_size=50, on_press=self.not_on_top, background_color=[2, 2, 2, 1])

        settings_layout.add_widget(title_settings)
        settings_layout.add_widget(self.keep_on_topButton)
        settings_layout.add_widget(self.keep_status_on_topButton)
        settings_layout.add_widget(self.not_on_topButton)

        bottom_buttons = BoxLayout(orientation = "horizontal", spacing = 50, padding = 50)

        settings_back_button = Button(text='<--- SAVE \nAND GO BACK', font_size=50, halign='center', on_press=self.on_settings_confirm)
        settings_back_button.bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, "main"))
        settings_STATS_button = Button(text='STATS', font_size=50, halign='center')
        settings_STATS_button.bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, "Stats"))

        bottom_buttons.add_widget(settings_back_button)
        bottom_buttons.add_widget(settings_STATS_button)

        settings_layout.add_widget(bottom_buttons)

        settings_screen.add_widget(settings_layout)

        screen_manager.add_widget(settings_screen)




        # Stats Screen
        stats_screen = Screen(name="Stats")
        
        # Get Info
        def GetMonthDays():
            now = datetime.now()
            month = now.month
            year = now.year
            days_in_month = calendar.monthrange(year, month)[1]
            return (calendar.month_name[month], days_in_month)
        
        # Build Layout
        class_stat_info = self.GetClassStats()
        Stats_layout = BoxLayout(orientation = "vertical")
        Stats_layout.add_widget(Label(text=GetMonthDays()[0], halign = "center", size_hint = (1, None), height = dp(100),font_size=100))

        Days_layout = BoxLayout(orientation = "horizontal", spacing = 10, padding = 15, size_hint = (1, None), height = dp(50))
        day_labels = ["SUN", "MON", "TUES", "WEDS", "THURS", "FRI", "SAT"]
        for day in day_labels:
            Days_layout.add_widget(Label(text=day))

        Stats_layout.add_widget(Days_layout)

        CalenderLayout = StackLayout(spacing = 10, padding = 15)
        # Add blank buttons at the beginning of the first row until the first day of the month falls on a Sunday
        first_day_of_month = calendar.weekday(datetime.now().year, datetime.now().month, 1)
        for i in range(first_day_of_month):
            size = dp(65)
            b = Button(text=" ", font_size=60, size_hint=(None, None), size=(size, size))
            CalenderLayout.add_widget(b)

        # Add buttons for each day of the month
        for i in range(1, GetMonthDays()[1] + 1):
            size = dp(65)
            b = Button(text=str(i), font_size=60, size_hint=(None, None), size=(size, size))
            # Iterate over the rows of the dataframe
            for index, row in class_stat_info.iterrows():
                # Check if the Month and Day columns match the specified values
                if row["Month"] == GetMonthDays()[0] and row["Day"] == i:
                    b.background_color=[0, 1, 0, 1]
            CalenderLayout.add_widget(b)

        toggle_back_layout = BoxLayout(orientation = "horizontal", spacing = 20, padding = 20)
        toggle_back_layout.add_widget(Button(text="Last Month", font_size=40, size_hint = (1, None), height = dp(100)))
        toggle_back_layout.add_widget(Button(text="Next Month", font_size=40, size_hint = (1, None), height = dp(100)))
        back_to_settings = Button(text="Back", font_size=40, size_hint = (1, None), height = dp(100))
        back_to_settings.bind(on_press=lambda _, class_name=class_name: self.show_class_screen(screen_manager, "Settings"))
        toggle_back_layout.add_widget(back_to_settings)

        Stats_layout.add_widget(CalenderLayout)
        Stats_layout.add_widget(toggle_back_layout)

        stats_screen.add_widget(Stats_layout)
        screen_manager.add_widget(stats_screen)


        return screen_manager

    def show_class_screen(self, screen_manager, class_name):
        screen_manager.current = class_name
        self.currentClass = class_name
        if class_name == "main":
            Window.size = (dp(250), dp(400))
        elif class_name == "Settings":
            pass
        elif class_name == "Stats":
            pass
        else:
            Window.size = (100 + len(class_name)*2, 160)
            self.pos = self.classes.index(self.currentClass)

if __name__ == '__main__':
    EngagementApp().run()
