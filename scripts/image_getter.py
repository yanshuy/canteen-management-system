import requests
import argparse
import sys

# --- Configuration ---
# !! REPLACE WITH YOUR ACTUAL API KEY AND CUSTOM SEARCH ENGINE ID !!
GOOGLE_API_KEY = "AIzaSyByXx-oq85SjGS69rJw47KN8AbLXztqvdM"
GOOGLE_CSE_ID = "f7d7b7fb8db0845bb"
# ---------------------

Google_Search_URL = "https://www.googleapis.com/customsearch/v1"

def search_google_images(api_key, cx_id, query, num_results=1):
    """Searches Google Images using the Custom Search API."""
    params = {
        'key': api_key,
        'cx': cx_id,
        'q': query,
        'searchType': 'image',  # This is crucial for image search
        'num': num_results      # Number of results per query (max 10 per request)
        # You can add 'start' parameter for pagination if you need more than 10
    }

    try:
        response = requests.get(Google_Search_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        search_results = response.json()

        image_urls = []
        # The 'items' key contains the search results
        if 'items' in search_results:
            for item in search_results['items']:
                # The 'link' is usually the direct URL to the image
                image_urls.append(item.get('link'))
        return image_urls

    except requests.exceptions.RequestException as e:
        print(f"Error making API request for '{query}': {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred for '{query}': {e}", file=sys.stderr)
        return None

def main():
    parser = argparse.ArgumentParser(description="Fetch image URLs for multiple search terms using Google Custom Search API.")
    parser.add_argument("terms", help="Comma-separated search terms (e.g., 'pancake,idli,pizza')")
    parser.add_argument("output_file", help="File to save the image URLs to")
    parser.add_argument("--num", type=int, default=10, help="Number of image results per term (max 10 per API request)")

    args = parser.parse_args()

    # Ensure API key and CX ID are set
    if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY" or GOOGLE_CSE_ID == "YOUR_GOOGLE_CSE_ID":
        print("Error: Please replace 'YOUR_GOOGLE_API_KEY' and 'YOUR_GOOGLE_CSE_ID' in the script with your actual credentials.", file=sys.stderr)
        sys.exit(1)

    search_terms = [term.strip() for term in args.terms.split(',') if term.strip()]
    output_filename = args.output_file
    num_results_per_term = args.num

    if not search_terms:
        print("No valid search terms provided.", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching images for terms: {', '.join(search_terms)}")

    with open(output_filename, 'w', encoding='utf-8') as f:
        for term in search_terms:
            print(f"Searching for: {term}...", file=sys.stderr)
            image_urls = search_google_images(
                GOOGLE_API_KEY,
                GOOGLE_CSE_ID,
                term,
                num_results=num_results_per_term
            )

            f.write(f"--- Images for: {term} ---\n\n")
            if image_urls is not None: # Check if API call was successful
                if image_urls:
                    for url in image_urls:
                        if url: # Ensure URL is not None/empty
                           f.write(f"{url}\n")
                else:
                    f.write("No image results found.\n")
            else:
                 f.write("Could not retrieve results due to an API error.\n")

            f.write("\n\n") # Add some spacing between terms

    print(f"\nImage URLs saved to {output_filename}")

if __name__ == "__main__":
    main()