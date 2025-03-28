# Diyanet İçerik Scraper

**Diyanet İçerik Scraper**, Diyanet'in dijital kitap koleksiyonlarından verileri çekip bir PostgreSQL veritabanına kaydeden bir Python uygulamasıdır. Bu proje, Diyanet'in e-kitap ve yayınlarını ("https://yayin.diyanet.gov.tr/Product/Index?&fileType=1") toplamak ve depolamak için kullanılabilir. 

## Proje Yapısı

Bu proje, iki ana bileşenden oluşmaktadır:

1. **PostgreSQL Veritabanı**: İçerik verilerini depolamak için kullanılan veritabanı.
2. **Python Scraper**: API'den verileri çeker, işler ve PostgreSQL veritabanına kaydeder.

Her iki bileşen de Docker konteynerlerinde çalışır ve Docker Compose kullanılarak yönetilir.

## Gereksinimler

- Docker
- Docker Compose
- Python 3.9 (Proje için kullanılan Python sürümü)
- PostgreSQL

## Kurulum ve Çalıştırma

### 1. **PostgreSQL Veritabanı Kurulumu**

1. **Docker Compose ile PostgreSQL konteynerini başlatın**:
    ```bash
    cd db
    docker compose up --build -d
    ```

   Bu komut, PostgreSQL veritabanı konteynerini başlatır ve `init.sql` dosyasındaki SQL komutları ile veritabanını oluşturur.

2. **Veritabanı bağlantı bilgilerini `.env` dosyasından düzenleyin**:
    - `POSTGRES_USER` — PostgreSQL kullanıcı adı
    - `POSTGRES_PASSWORD` — PostgreSQL şifresi
    - `POSTGRES_DB` — Veritabanı adı
    - `DB_PORT` — Dışa açılacak port (varsayılan `5432`)

   `.env` dosyasını açıp uygun değerleri girin.

### 2. **Python Scraper Kurulumu**

1. **Python scraper'ı çalıştırmak için Docker Compose ile başlatın**:
    ```bash
    cd scraper
    docker compose up --build -d
    ```

   Bu komut, Python scraper konteynerini başlatır ve verileri çekip PostgreSQL veritabanına kaydeder.

2. **Python scraper'ı için bağlantı bilgilerini `.env` dosyasından düzenleyin**:
    - `POSTGRES_USER` — PostgreSQL kullanıcı adı
    - `POSTGRES_PASSWORD` — PostgreSQL şifresi
    - `POSTGRES_DB` — Veritabanı adı
    - `DB_PORT` — PostgreSQL portu (kendi `.env` dosyanızdaki ayarlarla uyumlu olmalı)
    - `DB_HOST` — Host adı
    

   `.env` dosyasını açıp uygun değerleri girin.

### 3. **Veritabanı Yapılandırması**

PostgreSQL veritabanı için aşağıdaki tablo yapısı `init.sql` dosyasına eklenmiştir:

```sql
CREATE TABLE IF NOT EXISTS diyanet_icerik (             
    id SERIAL PRIMARY KEY,                                          -- Veritabanındaki artan id
    "icerikId" INT,                                                  -- Response'dan gelen id değeri burada kaydedilecek
    "name" TEXT,                                                     -- Product name
    "description" TEXT,                                              -- Product description
    "salesUrl" TEXT,                                                 -- Sales URL
    "releaseDate" DATE,                                              -- Release date
    "content" TEXT,                                                  -- Content of the product
    "isbn" TEXT,                                                     -- ISBN number
    "printNumber" TEXT,                                              -- Print number (if applicable)
    "publicationNumber" TEXT,                                        -- Publication number (if applicable)
    "thumbImagePath" TEXT,                                           -- Thumbnail image path
    "imagePath" TEXT,                                                -- Image path
    "author" TEXT[],                                                 -- Array of authors
    "uploadDate" TIMESTAMP WITH TIME ZONE,                           -- Upload date (if applicable)
    "language" TEXT,                                                 -- Language of the product
    "publisher" TEXT,                                                -- Publisher of the product
    "productTypeName" TEXT,                                          -- Product type name (e.g., e-book, etc.)
    "categoryName" TEXT,                                             -- Category name
    "categoryId" INT,                                                -- Category ID
    "authorIdList" TEXT[],                                           -- List of author IDs
    "ownLanguage" TEXT,                                              -- Own language of the product
    "categoryImagePath" TEXT,                                        -- Category image path
    "voicing" TEXT,                                                  -- Voicing (if applicable)
    "journalName" TEXT,                                              -- Journal name (if applicable)
    "audioBookPath" TEXT,                                            -- Audio book path (if applicable)
    "audioUrl" TEXT,                                                 -- Audio URL (if applicable)
    "downloadedDate" TIMESTAMP WITH TIME ZONE DEFAULT NULL,          -- Date when the content was downloaded
    "fileType" TEXT DEFAULT 'pdf',                                   -- File type (default: 'pdf')
    "downloadUrl" TEXT,                                              -- Generated download URL
    "update_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP   -- Timestamp when the record was last updated
);

CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    "categoryId" INT UNIQUE,
    "categoryName" TEXT
);

