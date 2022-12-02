from tkinter import Tk, Button, Entry, Frame, Label, ttk
from tkinter.filedialog import askdirectory

from financeanalytics.dataloader import DataLoader
from financeanalytics.dataquality import DataQuality
from financeanalytics.statementprocessor import StatementProcessor

from pathlib import Path

import pandas as pd

class FinanceAnalytics:

    def determine_statement_type(self, pdf_filepath):
        if 'chequing' in str(pdf_filepath).lower():
            return 'Chequing'
        elif 'visa' in str(pdf_filepath).lower():
            return 'Visa'
        else:
            raise NameError('Filepath does not specify chequing or visa statement type explicitly, please include')

    def extract_statement_data(self, df_record):

        pdf_filepath = df_record["Filepath"]
        bank = df_record["Bank"]
        statement_type = self.determine_statement_type(pdf_filepath)
        return StatementProcessor().extract_with_validation(pdf_filepath, bank, statement_type)

    def extract_all_statements(self, structured_data):
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
        output_path = Path(self.output_dir + '/extracted_transactions.xlsx')
        all_statements.to_excel(output_path, index=False)

    def get_directory(self):
        self.root_dir = askdirectory(title="Choose Root Folder for Financial Statement Processing")
        self.label_root_folder.config(text="Root Folder: {}".format(self.root_dir))

        # Output directory by default is the same as the root directory
        self.output_dir = self.root_dir
        self.label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(self.root_dir))

        # Enable output directory choosing and processing functions once input location determined
        self.button_choose_out.config(state="normal")
        self.button_run.config(state="normal")

    def get_output(self):
        self.output_dir = askdirectory(title="Choose Output Folder for Storing Processed Results")
        self.label_output_location.config(text="Output Location: {}/extracted_transactions.xlsx".format(self.output_dir))

    def run_processing(self):
        # Load the data
        structured_data = DataLoader().load_data(self.root_dir)

        # Run the DQ analysis
        DataQuality().analyze_data_quality(structured_data)

        # Extract the statements and write
        self.write_output_to_location(self.extract_all_statements(structured_data))

    def __init__(self):
        self.root = Tk()
        self.root.title("Finance Analytics")
        self.root.iconbitmap("../assets/icons/finance_analytics_logo.ico")

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
        self.startstopframe.grid(row=3, column=0)
        self.notesframe.grid(row=4, column=0, sticky="w")

        # Initialize Title Frame
        self.title_label = Label(self.titleframe, text="Finance Analytics Application", font=("Arial", 18))

        # Initialize Status Frame
        self.status_entry = Label(self.statusframe, width=100, text="Begin by selecting the root folder location for processing")

        # Initialize Parameters Widgets
        self.button_choose_root = Button(self.parametersframe, text="Choose Root Folder", command=self.get_directory, padx=20)
        self.button_choose_out = Button(self.parametersframe, text="Choose Output Location", command=self.get_output, state="disabled", padx=7)
        self.label_root_folder = Label(self.parametersframe, text="Root Folder: ")
        self.label_output_location = Label(self.parametersframe, text="Output Location: ")

        # Initialize Start Stop widgets
        self.button_run = Button(self.startstopframe, text="Run", command=self.run_processing, state="disabled", padx=15)
        self.button_quit = Button(self.startstopframe, text="Quit", command=self.root.quit, padx=13)
        self.progress_bar = ttk.Progressbar(self.startstopframe, orient="horizontal", length=200, mode="determinate")

        # Initialize Notes Widgets
        self.notes_label = Label(self.notesframe, text="Supported Financial Statements:\nRBC Chequing\nRBC Visa")

        # Place Title Widgets
        self.title_label.grid(row=0, column=0)

        # Place Status Widgets
        self.status_entry.grid(row=0, column=0)

        # Place Parameters Widgets
        self.button_choose_root.grid(row=0, column=0)
        self.button_choose_out.grid(row=1, column=0)
        self.label_root_folder.grid(row=0, column=2, sticky="w")
        self.label_output_location.grid(row=1, column=2, sticky="w")

        # Place Start Stop Widgets
        self.button_run.grid(row=0, column=0)
        self.progress_bar.grid(row=0, column=1)
        self.button_quit.grid(row=0, column=2)

        # Place Notes Widgets
        self.notes_label.grid(row=0, column=0)

        # Stop window resizing
        self.root.resizable(False, False)

        # Run main loop
        self.root.mainloop()

if __name__ == "__main__":
    FinanceAnalytics()