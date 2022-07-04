import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import pandas as pd
import re
from PIL import Image, ImageTk  # <- import PIL for the images
import os
# Import my modules
import file_handler as fh
import process_tabs as pt
import process_columns as pc
import destination_ip as dip
import find_duplicates as fd

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    # Application window width and height variables
    WIDTH = 900
    HEIGHT = 520

    # Column and row indices
    COLUMN_INDEX = 1
    ROW_INDEX = 0

    # Application name
    APP_NAME = "UHS Master"

    # Base file path
    PATH = os.path.dirname(os.path.realpath(__file__))

    # Store Excel file path - default path is current project path
    file_path = PATH + "/UHS_Master_list.xlsx"

    # Size we want to load images as
    image_size = 48

    # Global variables
    col_index = 'pocmonitor_sn'
    destination_ip_string = ''
    destination_ip = ''
    list_of_columns_to_drop = []
    list_of_column_values = []
    combine_all_column_values = []

    # Initialization method
    def __init__(self):
        # Initialize everything upon app creation contained in this section
        super().__init__()

        self.title(App.APP_NAME)
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ============ Handle Excel Image Start ============

        # Take the base file path of the project and append the image file path
        # resize the image to fit properly.
        excel_image = ImageTk.PhotoImage(
            Image.open(self.PATH + "/images/excel_icon.png").resize((self.image_size, self.image_size),
                                                                    Image.ANTIALIAS))

        # ============ Handle Excel Image End ============

        # ============ Container(s)/Frame(s) Start ============

        '''

             - Configure grid layout (2x1) i.e. 2 columns and 1 row (col x row).
             - Note: weight parameter determines how wide the column will
                     occupy, which is relative to the columns.

        '''

        # The columnconfigure() method configures the column index of the grid
        # since we will have 2 columns the current index value is 1.  The columns
        # start from 0 - so 1 one is actually 2 columns and 0 is one.
        self.grid_columnconfigure(App.COLUMN_INDEX, weight=1)

        # The rowconfigure() method configures the row index of the grid
        # we will have only one row so the current index value is 0.
        self.grid_rowconfigure(App.ROW_INDEX, weight=1)

        # Configure left container/frame
        self.left_container_frame = customtkinter.CTkFrame(master=self, width=0)
        self.left_container_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nwsw")

        # Configure center container/frame
        self.center_container_frame = customtkinter.CTkFrame(master=self, width=600, corner_radius=15)
        self.center_container_frame.grid(row=0, column=1, padx=0, pady=20, sticky="ns")

        # Configure right container/frame
        self.right_container_frame = customtkinter.CTkFrame(master=self, width=0, corner_radius=15)
        self.right_container_frame.grid(row=0, column=2, padx=0, pady=0, sticky="nese")

        # ============ Container(s)/Frame(s) End ============

        # ============ Labels Start ============

        # Place welcome banner label in top center of center container
        self.banner_label = customtkinter.CTkLabel(master=self.center_container_frame,
                                                   text="UHS Configuration Master",
                                                   text_font=("Roboto Large", -20))  # font name and size in px
        # Set the welcome banner labels grid configuration
        self.banner_label.grid(row=0, column=0, pady=10, padx=10, sticky='n')

        # Displays first line of text when opening the program - basically and about text.
        self.initial_text_label = customtkinter.CTkLabel(master=self.center_container_frame,
                                                         text="Enter the serial number you wish to obtain\n" +
                                                              "the configurations for in the box below",
                                                         height=300,
                                                         fg_color=("white", "gray38"),  # <- custom tuple-color
                                                         justify=tkinter.CENTER)
        self.initial_text_label.grid(column=0, row=1, sticky="n", padx=15, pady=0)

        # ============ Labels End ============

        # ============ Buttons Start ============

        # The checkbox will copy configurations to the clip board once pressed
        self.check_box_copy_to_clipboard = customtkinter.CTkCheckBox(master=self.center_container_frame,
                                                                     text="Copy",
                                                                     command=self.button_event(),
                                                                     bg_color=("white", "gray38"),
                                                                     corner_radius=15,
                                                                     text_color=("red", "black"),
                                                                     border_color='black')
        self.check_box_copy_to_clipboard.grid(row=1, column=0, pady=10, padx=20, sticky="se")

        # Submit serial number button
        self.submit_serial_number_button = customtkinter.CTkButton(master=self.center_container_frame,
                                                                   text="Submit",
                                                                   command=self.submit_serial_number_on_click)
        self.submit_serial_number_button.grid(row=3, column=0, pady=5, padx=20)

        # Export duplicates to excel file button
        export_duplicates_button = customtkinter.CTkButton(master=self.left_container_frame, image=excel_image,
                                                           text="Export Duplicates", width=190,
                                                           height=40,
                                                           compound="right",
                                                           command=self.export_duplicate_serial_numbers_on_click)
        export_duplicates_button.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="ns")

        # Browse file button
        excel_file_browse_button = customtkinter.CTkButton(master=self.left_container_frame, image=excel_image,
                                                           text="Import Excel File", width=190,
                                                           height=40,
                                                           compound="right", command=self.browse_files_on_click)
        excel_file_browse_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ns")

        # Submit excel file button
        self.submit_excel_file_button = customtkinter.CTkButton(master=self.left_container_frame,
                                                                text="Submit",
                                                                command=self.load_excel_file)
        self.submit_excel_file_button.grid(row=3, column=0, columnspan=2, pady=5, padx=20, sticky='ns')

        # ============ Buttons End ============

        # ============ Entry Box Start ============

        # Box the user will enter serial number in
        self.serial_number_entry = customtkinter.CTkEntry(master=self.center_container_frame,
                                                          width=120,
                                                          placeholder_text="Enter Serial Number Here!")
        self.serial_number_entry.grid(row=2, column=0, columnspan=2, pady=30, padx=20, sticky="we")

        # Box for Excel file path entry
        self.excel_file_path_entry = customtkinter.CTkEntry(master=self.left_container_frame,
                                                            width=120,
                                                            placeholder_text="Excel file path")
        self.excel_file_path_entry.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        # ============ Entry Box End ============

    # ============ Methods Begin ============ #

    def button_event(self):
        print("Meh...")

    '''
        Method: on_closing
        Purpose: Destroy the entire application window
    '''

    def on_closing(self, event=0):
        self.destroy()

    '''
        Method: browse_files_on_click
        Purpose: Allow the user to browse for then upload
                 a new Excel/configuration file.
    '''

    def browse_files_on_click(self):
        # Open file browser window
        self.file_path = self.get_file_path()
        # Insert the chosen file name into the entry box
        self.insert_file_path_to_entry_box()
        # Prepare file for processing
        self.prepare_excel_file()
        # Process excel file
        self.process_excel_file()

    '''
        Method: get_file_path
        Purpose: In the file options menu include 
                 Excel files first then all other files.
    '''

    def get_file_path(self):
        return filedialog.askopenfilename(filetypes=(("excel files", "*.xlsx"), ("All files", "*.*")))

    def insert_file_path_to_entry_box(self):
        return self.excel_file_path_entry.insert(tkinter.END, self.file_path)

    def prepare_excel_file(self):
        df = self.load_excel_file()
        return self.remove_invalid_tabs(df)

    def load_excel_file(self):
        # Store UHS excel file as pandas dataframe
        return fh.read_entire_excel_file(self.file_path)

    def remove_invalid_tabs(self, uhs_entire_excel_file_dataframe):
        # Get excel tabs list then remove invalid tabs
        return pt.remove_unwanted_tabs(pt.get_excel_tabs_list(uhs_entire_excel_file_dataframe))

    def process_excel_file(self):

        # Keep track of iterations
        iteration_count = 1
        # Get a list of valid excel tabs for later processing
        list_of_valid_tabs = self.prepare_excel_file()
        # Load the entire Excel sheet into a single dataframe
        uhs_entire_excel_file_dataframe = self.load_excel_file()

        for time_zone_tab in list_of_valid_tabs:

            # Read selected tab into dataframe
            single_tab_dataframe = pt.read_single_tab_into_dataframe(time_zone_tab, uhs_entire_excel_file_dataframe)

            # Grab the pocmonitor - incase there is a typo program will continue correctly
            pocmonitor_name = pc.check_pocmonitor_name(pc.get_excel_columns_list(single_tab_dataframe))

            # Set index to pocmonitor_name so config can be looked up by serial number
            single_tab_dataframe.set_index(pocmonitor_name, inplace=True)

            # Grab all column names and store them in a list
            list_of_all_columns = pc.get_excel_columns_list(single_tab_dataframe)

            # Get list of unwanted columns
            list_of_columns_to_drop = pc.get_empty_columns(list_of_all_columns)

            # Get values contained in unwanted columns
            list_of_column_values = pc.get_unwanted_column_values(list_of_columns_to_drop, single_tab_dataframe)

            # Find the destination IP from column values
            destination_ip_string = dip.get_destination_ip_string(list_of_column_values)

            # Get rid of unwanted/empty columns
            pc.drop_unwanted_columns(single_tab_dataframe, list_of_columns_to_drop)

            # Extract the destination ip address from string
            destination_ip = dip.get_destination_ip(destination_ip_string)

            # Create a new columns for destination IP address
            pc.create_destination_ip_column(destination_ip, single_tab_dataframe)

            # Time zone is the current tab selected
            time_zone = time_zone_tab

            # Add a new column time_zone
            single_tab_dataframe['time_zone'] = time_zone

            # Write results to csv file
            # If on the first iteration write the header to the csv file along with config
            # header information includes pocmonitor name, domain name etc..
            if iteration_count == 1:
                fh.write_to_csv_file(single_tab_dataframe, 'modified.csv')
            else:
                # Append all configs to csv file without including header info.
                fh.write_to_csv_file(single_tab_dataframe, 'modified.csv', 'a', False)

            # Increase iteration count by one.
            iteration_count += 1

    def read_modified_csv_file(self):
        # Read new csv file to data frame  use serial number as index
        return pd.read_csv(self.PATH + '/modified.csv', index_col='pocmonitor_sn')

    '''
        Method: submit_serial_number_on_click
        Purpose: Retrieve serial number configurations and display
                 the results once the user clicks the submit button.
    '''

    def submit_serial_number_on_click(self):
        global config
        # Get modified CSV file dataframe
        df_csv = self.read_modified_csv_file()
        # Create a variable to hold configuration
        config_output_text = customtkinter.StringVar()
        # Grab serial number from text box input
        sn = self.get_serial_number_from_input_text()
        # Check if serial number is the correct format
        if self.serial_number_isvalid(sn):

            # Locate the serial number
            config = df_csv.loc[int(sn)].fillna("None")

            # Set the configuration output text variable to configuration found
            config_output_text.set(config)

            # Get rid of initial widgets so updated configuration can be displayed
            self.destroy_widgets()

            # Create widgets for displaying configuration
            self.configuration_output_widgets(config_output_text)
        else:
            # Get rid of initial widgets so updated configuration can be displayed
            self.destroy_widgets()
            config_output_text.set("Please input a valid serial number or \n double check your current sn")
            self.configuration_output_widgets(config_output_text)

    '''
        Method: copy_to_clipboard_on_click
        Purpose: Copy configurations to clip board 
                 once the copy button is clicked.
    '''

    def copy_to_clipboard_on_click(self):
        self.withdraw()
        self.clipboard_clear()
        self.clipboard_append(config)
        # self.update()

    '''
        Method: get_serial_number_from_input_text
        Purpose: Retrieve serial input from entry text box.
    '''

    def get_serial_number_from_input_text(self):
        return self.serial_number_entry.get()

    '''
        Method: serial_number_isvalid
        Purpose: Make sure the user input the correct
                 serial number format.
    '''

    def serial_number_isvalid(self, serial_number):
        serial_number = self.strip_whitespace_from_serial_number_input(serial_number)
        pattern = re.compile(r'\d{10}')
        if pattern.search(serial_number):
            return True
        else:
            return False

    '''
        Method: strip_whitespace_from_serial_number_input
        Purpose: Remove any white space if the user 
                 unknowingly includes spaces.
    '''

    def strip_whitespace_from_serial_number_input(self, sn):
        return sn.strip()

    def destroy_widget(self, widget):
        return widget.destroy()

    def destroy_widgets(self):
        self.destroy_widget(self.initial_text_label)
        self.destroy_widget(self.check_box_copy_to_clipboard)

    '''
        Method: configuration_output_widgets
        Purpose: Displays configurations to user.
    '''

    def configuration_output_widgets(self, config_output_text):
        # Insert the configuration into the GUI text box
        self.initial_text_label = customtkinter.CTkLabel(master=self.center_container_frame,
                                                         textvariable=config_output_text,
                                                         height=300,
                                                         text_font=("white", 10),
                                                         fg_color=("white", "gray38"),  # <- custom tuple-color
                                                         justify=tkinter.CENTER)
        self.initial_text_label.grid(column=0, row=1, sticky="n", padx=15, pady=0)

        # The checkbox will copy configurations to the clip board once pressed
        self.check_box_copy_to_clipboard = customtkinter.CTkCheckBox(master=self.center_container_frame,
                                                                     text="Copy",
                                                                     command=self.copy_to_clipboard_on_click,
                                                                     bg_color=("white", "gray38"),
                                                                     corner_radius=15,
                                                                     text_color=("red", "black"),
                                                                     border_color='black')
        self.check_box_copy_to_clipboard.grid(row=1, column=0, pady=10, padx=20, sticky="se")

    def export_duplicate_serial_numbers_on_click(self):
        df_csv = pd.read_csv(self.PATH + '/modified.csv', index_col='pocmonitor_sn')
        sorted_dataframe = fd.find_duplicate_serial_numbers(df_csv)
        print(sorted_dataframe)
        return fh.write_to_excel_file(sorted_dataframe, self.PATH + '/duplicates.xlsx')

    # ============ Methods End ============ #
