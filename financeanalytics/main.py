from tkinter import Tk, Button, Entry, Frame, Label, ttk
from tkinter.filedialog import askdirectory

from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor

from pathlib import Path

import pandas as pd

class FinanceAnalytics:

    def determine_statement_type(self, pdf_filepath):
        """Identifies chequing or visa statement based on filepath (directory or file name)"""
        if 'chequing' in str(pdf_filepath).lower():
            return 'Chequing'
        elif 'visa' in str(pdf_filepath).lower():
            return 'Visa'
        else:
            raise NameError('Filepath does not specify chequing or visa statement type explicitly, please include')

    def extract_statement_data(self, df_record):
        """Extract the transactions from the statement"""
        pdf_filepath = df_record["Filepath"]
        bank = df_record["Bank"]
        statement_type = self.determine_statement_type(pdf_filepath)
        return StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

    def extract_all_statements(self, structured_data):
        """Loops through all statements in the dataframe to extract transactions"""
        total_records = structured_data.shape[0]
        column_names = list(structured_data.columns)

        df_all_statements = []

        # Set the GUI progress bar
        self.progress_bar["maximum"] = structured_data.shape[0]
        files_processed = 0

        # Iteratively process financial statements
        for index, row in structured_data.iterrows():
            pdf_filepath = row["Filepath"]
            bank = row["Bank"]
            statement_type = self.determine_statement_type(pdf_filepath)

            statement_df = StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

            # Append the hierarchy onto the results
            statement_df[column_names] = row.values

            # Add the statement with hierarchy to the complete dataset
            df_all_statements.append(statement_df)

            # Update the progress bar
            files_processed += 1
            self.progress_bar["value"] = files_processed
            self.progress_bar.update()


        # Merge statements into one dataframe
        return pd.concat(df_all_statements, axis=0).reset_index(drop=True)

    def write_output_to_location(self, all_statements):
        """Outputs the structured transaction data to the users designated output location"""
        output_path = Path(self.output_dir + '/extracted_transactions.xlsx')
        all_statements.to_excel(output_path, index=False)

    def get_directory(self):
        """User specifies the root folder location containing all subfolders and financial statements"""
        self.root_dir = askdirectory(title="Choose Root Folder for Financial Statement Processing")
        self.label_root_folder.config(text="Root Folder: {}".format(self.root_dir))

        # Output directory by default is the same as the root directory
        self.output_dir = self.root_dir
        self.label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(self.root_dir))

        # Enable output directory choosing and processing functions once input location determined
        self.button_choose_out.config(state="normal")
        self.button_run.config(state="normal")

        # Update status note so user knows how to proceed
        self.status_label.config(text="Either change the output location for the Excel document or choose to run the program")

    def get_output(self):
        """User specifies output location for the extracted transaction data"""
        self.output_dir = askdirectory(title="Choose Output Folder for Storing Processed Results")
        self.label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(self.output_dir))

        # Update status note so user knows how to proceed
        self.status_label.config(text="Run the program if the locations are correct")

    def run_processing(self):
        """Invokes the different stages of processing to coordinate all modules in extracting data"""
        # Update status note
        self.status_label.config(text="Processing financial statements, please wait...")

        # Load the data
        structured_data = DataLoader().load_data(self.root_dir)

        # Run the DQ analysis
        DataQuality().analyze_data_quality(structured_data)

        # Extract the statements and write
        self.write_output_to_location(self.extract_all_statements(structured_data))

        # Update status note
        self.status_label.config(text="Processing complete!")

    def _ui_frame_setup(self):
        """Set up the high level frames in the user interface"""
        # Set up frames for organizing the front end
        app_width = 600
        self.titleframe = Frame(self.root, width=app_width)
        self.statusframe = Frame(self.root, width=app_width)
        self.parametersframe = Frame(self.root, width=app_width)
        self.startstopframe = Frame(self.root, width=app_width)
        self.notesframe = Frame(self.root, width=app_width)

        # Organize frame positions
        self.titleframe.grid(row=0, column=0)
        self.statusframe.grid(row=1, column=0)
        self.parametersframe.grid(row=2, column=0, sticky="w")
        self.notesframe.grid(row=3, column=0)
        self.startstopframe.grid(row=4, column=0)

    def _ui_title_setup(self):
        """Sets up the title frame components"""
        # Initialize Title Frame
        self.title_label = Label(self.titleframe, text="Finance Analytics Application", font=("Arial", 18))

        # Place Title Widgets
        self.title_label.grid(row=0, column=0)

    def _ui_status_setup(self):
        """Sets up the status frame components used to direct/guide the user through the application"""
        # Initialize Status Frame
        self.status_label = Label(self.statusframe, width=100, text="Begin by selecting the root folder location for processing")

        # Place Status Widgets
        self.status_label.grid(row=0, column=0)

    def _ui_parameter_setup(self):
        """Sets up the parameter components the user will interact with to specify processing parameters"""
        # Initialize Parameters Widgets
        self.button_choose_root = Button(self.parametersframe, text="Choose Root Folder", command=self.get_directory, padx=20)
        self.button_choose_out = Button(self.parametersframe, text="Choose Output Location", command=self.get_output, state="disabled", padx=7)
        self.label_root_folder = Label(self.parametersframe, text="Root Folder: ")
        self.label_output_location = Label(self.parametersframe, text="Output Location: ")

        # Place Parameters Widgets
        self.button_choose_root.grid(row=0, column=0)
        self.button_choose_out.grid(row=1, column=0)
        self.label_root_folder.grid(row=0, column=2, sticky="w")
        self.label_output_location.grid(row=1, column=2, sticky="w")

    def _ui_startstop_setup(self):
        """Sets up the components for the user to run the processing and exit the program, including the status bar"""
        # Initialize Start Stop widgets
        self.button_run = Button(self.startstopframe, text="Run", command=self.run_processing, state="disabled", padx=15)
        self.button_quit = Button(self.startstopframe, text="Quit", command=self.root.quit, padx=13)
        self.progress_bar = ttk.Progressbar(self.startstopframe, orient="horizontal", length=200, mode="determinate")

        # Place Start Stop Widgets
        self.button_run.grid(row=0, column=0)
        self.progress_bar.grid(row=0, column=1)
        self.button_quit.grid(row=0, column=2)

    def toggle_show_supported_statements(self):
        """Toggles between showing all the supported financial statements and hiding on the GUI"""
        if self.show_supported_banks == False:
            self.notes_label.grid(row=1, column=0)
            self.expand_retract_supported_banks.config(text="Hide Supported Financial Statements")
            self.show_supported_banks = True
        else:
            self.notes_label.grid_remove()
            self.expand_retract_supported_banks.config(text="Show Supported Financial Statements")
            self.show_supported_banks = False


    def _ui_notes_setup(self):
        """Sets up the notes section of the application to provide build-specific info and other static information"""
        # Initialize Notes Widgets
        self.notes_label = Label(self.notesframe, text="RBC Chequing\nRBC Visa")
        self.expand_retract_supported_banks = Button(self.notesframe, text="Show Supported Financial Statements", command=self.toggle_show_supported_statements)
        self.show_supported_banks = False

        # Place Notes Widgets
        self.expand_retract_supported_banks.grid(row=0, column=0)

    def initialize_ui(self):
        """Initializes all the components of the user interface"""
        self.root = Tk()
        self.root.title("Finance Analytics")

        self._ui_frame_setup()
        self._ui_title_setup()
        self._ui_status_setup()
        self._ui_parameter_setup()
        self._ui_notes_setup()
        self._ui_startstop_setup()

        # Stop window resizing
        self.root.resizable(False, False)

        # Run main loop
        self.root.mainloop()

    def __init__(self):
        self.initialize_ui()

if __name__ == "__main__":
    FinanceAnalytics()