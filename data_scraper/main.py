from pdf.scraper import process_pdf_urls as process_pdf_urls
# from goodreads.scraper import scrape_goodreads

def main():
    pdf_urls = [
        'https://www.research.autodesk.com/publications/#/page/1',
        'https://www.research.autodesk.com/publications/#/page/2'
        # Add more URLs as needed
    ]

    goodreads_urls = [
        'https://www.goodreads.com/list/show/1.Best_Books_Ever',
        # Add more URLs as needed
    ]

    print("Starting PDF scraping...")
    process_pdf_urls(pdf_urls)
    
    print("Starting Goodreads scraping...")
    scrape_goodreads(goodreads_urls)

if __name__ == "__main__":
    main()