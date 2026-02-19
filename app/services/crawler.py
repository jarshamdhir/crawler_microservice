import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langdetect import detect
import re
import time
from typing import List, Dict, Optional


class PunjabiCrawler:
    """
    A web crawler specifically designed to crawl Punjabi content from websites.
    """
    
    def __init__(self, delay: float = 1.0, max_pages: int = 100):
        """
        Initialize the crawler with configuration.
        
        Args:
            delay: Delay between requests in seconds to be respectful to servers
            max_pages: Maximum number of pages to crawl
        """
        self.delay = delay
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common Punjabi text patterns and keywords to help identify Punjabi content
        self.punjabi_patterns = [
            r'[ਅ-ਊਏਐਓਔਕ-ਊਖ-ਊਗ-ਊਘ-ਊਚ-ਊਛ-ਊਜ-ਊਝ-ਊਟ-ਊਠ-ਊਡ-ਊਢ-ਊਣ-ਊਤ-ਊਥ-ਊਦ-ਊਧ-ਊਨ-ਊਪ-ਊਫ-ਊਬ-ਊਭ-ਊਮ-ਊਯ-ਊਰ-ਊਲ-ਊਵ-ਊਸ਼-ਊਸ-ਊਹ-ਊ਼-ਊਾ-ਊਿ-ਊੀ-ਊੁ-ਊੂ-ਊ੃-ਊੇ-ਊੈ-ਊੋ-ਊੌ-ਊ੍-ਊੰ-ਊੱ-ਊੲ-ਊੳ-ਊੴ]',
            r'punjabi',
            r'ਪੰਜਾਬੀ',
            r'gurmukhi',
            r'gurumukhi'
        ]
        
    def is_punjabi_content(self, text: str) -> bool:
        """
        Check if the given text is in Punjabi.
        
        Args:
            text: Text to check
            
        Returns:
            True if the text is likely in Punjabi, False otherwise
        """
        if not text.strip():
            return False
            
        # Check for Gurmukhi script characters (Punjabi script)
        gurmukhi_chars = (
            '\u0A00-\u0A7F'  # Complete Gurmukhi Unicode block
        )
        gurmukhi_pattern = re.compile(f'[{gurmukhi_chars}]')
        if gurmukhi_pattern.search(text):
            return True
            
        # If there's no Gurmukhi script, try language detection on English text
        # that might mention Punjabi content
        try:
            # Look for Punjabi-related keywords in English text
            lower_text = text.lower()
            for pattern in self.punjabi_patterns[1:]:  # Skip the Gurmukhi pattern
                if re.search(pattern, lower_text, re.IGNORECASE):
                    return True
                    
            # Try to detect language if there's enough text
            if len(text.split()) > 3:  # Only detect if we have meaningful text
                detected_lang = detect(text)
                return detected_lang == 'pa'  # 'pa' is the ISO code for Punjabi
        except:
            pass  # If language detection fails, continue with other checks
            
        return False
    
    def extract_punjabi_content(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Extract Punjabi content from a BeautifulSoup object.
        
        Args:
            soup: BeautifulSoup object representing HTML page
            
        Returns:
            Dictionary containing different types of Punjabi content
        """
        content = {
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images_alt': [],
            'all_text': []
        }
        
        # Extract headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = heading.get_text(strip=True)
            if self.is_punjabi_content(text):
                content['headings'].append(text)
                
        # Extract paragraphs
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if self.is_punjabi_content(text):
                content['paragraphs'].append(text)
                
        # Extract links with Punjabi text
        for link in soup.find_all('a', href=True):
            link_text = link.get_text(strip=True)
            if self.is_punjabi_content(link_text):
                content['links'].append({
                    'text': link_text,
                    'url': urljoin(soup.base.get('href', ''), link['href']) if soup.base else link['href']
                })
                
        # Extract image alt texts
        for img in soup.find_all('img', alt=True):
            alt_text = img.get('alt', '').strip()
            if self.is_punjabi_content(alt_text):
                content['images_alt'].append({
                    'alt': alt_text,
                    'src': img.get('src', '')
                })
                
        # Extract all text blocks
        for element in soup.find_all(text=True):
            if element.parent.name not in ['script', 'style', 'head', 'title', 'meta']:
                text = element.strip()
                if self.is_punjabi_content(text):
                    content['all_text'].append(text)
                    
        return content
    
    def get_page_content(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if failed
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Try to detect encoding
            encoding = response.apparent_encoding
            response.encoding = encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def crawl_single_url(self, url: str) -> Dict[str, any]:
        """
        Crawl a single URL and extract Punjabi content.
        
        Args:
            url: URL to crawl
            
        Returns:
            Dictionary containing crawled Punjabi content
        """
        soup = self.get_page_content(url)
        if not soup:
            return {'error': f'Failed to fetch {url}', 'content': {}}
            
        content = self.extract_punjabi_content(soup)
        
        return {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'content': content
        }
    
    def crawl_website(self, base_url: str, max_depth: int = 1) -> List[Dict[str, any]]:
        """
        Crawl a website recursively to find Punjabi content.
        
        Args:
            base_url: Base URL of the website to crawl
            max_depth: Maximum depth to crawl
            
        Returns:
            List of dictionaries containing crawled Punjabi content
        """
        visited_urls = set()
        urls_to_visit = [(base_url, 0)]  # (url, depth)
        results = []
        
        while urls_to_visit and len(results) < self.max_pages:
            current_url, depth = urls_to_visit.pop(0)
            
            if current_url in visited_urls or depth > max_depth:
                continue
                
            visited_urls.add(current_url)
            print(f"Crawling: {current_url} (depth: {depth})")
            
            soup = self.get_page_content(current_url)
            if not soup:
                continue
                
            # Extract Punjabi content
            content = self.extract_punjabi_content(soup)
            
            # Add to results if we found any Punjabi content
            total_content_items = sum(len(content[key]) for key in content if isinstance(content[key], list))
            if total_content_items > 0:
                results.append({
                    'url': current_url,
                    'title': soup.title.string if soup.title else '',
                    'content': content,
                    'depth': depth
                })
                
            # Find more URLs to crawl if we haven't reached max depth
            if depth < max_depth:
                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    absolute_url = urljoin(current_url, href)
                    
                    # Only add URLs from the same domain
                    if urlparse(absolute_url).netloc == urlparse(base_url).netloc:
                        if absolute_url not in visited_urls:
                            urls_to_visit.append((absolute_url, depth + 1))
                            
            # Be respectful to the server
            time.sleep(self.delay)
            
        return results
    
    def search_punjabi_text_in_html(self, html_content: str) -> List[str]:
        """
        Search for Punjabi text directly in HTML content string.
        
        Args:
            html_content: HTML content as string
            
        Returns:
            List of Punjabi text found
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        all_text = []
        
        for element in soup.find_all(text=True):
            if element.parent.name not in ['script', 'style', 'head', 'title', 'meta']:
                text = element.strip()
                if self.is_punjabi_content(text):
                    all_text.append(text)
                    
        return all_text