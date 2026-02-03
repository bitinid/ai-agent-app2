from flask import Flask, request, jsonify, send_from_directory, send_file
import os
from dotenv import load_dotenv
import json
import requests
from flask_cors import CORS


load_dotenv()


app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
CORS(app)

class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.api_key = os.getenv("GROQ_API_KEY")

    def get_response(self, prompt):

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            data = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are {self.name}, {self.description}. Respond in a helpful, concise, and professional manner."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            }

            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"An error occurred: {str(e)}"

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            "ResearchAgent",
            "a research specialist who provides information about technologies, trends, and industry news"
        )

    def search_web(self, query):
        return self.get_response(f"Provide information about '{query}' as if you've just searched the web for the latest information. Include key points and insights.")

    def compare_technologies(self, tech1, tech2):
        return self.get_response(f"Compare {tech1} vs {tech2} in terms of features, performance, use cases, community support, and future prospects.")

    def get_industry_trends(self):
        return self.get_response("Describe current trends in software development and technology that are important for developers to be aware of.")


research_agent = ResearchAgent()


@app.route('/')
def serve_index():
    """Serve React index.html for SPA routing."""
    return send_file('frontend/dist/index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the React build directory."""
    file_path = os.path.join('frontend/dist', path)
    if os.path.isfile(file_path):
        return send_from_directory('frontend/dist', path)
    # For SPA, serve index.html for unknown routes
    return send_file('frontend/dist/index.html')


@app.route('/static/images/default_avatar.png')
@app.route('/static/images/default_project.jpg')
def block_default_images():

    response = app.make_response(
        b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
    response.headers['Content-Type'] = 'image/gif'

    response.headers['Cache-Control'] = 'public, max-age=31536000'
    response.headers['Expires'] = 'Thu, 31 Dec 2037 23:59:59 GMT'
    return response


@app.route('/api/research', methods=['POST'])
def research_agent_endpoint():
    data = request.json
    message = data.get('message', '')

    if 'compare' in message.lower() and ('vs' in message.lower() or 'versus' in message.lower()):

        tech_parts = message.lower().replace('compare', '').replace(
            'vs', ' ').replace('versus', ' ').split()
        tech1 = tech_parts[0] if len(tech_parts) > 0 else ''
        tech2 = tech_parts[-1] if len(tech_parts) > 1 else ''
        response = research_agent.compare_technologies(tech1, tech2)
    elif 'trends' in message.lower() or 'industry' in message.lower():
        response = research_agent.get_industry_trends()
    else:
        response = research_agent.search_web(message)

    return jsonify({'response': response})


if __name__ == '__main__':

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config['TEMPLATES_AUTO_RELOAD'] = True   # Ensure templates reload

    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
