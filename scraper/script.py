import requests
import psycopg2
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

load_dotenv()


turkey_timezone = pytz.timezone('Europe/Istanbul')


utc_timezone = pytz.timezone('UTC')

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"), 
        database=os.getenv("POSTGRES_DB"), 
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD") 
    )
    return conn


def fetch_pdf_data(page_number):
    url = "https://yayin.diyanet.gov.tr/Product/GetProduct"
    payload = {
        "PageNumber": page_number,
        "PageSize": 50,
        "FileType": "1",
        "Category": None,
        "Search": None,
        "ProductType": None
    }
    print(f"Attending to PDF URL: {url} for page {page_number}")
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Successfully fetched pdf data for page {page_number}")
        return response.json()
    else:
        print(f"Failed to fetch pdf data for page {page_number} with status code {response.status_code}")
    return []

def fetch_epub_data(page_number):
    url = "https://yayin.diyanet.gov.tr/Product/GetProduct"
    payload = {
        "PageNumber": page_number,
        "PageSize": 50,
        "FileType": "2",
        "Category": None,
        "Search": None,
        "ProductType": None
    }
    print(f"Attending to e-PUB URL: {url} for page {page_number}")
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"Successfully fetched e-PUB data for page {page_number}")
        return response.json()
    else:
        print(f"Failed to fetch e-PUB data for page {page_number} with status code {response.status_code}")
    return []

def generate_pdf_download_url(product_id):
    return f"https://yayin.diyanet.gov.tr/File/Download?path={product_id}_1.pdf&id={product_id}"

def generate_epub_download_url(product_id, product_name):
    return f"https://yayin.diyanet.gov.tr/File/EpubDownload?path={product_id}_2.epub&name={product_name}=&id={product_id}"

def convert_to_timezone(upload_date):
    if upload_date:

        if isinstance(upload_date, str):
            try:
                upload_date_obj = datetime.fromisoformat(upload_date) 
                upload_date_obj = turkey_timezone.localize(upload_date_obj) 
                return upload_date_obj
            except ValueError:
                return None
        else:
            return upload_date  
    else:
        return None  


def save_to_db(data, type):
    conn = get_db_connection()
    cursor = conn.cursor()

    for item in data:
        icerik_id = item['id']

        category_id = item.get('categoryId')
        category_name = item.get('categoryName')
        if category_id is not None and category_name is not None:
            cursor.execute('SELECT 1 FROM "category" WHERE "categoryId" = %s', (category_id,))
            if not cursor.fetchone():
                cursor.execute(
                    'INSERT INTO "category" ("categoryId", "categoryName") VALUES (%s, %s)',
                    (category_id, category_name)
                )

        if type == "pdf":
            download_url = generate_pdf_download_url(item['id'])
        elif type == "epub":
            download_url = generate_epub_download_url(item['id'], item['name'])
            print(f"e-PUB download_url: {download_url}") 

        item['author'] = item.get('author', [])
        item['authorIdList'] = item.get('authorIdList', []) 
        item['releaseDate'] = item.get('releaseDate', None)
        item['uploadDate'] = item.get('uploadDate', None)

        current_time = datetime.now(tz=utc_timezone) 
        upload_date = convert_to_timezone(item.get('uploadDate'))



        print(f"Processing icerikId: {icerik_id}") 

        cursor.execute('SELECT 1 FROM "diyanet_icerik" WHERE "icerikId" = %s', (icerik_id,))
        existing_record = cursor.fetchone()

        if existing_record:
            print(f"Already exists record with icerikId: {icerik_id}")
            cursor.execute(""" 
                SELECT "name", "description", "salesUrl", "releaseDate", "content", 
                       "isbn", "printNumber", "publicationNumber", "thumbImagePath", "imagePath", 
                       "author", "uploadDate", "language", "publisher", "productTypeName", 
                       "categoryName", "categoryId", "authorIdList", "ownLanguage", 
                       "categoryImagePath", "voicing", "journalName", "audioBookPath", 
                       "audioUrl", "fileType" 
                FROM "diyanet_icerik" 
                WHERE "icerikId" = %s
            """, (icerik_id,))
            existing_data = cursor.fetchone()

            if existing_data != (item['name'], item['description'], item['salesUrl'], item['releaseDate'],
                                 item['content'], item['isbn'], item['printNumber'], item['publicationNumber'],
                                 item['thumbImagePath'], item['imagePath'], item['author'], upload_date, item['language'],
                                 item['publisher'], item['productTypeName'], item['categoryName'], item['categoryId'],
                                 item['authorIdList'], item['ownLanguage'], item['categoryImagePath'], item['voicing'],
                                 item['journalName'], item['audioBookPath'], item['audioUrl'], type):

           
                print(f"Updating record with icerikId: {icerik_id}")
                print(f"Updated data: {item}") 

                try:
                    cursor.execute(""" 
                        UPDATE "diyanet_icerik" SET
                            "name" = %s, "description" = %s, "salesUrl" = %s, "releaseDate" = %s, "content" = %s,
                            "isbn" = %s, "printNumber" = %s, "publicationNumber" = %s, "thumbImagePath" = %s, "imagePath" = %s,
                            "author" = %s, "uploadDate" = %s, "language" = %s, "publisher" = %s, "productTypeName" = %s,
                            "categoryName" = %s, "categoryId" = %s, "authorIdList" = %s, "ownLanguage" = %s, 
                            "categoryImagePath" = %s, "voicing" = %s, "journalName" = %s, "audioBookPath" = %s, "audioUrl" = %s,
                            "fileType" = %s, "downloadUrl" = %s, "update_at" = %s
                        WHERE "icerikId" = %s
                    """, (
                        item['name'], item['description'], item['salesUrl'], item['releaseDate'], item['content'],
                        item['isbn'], item['printNumber'], item['publicationNumber'], item['thumbImagePath'], item['imagePath'],
                        item['author'], upload_date, item['language'], item['publisher'], item['productTypeName'],
                        item['categoryName'], item['categoryId'], item['authorIdList'], item['ownLanguage'],
                        item['categoryImagePath'], item['voicing'], item['journalName'], item['audioBookPath'],
                        item['audioUrl'], type, download_url, current_time, icerik_id
                    ))

                except Exception as e:
                    print(f"Error during update for icerikId {icerik_id}: {e}")

        else:
            print(f"Not exists record with icerikId: {icerik_id}")

            print(f"Inserting new record with icerikId: {icerik_id}")
            print(f"New data to insert: {item}")  

            try:
                cursor.execute(""" 
                    INSERT INTO "diyanet_icerik" (
                        "icerikId", "name", "description", "salesUrl", "releaseDate", "content", 
                        "isbn", "printNumber", "publicationNumber", "thumbImagePath", "imagePath", 
                        "author", "uploadDate", "language", "publisher", "productTypeName", 
                        "categoryName", "categoryId", "authorIdList", "ownLanguage", 
                        "categoryImagePath", "voicing", "journalName", "audioBookPath", "audioUrl", 
                        "downloadedDate", "fileType", "downloadUrl"
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    icerik_id, item['name'], item['description'], item['salesUrl'], 
                    item['releaseDate'], item['content'], item['isbn'], item['printNumber'], 
                    item['publicationNumber'], item['thumbImagePath'], item['imagePath'], 
                    item['author'], upload_date, item['language'], item['publisher'], 
                    item['productTypeName'], item['categoryName'], item['categoryId'], 
                    item['authorIdList'], item['ownLanguage'], item['categoryImagePath'], 
                    item['voicing'], item['journalName'], item['audioBookPath'], 
                    item['audioUrl'], None, type, download_url
                ))

            except Exception as e:
                print(f"Error during insert for icerikId {icerik_id}: {e}")

    conn.commit()
    cursor.close()
    conn.close()


def main():
    page_number = 1
    while True:
        data = fetch_pdf_data(page_number)
        if not data:
            print(f"Pdf data is finished last page taken: {page_number}")
            print(f"////////////////////////////////////////////////////////")
            print(f"////////////////////////////////////////////////////////")
            print(f"////////////////////////////////////////////////////////")
            break
        save_to_db(data, "pdf")
        print(f"Pdf data page saved: {page_number}")
        page_number += 1

    page_number = 1
    while True:
        data = fetch_epub_data(page_number)
        if not data:
            print(f"e-PUB data is finished last page taken: {page_number}")
            print(f"////////////////////////////////////////////////////////")
            print(f"////////////////////////////////////////////////////////")
            print(f"////////////////////////////////////////////////////////")
            break
        save_to_db(data, "epub")
        print(f"e-PUB data page saved: {page_number}")

        page_number += 1

if __name__ == '__main__':
    main()
