# AI Intelligence & Risk Advisor

An AI-powered platform that analyzes project documents to identify risks, blockers, project scope, project health, and documentation insights using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- **Document Upload:** Upload project documents for AI-powered analysis.
- **Scope & Deliverables:** Extract project scope, requirements, and deliverables.
- **Risk Analysis:** Identify and prioritize project risks based on severity.
- **Blocker Detection:** Highlight potential blockers and project dependencies.
- **Project Health Analysis:** Generate insights into overall project status.
- **AI Chatbot:** Ask questions about uploaded documents and receive contextual answers.
- **Documentation Generation:** Generate project documentation from analyzed content.
- **PDF Reports:** Download analysis results and documentation as PDF files.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Backend:** FastAPI
- **Frontend:** Streamlit
- **AI/LLM:** Large Language Models (LLMs)
- **Retrieval:** Retrieval-Augmented Generation (RAG)
- **API Communication:** REST APIs
- **Report Generation:** ReportLab

## 🏗️ Architecture

1. Upload project documents through the Streamlit interface.
2. Send documents to the FastAPI backend for processing.
3. Retrieve relevant document information using the RAG workflow.
4. Use LLM-powered agents to analyze project scope, risks, blockers, health, and documentation.
5. Display structured insights through the interface and allow users to download PDF reports.

## 📁 Project Structure

```text
AI-Intelligence-Risk-Advisor/
├── app.py                  # Streamlit frontend
├── main.py                 # FastAPI backend entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
└── ...                     # Other backend modules and configuration files
```

*Note: Update the project structure to match your actual repository.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Required API keys for the configured LLM provider

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Intelligence-Risk-Advisor
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the environment variables required by your backend.

```env
GROQ_API_KEY=your_api_key_here
```

Use the variable names expected by your actual backend configuration. Never commit API keys or other secrets to GitHub.

### 5. Start the FastAPI Backend

```bash
uvicorn main:app --reload --port 8000
```

The backend API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 6. Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 💡 Use Cases

- Analyze project requirements and deliverables.
- Identify potential risks and project blockers early.
- Review project status using uploaded documents.
- Ask contextual questions through an AI chatbot.
- Generate downloadable reports for project review.

## 🔐 Security

- Store API keys in environment variables.
- Exclude `.env` and other sensitive files from version control.
- Validate uploaded files before processing.
- Avoid uploading confidential documents to environments that are not authorized to process them.

## 🔮 Future Enhancements

- Real-time project monitoring and alerts.
- Risk trend analysis and visual dashboards.
- Support for additional document formats.
- Integration with project management tools.
- Enhanced reporting and collaboration features.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Lalit Aditya**

