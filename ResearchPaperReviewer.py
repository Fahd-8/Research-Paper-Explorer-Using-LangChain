from flask import Flask, request, jsonify, render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Function to get results from Arxiv API
def get_arxiv_results(query):
    arxiv_url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=10'
    
    try:
        response = requests.get(arxiv_url)
        response.raise_for_status()
        
        # Parse the XML response from Arxiv
        root = ET.fromstring(response.text)
        entries = []
        
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in entry.findall('{http://www.w3.org/2005/Atom}author')]
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            id = entry.find('{http://www.w3.org/2005/Atom}id').text
            
            entries.append({
                'title': title,
                'authors': authors,
                'published': published,
                'summary': summary,
                'id': id
            })
        
        return jsonify({'entries': entries})
    
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('ResearchPaper.html')

# New route for fetching Arxiv articles
@app.route('/arxiv', methods=['GET'])
def arxiv_search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    return get_arxiv_results(query)

if __name__ == '__main__':
    app.run(debug=True, port=50018)
