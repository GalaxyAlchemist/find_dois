import requests
import time

def get_doi(title):
    url = "https://api.crossref.org/works"
    params = {
        "query.title": title,
        "rows": 1
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['message']['items']:
                return data['message']['items'][0]['DOI']
        return None
    except Exception as e:
        print(f"Error fetching DOI for {title}: {str(e)}")
        return None

def main():
   try:
        with open('dois.txt', 'r', encoding='utf-8') as f:
            existing_dois = [line.split('\t')[0] for line in f.readlines()]
    except FileNotFoundError:
        existing_dois = []

  
    try:
        with open('ref_titles.txt', 'r', encoding='utf-8') as f:
            titles = [t.strip() for t in f.readlines() if t.strip()]
    except FileNotFoundError:
        print("Error: ref_titles.txt file not found.")
        return

    with open('dois.txt', 'a', encoding='utf-8') as f:
        for title in titles:
            if title in existing_dois:
                print(f"Skipping already processed title: {title}")
                continue

            try:
                doi = get_doi(title)
                if doi:
                    f.write(f"{doi}\n")
                else:
                    f.write(f"{title}\tDOI not found\n")
                f.flush() 
                print(f"Processed: {title}")
                time.sleep(1)
            except Exception as e:
                print(f"Error processing {title}: {str(e)}")
                continue

if __name__ == "__main__":
    main()
