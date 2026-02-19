#!/usr/bin/env python3
"""
Example usage of the Punjabi Crawler
"""

from app.services.crawler import PunjabiCrawler


def main():
    # Create an instance of the PunjabiCrawler
    crawler = PunjabiCrawler(delay=1.0, max_pages=10)
    
    print("Punjabi Web Crawler Example Usage")
    print("=" * 40)
    
    # Example 1: Check if text is in Punjabi
    test_texts = [
        "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਪੰਜਾਬੀ ਸੀਖਣ ਦੀ ਕੋਸ਼ਿਸ਼ ਕਰ ਰਹੀ ਹਾਂ।",  # Punjabi in Gurmukhi script
        "This is an English sentence.",  # English
        "Punjabi news website",  # English text mentioning Punjabi
        "ਪੰਜਾਬੀ ਗੀਤ ਸੁਣੋ",  # More Punjabi
        "Hello, how are you?"  # English
    ]
    
    print("\n1. Testing Punjabi Content Detection:")
    for text in test_texts:
        is_punjabi = crawler.is_punjabi_content(text)
        print(f"Text: '{text}' -> Is Punjabi: {is_punjabi}")
    
    # Example 2: Extract Punjabi content from HTML
    sample_html = """
    <html>
        <head><title>Sample Website</title></head>
        <body>
            <h1>ਸਤ ਸ੍ਰੀ ਅਕਾਲ World News</h1>
            <p>This is some English text.</p>
            <p>ਪੰਜਾਬੀ ਸਮਾਚਾਰ: ਅੱਜ ਦੀਆਂ ਤਾਜ਼ਾ ਖਬਰਾਂ</p>
            <a href="/news">ਪੰਜਾਬੀ ਖ਼ਬਰਾਂ</a>
            <a href="/english">English News</a>
            <img src="image.jpg" alt="ਪੰਜਾਬੀ ਲੋਕ ਗਾਇਕੀ">
        </body>
    </html>
    """
    
    print("\n2. Extracting Punjabi content from HTML:")
    punjabi_texts = crawler.search_punjabi_text_in_html(sample_html)
    for text in punjabi_texts:
        print(f"- {text}")
    
    # Example 3: Crawling a single URL (this would work with real URLs)
    print("\n3. Example of crawling a single URL:")
    print("crawler.crawl_single_url('https://example-punjabi-news.com')")
    print("# This would return structured data with Punjabi content if the site has any")
    
    # Example 4: Show the crawling capabilities
    print("\n4. Crawler Capabilities:")
    print(f"- Delays between requests: {crawler.delay} seconds")
    print(f"- Max pages to crawl: {crawler.max_pages}")
    print("- Detects Punjabi content using both script recognition and language detection")
    print("- Extracts headings, paragraphs, links, and image alt text")
    print("- Respects robots.txt by implementing delays")
    print("- Follows links to crawl deeper into websites")


if __name__ == "__main__":
    main()