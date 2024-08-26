import requests
import csv
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Supabase URL and key from environment variables
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)


def fetch_book_data(title, author):
    response = requests.get(f'http://openlibrary.org/search.json?title={title}&author={author}')
    if response.status_code == 200:
        data = response.json()
        if data['docs']:
            return data['docs'][0]  # Return the first result
    return None

def map_data_to_columns(api_data, book_uuid, author_id):
    return {
        'id': str(book_uuid),
        'title': api_data.get('title', ''),
        'description': api_data.get('first_sentence', '')[0] if api_data.get('first_sentence', '') else '',
        'ai_description': '',
        'cover_path': f"http://covers.openlibrary.org/b/id/{api_data.get('cover_i', '')}-L.jpg" if api_data.get('cover_i') else None,
        'language': api_data.get('language', [''])[0] if 'language' in api_data else None,
        'original_url': f"http://openlibrary.org{api_data.get('key')}",
        'page_count': api_data.get('number_of_pages_median', 0),
        'chapter_count': 0,
        'word_count': 0,
        'rating': 0.0,
        'created_at': 'now()',
        'updated_at': 'now()',
        'main_author_id': author_id,
        'is_public_domain': False,
    }

def insert_book_metadata(supabase, mapped_data):
    return supabase.table('books_metadata').insert(mapped_data).execute()

def get_author_id(supabase, author_name):
    response = supabase.table('authors').select('id').eq('name', author_name).execute()
    if response.data:
        return response.data[0]['id']
    return None

def insert_author(supabase, author_name):
    author_uuid = str(uuid.uuid4())
    supabase.table('authors').insert({'id': author_uuid, 'name': author_name}).execute()
    return author_uuid

def insert_book_author(supabase, book_id, author_id):
    supabase.table('book_authors').insert({'book_id': book_id, 'author_id': author_id}).execute()

def insert_book_category(supabase, book_id):
    category_id = "f7985ed7-f1ae-4dae-a7d7-b7340a1a174b"
    supabase.table('book_categories').insert({'book_id': book_id, 'category_id': category_id}).execute()

def process_book(supabase, title, author):
    # Generate a unique UUID for the book
    book_uuid = uuid.uuid4()

    # Fetch book data from OpenLibrary API
    book_data = fetch_book_data(title, author)
    if not book_data:
        print(f"No data found for {title} by {author}")
        return
    
    # Check if author exists in the authors table
    author_id = get_author_id(supabase, author)
    if not author_id:
        author_id = insert_author(supabase, author)
        print(f"Inserted new author {author}")

    # Map the data to the columns of books_metadata
    mapped_data = map_data_to_columns(book_data, book_uuid, author_id)

    # Insert book metadata
    insert_book_metadata(supabase, mapped_data)
    print(f"Inserted book metadata for {title}")

    # Insert into book_authors table
    insert_book_author(supabase, str(book_uuid), author_id)
    print(f"Inserted book-author relation for {title} by {author}")

    # Insert into book_categories table
    insert_book_category(supabase, str(book_uuid))
    print(f"Inserted book category for {title}")

def process_csv(supabase, csv_file):
    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row['Title']
            author = row['Author'].split(',')[0].strip()  # Take the first author and strip any surrounding whitespace

            process_book(supabase, title, author)

if __name__ == "__main__":
    process_csv(supabase, 'pdfs.csv')