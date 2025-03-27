import argparse
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os

class ImageUrlScraper:
    def __init__(self, api_key=None, user_agent=None):
        """
        Initialize the Image URL Scraper with optional custom user agent.
        
        :param api_key: Unsplash API key
        :param user_agent: Custom user agent string to use for requests
        """
        self.default_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.user_agent = user_agent or self.default_user_agent
        self.api_key = api_key or os.environ.get('UNSPLASH_API_KEY')

    def _fetch_unsplash_image_urls(self, search_term, num_images=5):
        """
        Fetch image URLs from Unsplash API.
        
        :param search_term: Search query string
        :param num_images: Number of image URLs to retrieve
        :return: List of image URLs
        """
        if not self.api_key:
            print("Error: Unsplash API key is required. Provide it with --api-key or set UNSPLASH_API_KEY environment variable.", file=sys.stderr)
            return []
            
        # Encode search term for URL
        encoded_term = urllib.parse.quote(search_term)
        url = f"https://api.unsplash.com/search/photos?query={encoded_term}&per_page={num_images}"
        
        # Setup headers with API key
        headers = {
            "Authorization": f"Client-ID {self.api_key}",
            "Accept-Version": "v1",
            "User-Agent": self.user_agent
        }
        
        try:
            # Send request to Unsplash API
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Extract image URLs
            image_links = []
            for result in data.get('results', []):
                image_links.append(result['urls']['regular'])
            
            return image_links
        
        except requests.RequestException as e:
            print(f"Error fetching images for '{search_term}': {e}", file=sys.stderr)
            return []
        except ValueError as e:
            print(f"Error parsing JSON response: {e}", file=sys.stderr)
            return []

    def _fetch_google_image_urls(self, search_term, num_images=5):
        """
        Scrape image URLs from Google Image search. (Legacy method)
        
        :param search_term: Search query string
        :param num_images: Number of image URLs to retrieve
        :return: List of image URLs
        """
        # Encode search term for URL
        encoded_term = urllib.parse.quote(search_term)
        url = f"https://www.google.com/search?q={encoded_term}&tbm=isch"
        
        # Setup headers to mimic browser request
        headers = {
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        try:
            # Send request to Google Images
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find image links
            image_links = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src and src.startswith(('http', 'https')) and len(image_links) < num_images:
                    image_links.append(src)
            
            return image_links
        
        except requests.RequestException as e:
            print(f"Error fetching images for '{search_term}': {e}", file=sys.stderr)
            return []

    def search_images(self, search_terms, images_per_term=5, output_file=None):
        """
        Search and collect image URLs for multiple search terms using Unsplash.
        
        :param search_terms: List of search terms
        :param images_per_term: Number of images to retrieve per search term
        :param output_file: Optional file to save image URLs
        :return: Dictionary of search terms and their image URLs
        """
        all_image_urls = {}
        
        # Validate inputs
        if not isinstance(search_terms, list):
            search_terms = [search_terms]
        
        # Search images for each term
        for term in search_terms:
            print(f"Searching images for: {term}")
            urls = self._fetch_unsplash_image_urls(term, images_per_term)
            
            # Print or output URLs
            print(f"\nResults for '{term}':")
            for i, url in enumerate(urls, 1):
                print(f"{i}. {url}")
            
            all_image_urls[term] = urls
            print("\n" + "-"*50 + "\n")
        
        # Save to file if output file is specified
        if output_file:
            self._save_image_urls(all_image_urls, output_file)
        
        return all_image_urls

    def _save_image_urls(self, image_urls, output_file):
        """
        Save image URLs to a text file.
        
        :param image_urls: Dictionary of search terms and their image URLs
        :param output_file: Output file path
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for term, urls in image_urls.items():
                    f.write(f"Search Term: {term}\n")
                    for url in urls:
                        f.write(f"{url}\n")
                    f.write("\n")
            
            print(f"\nImage URLs saved to {output_file}")
        
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)

    def download_images(self, image_urls, download_dir="downloaded_images"):
        """
        Download images from URLs to specified directory.
        
        :param image_urls: Dictionary of search terms and their image URLs
        :param download_dir: Directory to save downloaded images
        :return: Dictionary with terms and paths to downloaded images
        """
        downloaded_images = {}
        
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        for term, urls in image_urls.items():
            # Create term-specific directory
            term_dir = os.path.join(download_dir, term.replace(" ", "_"))
            os.makedirs(term_dir, exist_ok=True)
            
            downloaded_images[term] = []
            print(f"\nDownloading images for '{term}':")
            
            for i, url in enumerate(urls, 1):
                try:
                    # Download image
                    response = requests.get(url, headers={"User-Agent": self.user_agent})
                    response.raise_for_status()
                    
                    # Determine file extension from content type
                    content_type = response.headers.get('content-type', '').lower()
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'png' in content_type:
                        ext = 'png'
                    elif 'gif' in content_type:
                        ext = 'gif'
                    elif 'bmp' in content_type:
                        ext = 'bmp'
                    else:
                        ext = 'jpg'  # Default to jpg
                    
                    # Create filename
                    filename = f"{term.replace(' ', '_')}_{i}.{ext}"
                    filepath = os.path.join(term_dir, filename)
                    
                    # Save image
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"  ✓ Downloaded: {filename}")
                    downloaded_images[term].append(filepath)
                    
                except requests.RequestException as e:
                    print(f"  ✗ Error downloading image {i} for '{term}': {e}", file=sys.stderr)
                except IOError as e:
                    print(f"  ✗ Error saving image {i} for '{term}': {e}", file=sys.stderr)
        
        print(f"\nAll images downloaded to {os.path.abspath(download_dir)}")
        return downloaded_images

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(
        description="Search, retrieve, and optionally download images from Unsplash.",
        epilog="Example: python image_scraper.py 'cute cats' 'dogs' -n 5 -o images.txt -k your_api_key -d -p downloads"
    )
    
    # Positional argument for search terms
    parser.add_argument(
        'search_terms', 
        nargs='+', 
        help='One or more search terms in quotes'
    )
    
    # Optional arguments
    parser.add_argument(
        '-n', '--num-images', 
        type=int, 
        default=5, 
        help='Number of images to retrieve per search term (default: 5)'
    )
    
    parser.add_argument(
        '-o', '--output', 
        help='Output file to save image URLs (optional)'
    )
    
    parser.add_argument(
        '-k', '--api-key',
        help='Unsplash API key (can also be set as UNSPLASH_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '-d', '--download',
        action='store_true',
        help='Download the images'
    )
    
    parser.add_argument(
        '-p', '--path',
        default='downloaded_images',
        help='Directory to save downloaded images (default: downloaded_images)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create scraper and search
    scraper = ImageUrlScraper(api_key=args.api_key)
    image_urls = scraper.search_images(
        search_terms=args.search_terms, 
        images_per_term=args.num_images, 
        output_file=args.output
    )
    
    # Download images if requested
    if args.download:
        scraper.download_images(image_urls, download_dir=args.path)

if __name__ == "__main__":
    main()