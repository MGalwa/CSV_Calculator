# Magdalena Galwa
# 19/09/2025
# Description:

# Homework:
    # Calculate number of words and letters from previous Homeworks 5/6 output test file.
    # Create two csv:
        # word-count (all words are preprocessed in lowercase)
        # letter, cout_all, count_uppercase, percentage (add header, spacecharacters are not included)
        # CSVs should be recreated each time new record added.
import re # Importing the Regex module to search for words in output file
import os  # Importing the os module for file and directory operations
import csv # Importing the CSV module to process csv files
from datetime import datetime  # Importing datetime module for working with dates and times


# Class GUI - responsible for displaying information and capturing the user's choice
class GUI:
    def __init__(self):
        # Display the opening menu and instructions at the start of the application
        self.show_menu_options()

    def show_menu_options(self):
        # Display the application's initial menu options
        self.display_message("=== News Feed Tool ===")  # Application header
        self.display_message("Choose one of the options:")  # Inform user of available menu options
        self.display_message("1 - News Feed")  # Option 1: News
        self.display_message("2 - Private Ad")  # Option 2: Private Ad
        self.display_message("3 - Book Review")  # Option 3: Book Review
        self.display_message("\nA default input file will be created in:")  # Show input file location
        self.display_message(r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\CSV_Calculator\input.txt")
        self.display_message("After filling the file, you can process it.")  # How to proceed with the app

    def display_message(self, message):
        # Centralized method to print messages to the console
        print(message)  # Print the given message in terminal

    def get_user_choice(self):
        # Get and validate the user's choice from the menu
        while True:  # Repeat until a valid choice is provided
            try:
                choice = int(input("Enter your choice (1, 2, 3): "))  # Prompt user to input a choice
                if choice in [1, 2, 3]:  # Check if the choice is valid (1, 2, or 3)
                    return choice  # Return the valid choice
                else:
                    self.display_message("Invalid choice. Please select 1, 2, or 3.")  # Handle invalid choices
            except ValueError:
                self.display_message("Invalid input. Please enter the number 1, 2, or 3.")  # Handle non-integer inputs


# Class User - represents the user and their selected category choice
class User:
    def __init__(self, gui):
        self.gui = gui  # Reference to the GUI instance for displaying messages
        self.choice = self.gui.get_user_choice()  # Store the user's menu choice (1, 2, or 3)


# Class for the News category
class News:
    def __init__(self, text, city):
        self.text = text  # The message body of the news
        self.city = city  # The city associated with the news
        self.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")  # Full timestamp for internal processing
        self.publication_date = datetime.now().strftime("%d/%m/%Y")  # Only date for output formatting

    def __str__(self):
        # Format the News record as a string for saving in the output file
        # Includes the text, city, and publication date in separate lines
        return f"News ------------------------\n{self.text}\n{self.city}\nPublished on: {self.publication_date}\n"


# Class for the Private Ad category
class AdPrivate:
    def __init__(self, text, expire_date):
        self.text = text  # The message body of the private ad
        self.expire_date = expire_date  # Expiration date entered by the user

    def __str__(self):
        # Calculate the number of days remaining until the expiration date
        days_left = (self.expire_date - datetime.now().date()).days
        # Format the Private Ad record for saving in the output file
        return f"Private Ad ------------------------\n{self.text}\nActual until: {self.expire_date}, {days_left} days left\n"


# Class for the Book Review category
class BookReview:
    def __init__(self, text, rate):
        self.text = text  # The message body of the book review
        self.rate = rate  # Rating for the book (1-5)
        self.publication_date = datetime.now().strftime("%d/%m/%Y")  # Current date for output formatting

    def __str__(self):
        # Format the Book Review record for saving in the output file
        return f"Book Review ------------------------\n{self.text}\nRate: {self.rate}/5\nPublished on: {self.publication_date}\n"


# Class FileProcessor - responsible for handling input and output files
class FileProcessor:

    def __init__(self):
        # Paths to the input and output files
        self.input_file_path = r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\CSV_Calculator\input.txt"
        self.output_file_path = "output.txt"  # The output file where records are saved

    def create_input_file(self, choice, gui):
        # Create an input file with an example based on the user's choice
        examples = {
            1: "Today it's raining. Take your umbrella.;Gliwice",  # Example for News
            2: "I want to sell a bike;2026-02-02",  # Example for Private Ad
            3: "This book is amazing. Excellent storytelling.;5"  # Example for Book Review
        }

        # Create the directory for the input file if it doesn't exist
        input_dir = os.path.dirname(self.input_file_path)
        os.makedirs(input_dir, exist_ok=True)  # Ensure the directory exists

        # If the input file doesn't already exist, create it with an example
        if not os.path.exists(self.input_file_path):
            with open(self.input_file_path, "w", encoding="utf-8") as file:
                file.write("# Add your records here.\n")  # Add a comment at the top of the file
                file.write(f"# Example for this category: {examples[choice]}\n")  # Add an example line
                gui.display_message(f"Input file '{self.input_file_path}' has been created. Please fill it with data.")  # Inform the user

    def normalize_text(self, text, capitalize_all_words=False):

        normalized_text = text.lower()  # Convert all text to lowercase
        result = ""  # Initialize an empty string for the normalized output
        capitalize_next = True  # Start by capitalizing the first character

        # Iterate through each character in the text
        for i, char in enumerate(normalized_text):
            if capitalize_next and char.isalpha():  # If flag is set and the character is alphabetic
                result += char.upper()
                capitalize_next = False  # Reset the flag
            else:
                result += char  # Otherwise, add the character as is

            # Check for sentence-ending punctuation
            if char in [".", "!", "?"]:  # If the character is one of the end-of-sentence markers
                capitalize_next = True  # Set the flag to capitalize the next non-space character

            # Handle capitalization after spaces (optional, if requested)
            elif capitalize_all_words and char == " ":
                capitalize_next = True

        return result  # Return the fully normalized text

    def read_and_validate_records(self, choice, gui):

        # Process and validate records from the input file
        records = []  # List to store validated records

        # Check if the input file exists
        if not os.path.exists(self.input_file_path):
            gui.display_message("Input file not found. Please ensure the file exists.")
            return None

        # Read all valid lines (skip empty lines and comments)
        with open(self.input_file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("#")]

        if not lines:  # If the file is empty, inform the user
            gui.display_message("Input file is empty. Please provide valid records.")
            return None

        for line in lines:  # Iterate through each line in the file
            try:
                parts = line.split(";")  # Split the line into components using `;`
                if choice == 1 and len(parts) == 2:  # News category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    city = self.normalize_text(parts[1], capitalize_all_words=True)  # Normalize the city name
                    records.append(News(text, city))
                elif choice == 2 and len(parts) == 2:  # Private Ad category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    expire_date = datetime.strptime(parts[1], "%Y-%m-%d").date()  # Validate expiration date
                    if expire_date <= datetime.now().date():  # Check if date is in the future
                        raise ValueError("Expiration date must be a future date.")
                    records.append(AdPrivate(text, expire_date))
                elif choice == 3 and len(parts) == 2:  # Book Review category
                    text = self.normalize_text(parts[0])  # Normalize the text body
                    rate = int(parts[1])  # Ensure the rate is a valid integer
                    if rate < 1 or rate > 5:  # Validate rating range (1-5)
                        raise ValueError("Rate must be between 1 and 5.")
                    records.append(BookReview(text, rate))
                else:
                    raise ValueError("Invalid format or missing fields.")
            except Exception as e:  # Handle any errors in processing
                gui.display_message(f"Error processing line '{line}': {e}")
                gui.display_message("Please correct the input file and try again.")
                return None

        return records  # Return the list of validated records

    def save_to_output_file(self, records, gui):

        # Save all validated records to the output file
        if not os.path.exists(self.output_file_path):
            # If the file doesn't exist, create it with a header
            with open(self.output_file_path, "w", encoding="utf-8") as file:
                file.write("News Feed App\n\n")

        # Append each record to the file
        with open(self.output_file_path, "a", encoding="utf-8") as file:
            for record in records:
                file.write(str(record) + "\n")  # Convert each record to a string and add it to the file
        gui.display_message(f"All records have been saved to '{self.output_file_path}'.")

    # Method to extract all the words from the output file and write them to a list
    def write_words_output_file(self):
        words_list = []  # Initialize an empty list to store the words extracted from the output file.

        try:
            # Open the output file for reading using UTF-8 encoding.
            with open(self.output_file_path, "r", encoding="utf-8") as file:
                # Iterate through each line in the file.
                for line in file:
                    # Use a regex pattern to match words (including those with apostrophes like "I'm", "can't").
                    words = re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", line)
                    # Convert words to lowercase and extend the `words_list`.
                    words_list.extend(
                        [word.lower() for word in words])  # Normalize all words to lowercase for consistency.
        except FileNotFoundError:
            # Handle the error if the output file is not found in the specified location.
            print(f"File named output.txt from this localization '{self.output_file_path}' was not found.")
        except Exception as error:
            # Handle any other error that occurs during file processing.
            print(f"There is an error: {error}")
        return words_list  # Return the list of extracted words.

    # Method to extract all letters from the output file and write them to a list
    def write_letters_output_file(self):
        letters_list = []  # Initialize an empty list to store the letters extracted from the output file.

        try:
            # Open the output file for reading using UTF-8 encoding.
            with open(self.output_file_path, "r", encoding="utf-8") as file:
                # Iterate through each line in the file.
                for line in file:
                    # Use a regex pattern to match individual letters (both uppercase and lowercase).
                    letters = re.findall(r"[a-zA-Z]", line)
                    # Extend the `letters_list` with the matches (letters remain case-sensitive for further analysis).
                    letters_list.extend(letters)
        except FileNotFoundError:
            # Handle the error if the output file is not found in the specified location.
            print(f"File named output.txt from this localization '{self.output_file_path}' was not found.")
        except Exception as error:
            # Handle any other error that occurs during file processing.
            print(f"There is an error: {error}")
        return letters_list  # Return the list of extracted letters.

    # Method to count occurrences of words from a given list
    def count_word_occurrences_from_list(self, words_list):
        word_count = {}  # Initialize an empty dictionary to store word counts.

        # Iterate through each word in the provided list of words.
        for word in words_list:
            if word in word_count:
                # If the word is already in the dictionary, increment its count by 1.
                word_count[word] += 1
            else:
                # If the word is not in the dictionary, add it with an initial count of 1.
                word_count[word] = 1

        return word_count  # Return the dictionary containing word occurrences.

    # Method to count occurrences of letters (both total and uppercase) from a given list
    def count_letters_occurrences_from_list(self, letters_list):
        letters_count = {}  # Initialize an empty dictionary to store lowercase letter counts.
        uppercase_count = {}  # Initialize an empty dictionary to store uppercase letter counts.

        # Calculate the total number of letters for percentage calculations.
        total_letters = len(letters_list)

        # Iterate through each letter in the provided list of letters.
        for letter in letters_list:
            # Convert the letter to lowercase for counting total occurrences.
            letter_lower = letter.lower()
            # Add to the total count for lowercase letters.
            letters_count[letter_lower] = letters_count.get(letter_lower, 0) + 1

            # Check if the letter is uppercase for specific uppercase counts.
            if letter.isupper():
                uppercase_count[letter] = uppercase_count.get(letter, 0) + 1

        # Return lowercase counts, uppercase counts, and the total number of letters.
        return letters_count, uppercase_count, total_letters


    # Method to remove the input file after processing is complete
    def remove_input_file(self, gui):
        try:
            os.remove(self.input_file_path)  # Remove the input file from the directory.
            # Notify the user that the input file has been deleted successfully.
            gui.display_message(f"Input file '{self.input_file_path}' has been successfully deleted.")
        except Exception as e:
            # Handle any errors that occur during the deletion process.
            gui.display_message(f"Error deleting the input file: {e}")


 # Helper function to calculate statistics for letters
def calculate_letter_statistics(letters_list):

    letters_count = {}  # Dictionary to hold total count of each letter (lowercase).
    uppercase_count = {}  # Dictionary to hold uppercase counts of each letter.
    total_letters = len(letters_list)  # Total number of letters for percentage calculations.

     # Iterate through each letter in the list and gather stats.
    for letter in letters_list:
        # Convert to lowercase to handle total occurrences (case-insensitive).
        letter_lower = letter.lower()
        letters_count[letter_lower] = letters_count.get(letter_lower, 0) + 1

        # If the letter is uppercase, increment its uppercase count.
        if letter.isupper():
            uppercase_count[letter] = uppercase_count.get(letter, 0) + 1

    # Create a result table with combined statistics for each letter.
    letter_stats = {}
    for letter, count in letters_count.items():
         # Get uppercase occurrences, default to 0 if unavailable.
        upper_count = uppercase_count.get(letter.upper(), 0)
        # Calculate the percentage of the letter relative to total letters.
        percentage = (count / total_letters) * 100
        # Store all statistics in a dictionary keyed by the letter.
        letter_stats[letter] = {
            'count_all': count,
            'count_uppercase': upper_count,
            'percentage': percentage
        }

    return letter_stats  # Return the consolidated letter statistics dictionary.

# Class CSVProcessor handles the creation and updating of CSV files for word and letter statistics.
class CSVProcessor:
    def __init__(self, file_processor):
        # Paths to the CSV files for word and letter statistics.
        self.csv1_file_path = r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\CSV_Calculator\csv_1.txt"  # File path for word statistics.
        self.csv2_file_path = r"C:\Users\MagdalenaGalwa\Desktop\Nauka\Python\Python_Projects\CSV_Calculator\csv_2.txt"  # File path for letter statistics.
        self.file_processor = file_processor  # Instance of FileProcessor to extract data from the output file.

    # Method to create or update the first CSV file (word statistics).
    def create_or_update_csv1_file(self):

        try:
            # Extract the list of lowercase words from the output file using FileProcessor.
            words_list = self.file_processor.write_words_output_file()

            # Check if there are any valid words in the output file.
            if not words_list:  # If no words are found, print a message and exit the function.
                print("Output file is empty or contains no valid words. CSV file will not be created or updated.")
                return  # Stop processing if the word list is empty.

            # Count occurrences of words using FileProcessor.
            word_occurrences = self.file_processor.count_word_occurrences_from_list(words_list)

            # Write the word occurrences to the CSV file.
            with open(self.csv1_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)  # Initialize the CSV writer.
                # Iterate through the dictionary and write each word and its count as rows in the CSV file.
                for word, count in word_occurrences.items():
                    csv_writer.writerow([word, count])  # Write the word and its count to the file.

            # Inform the user that the CSV file has been successfully updated.
            print(f"CSV file '{self.csv1_file_path}' has been updated with word occurrences.")

        except Exception as e:
            # Handle errors during file processing and print the exception message.
            print(f"Error during CSV file processing: {e}")

    def create_or_update_csv2_file(self):

        try:
            letters_list = self.file_processor.write_letters_output_file()  # Extract letters

            if not letters_list:  # No letters found
                print("Output file is empty or contains no valid letters. CSV file will not be created or updated.")
                return

            # Directly call the global `calculate_letter_statistics` function
            letter_stats = calculate_letter_statistics(letters_list)

            # Write to the CSV
            with open(self.csv2_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(['Letter', 'Count_All', 'Count_Uppercase', 'Percentage'])  # Write header
                for letter, stats in letter_stats.items():
                    csv_writer.writerow([
                        letter, stats['count_all'], stats['count_uppercase'], f"{stats['percentage']:.2f}%"
                    ])
            print(f"CSV file '{self.csv2_file_path}' has been updated with letter occurrence statistics.")
        except Exception as e:
            print(f"Error during CSV file processing: {e}")

# Main execution logic - entry point of the script.
if __name__ == "__main__":
    # Create an instance of GUI to display messages to the user.
    gui = GUI()

    # Get the user's choice of record category (News, Private Ad, or Book Review).
    user = User(gui)  # Store the selected category in the User object.

    # Initialize FileProcessor to handle reading, validating, and saving files.
    processor = FileProcessor()

    # Create an input file based on the user's selected category and display an example.
    processor.create_input_file(user.choice, gui)

    # Instantiate CSVProcessor, linking it to the FileProcessor instance.
    csv_processor = CSVProcessor(processor)

    # Run a loop to allow the user to choose processing actions until they decide to exit.
    while True:
        # Prompt user for processing or exiting options.
        gui.display_message("\nType '1' to process the input file after filling it.")  # Option 1: Process file.
        gui.display_message("Type '2' to exit the application.")  # Option 2: Exit the application.

        # Capture the user's choice and remove extra spaces.
        user_action = input("Your choice: ").strip()

        # Check if the user chose to process the input file.
        if user_action == "1":
            # Read and validate records based on user's category choice.
            records = processor.read_and_validate_records(user.choice, gui)

            # Proceed if valid records are retrieved.
            if records:
                processor.save_to_output_file(records, gui)  # Save validated records to the output file.
                processor.remove_input_file(gui)  # Remove the processed input file.

                # Create or update the word and letter statistics CSVs.
                csv_processor.create_or_update_csv1_file()  # Process and update word statistics.
                csv_processor.create_or_update_csv2_file()  # Process and update letter statistics.

                # Inform the user that processing is complete and exit the application.
                gui.display_message("Processing completed. Exiting the application.")
                break  # Exit the loop.

            else:
                # If records are invalid or missing, ask the user to fix the input file.
                gui.display_message("No valid records found. Please fix the input file.")
        elif user_action == "2":
            # If the user chose to exit the application, display a message and break the loop.
            gui.display_message("Exiting application.")
            break
        else:
            # Handle invalid inputs from the user and prompt them to try again.
            gui.display_message("Invalid input. Please enter '1' or '2'.")