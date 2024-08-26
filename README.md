# Book Metadata Processor

This project provides a Python-based tool for fetching, processing, and inserting book metadata into a Supabase database. It utilizes the OpenLibrary API to retrieve book details and manages the metadata in Supabase, a backend-as-a-service platform. This tool is particularly useful for managing and categorizing a large collection of books efficiently.

## Features

- **Fetch Book Data**: Retrieves metadata for books from the OpenLibrary API based on title and author.
- **Supabase Integration**: Inserts and manages book metadata within a Supabase database.
- **CSV File Processing**: Reads a CSV file containing book titles and authors, processes each entry, and updates the database accordingly.
- **Dynamic Author and Category Management**: Automatically checks for existing authors and adds new ones as needed. Assigns books to predefined categories.

## Requirements

- Python 3.x
- Supabase account and API keys
- `.env` file with the following variables:
  - `SUPABASE_URL`: Your Supabase project URL.
  - `SUPABASE_KEY`: Your Supabase API key.
- CSV file (`pdfs.csv`) containing book titles and authors in the following format:

  ```csv
  Title, Author
  The Great Gatsby, F. Scott Fitzgerald
  To Kill a Mockingbird, Harper Lee
  ```

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/book-metadata-processor.git
   cd book-metadata-processor
   ```

2. **Install Dependencies**:
   Install the required Python packages using pip:
   ```bash
   pip install requests python-dotenv supabase
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory of your project and add your Supabase URL and API key:
   ```env
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_supabase_key
   ```

4. **Prepare CSV File**:
   Ensure you have a CSV file named `pdfs.csv` in the root directory with the book titles and authors.

## Usage

Run the script to process the books listed in your CSV file and insert their metadata into the Supabase database:

```bash
python fetch_data.py
```

## Script Overview

The script performs the following tasks:

1. **Load Environment Variables**: Loads the Supabase URL and key from the `.env` file.
   
2. **Initialize Supabase Client**: Sets up the connection to the Supabase database using the provided credentials.

3. **Fetch Book Data**: Queries the OpenLibrary API to fetch book metadata based on the title and author provided.

4. **Map Data to Supabase Schema**: Transforms the fetched data to match the Supabase database schema.

5. **Insert Metadata into Supabase**: Adds the book metadata, author information, and category into their respective tables in the Supabase database.

6. **CSV Processing**: Reads book titles and authors from a CSV file and processes each entry to update the database.

## Functions

- `fetch_book_data(title, author)`: Fetches book data from the OpenLibrary API.
- `map_data_to_columns(api_data, book_uuid, author_id)`: Maps API data to the columns in the `books_metadata` table.
- `insert_book_metadata(supabase, mapped_data)`: Inserts the mapped book metadata into the Supabase `books_metadata` table.
- `get_author_id(supabase, author_name)`: Retrieves the ID of an author from the `authors` table.
- `insert_author(supabase, author_name)`: Inserts a new author into the `authors` table and returns their ID.
- `insert_book_author(supabase, book_id, author_id)`: Creates a relation between a book and its author in the `book_authors` table.
- `insert_book_category(supabase, book_id)`: Assigns a book to a predefined category in the `book_categories` table.
- `process_book(supabase, title, author)`: Processes a single book, including fetching data, mapping it, and inserting it into the database.
- `process_csv(supabase, csv_file)`: Reads and processes all books listed in a CSV file.
