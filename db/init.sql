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
