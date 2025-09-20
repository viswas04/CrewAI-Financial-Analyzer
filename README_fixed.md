# Financial Document Analyzer - AI Internship Debug Assignment

## What This Project Is About

This project is an AI-powered system designed to analyze financial documents like corporate reports and balance sheets. It uses a group of specialized AI agents working together to dig into your financial PDFs and give you insightful investment recommendations and risk assessments — all powered by advanced language models and CrewAI.


## Getting Started

### Quick Setup: Install Required Libraries

Just run:

```bash
pip install -r requirements.txt


### Setting Up Your Environment

Create a `.env` file in the project folder and add your API keys like this:


OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here


### Using Sample Financial Documents

The system is ready to analyze real-world documents like Tesla’s Q2 2025 financial update.

To test it out:

1. Download Tesla’s Q2 2025 report [here](https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf).
2. Save it as `data/sample.pdf` inside your project folder.
3. Or upload **any** PDF through the API endpoint for analysis.

Note: The current `data/sample.pdf` is just a placeholder; replace it with actual financial reports for meaningful results.


## Running The Application

Start the FastAPI server simply by running in your terminal:

```bash
python main.py
```

Once the server is up, head to [http://localhost:8000](http://localhost:8000) to see that it is running.


## API Overview

- **Health Check**
  - `GET /`
  - Quick check to make sure your API is live and ready.
- **Analyze Document**
  - `POST /analyze`
  - Upload a PDF file and submit your query.
  - Query is optional — defaults to analyzing investment insights.
  
### Example Request (Python)

```python
import requests

with open('financial_report.pdf', 'rb') as f:
    files = {'file': f}
    data = {'query': 'What are the key revenue trends?'}
    response = requests.post('http://localhost:8000/analyze', files=files, data=data)
    print(response.json())
```


## Bugs We Fixed

During development, several important bugs were spotted and resolved, including:

1. Syntax issues like missing parentheses and braces.
2. Import paths that were incorrect.
3. Circular references causing runtime errors.
4. Confusing parameter names fixed.
5. Better method signatures and decorators.
6. Missing and incorrect library dependencies.
7. And more…

In addition, we rewrote AI agent instructions and task descriptions to be professional, clear, and measurable for dependable financial advice.


## How It Works - Architecture

1. Upload PDF reports through the API.
2. The file is saved temporarily and read using PDF tools.
3. AI agents analyze the document according to your question.
4. Results are compiled into a neat, actionable report.
5. Temporary files are deleted after processing.


## Features At A Glance

- Upload and analyze financial PDFs
- AI-powered investment insights and risk assessments
- Detailed market trend evaluation
- Professional and compliant financial advice


## Future Directions

We suggest integrating:

- **Queue Workers:** Enable multiple requests with Redis and Celery.
- **Database Storage:** Save analysis results with PostgreSQL.
- **Containerized Deployment:** Use Docker for easy setup and scaling.


## Testing

Manual and automated test cases ensure reliability and easy maintenance.


## Contributing

Feel free to fork, improve, and send back your contributions with tests and documentation.


## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

For educational use during the AI Internship.

