
# LangChain Multi-Agent Research System

A powerful multi-agent research system built with LangChain and Ollama that autonomously researches topics, gathers information, writes comprehensive reports, and evaluates their quality using locally running AI models.

<p align="center">
  <strong>🔬 Research Automation • 🤖 Multi-Agent Orchestration • 📝 Intelligent Report Generation</strong>
</p>

---

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for searching, reading, writing, and critiquing
- **Automated Web Research**: Intelligent web search with Tavily API
- **Smart Content Extraction**: Advanced web scraping with multiple fallback strategies
- **AI-Powered Report Generation**: Automatically generates structured research reports using a local LLM
- **Quality Evaluation**: Built-in critic agent for report validation and scoring
- **Local LLM Integration**: Runs AI models locally using Ollama
- **Interactive UI**: Streamlit-based user interface for easy interaction
- **Pipeline Orchestration**: Seamless coordination of multiple agents

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────┐
│           Streamlit UI (app.py)                     │
│      Multi-Agent Research Assistant Interface       │
└──────────────────┬──────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────┐
│      Research Pipeline (pipeline.py)                │
│        Orchestrates multi-agent workflow            │
└──────────────────┬──────────────────────────────────┘
                   │
      ┌────────────┼──────────────┐
      │            │              │
  ┌───▼───┐   ┌────▼─────┐   ┌───▼────┐
  │Search │   │  Reader  │   │ Writer │
  │Agent  │   │  Agent   │   │ Chain  │
  └───┬───┘   └────┬─────┘   └───┬────┘
      │            │              │
      │  ┌─────────▼──────────┐   │
      └─▶│    Tools Layer     │◀──┘
         │                    │
         │ • web_search       │
         │ • scrape_url       │
         │                    │
         └────────┬───────────┘
                  │
             ┌────▼─────┐
             │  Critic  │
             │  Chain   │
             └──────────┘
```

### Agent Responsibilities

- **Search Agent**: Discovers relevant information across the web using Tavily
- **Reader Agent**: Extracts clean, readable content from URLs
- **Writer Chain**: Composes structured, professional research reports
- **Critic Chain**: Evaluates reports and provides improvement suggestions

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python** | Core programming language |
| **LangChain** | Multi-agent orchestration and chain management |
| **Ollama** | Runs local large language models |
| **Qwen 2.5:3b** | Local language model for agents and chains |
| **LangChain-Ollama** | Integration between LangChain and Ollama |
| **Streamlit** | Interactive web UI |
| **Tavily API** | Web search and information retrieval |
| **BeautifulSoup4** | HTML parsing and content extraction |
| **Trafilatura** | Web content extraction |
| **Readability-lxml** | Article content extraction |
| **Python-dotenv** | Environment configuration management |
| **Rich** | Terminal output formatting |

---

## 📋 Prerequisites

- Python 3.11 or higher
- [Ollama](https://ollama.com/) installed and running
- Tavily API Key
- Sufficient system resources to run the selected local LLM

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

### 2. Create Environment (Conda)

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
```

Or with venv:

```bash
python -m venv venv
```

Activate on Windows:

```powershell
venv\Scripts\activate
```

Activate on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Ollama

Download and install Ollama from:

https://ollama.com/

Pull the Qwen 2.5:3b model:

```bash
ollama pull qwen2.5:3b
```

Make sure Ollama is running before starting the application.

You can verify the model installation with:

```bash
ollama list
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your API key from:

- [Tavily API](https://tavily.com)

**Note:** No OpenAI API key is required. The language model runs locally through Ollama.

---

## 💡 Usage

### Run with Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

### Run as a Script

```bash
python main.py
```

Edit the `topic` variable in `main.py` to research different topics.

---

## 📁 Project Structure

```text
.
├── app.py                      # Streamlit web interface
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── LICENSE                     # License file
├── demo.excalidraw              # Architecture diagram
│
└── src/
    ├── __init__.py
    ├── agents/
    │   ├── __init__.py
    │   └── agents.py            # Search, Reader, Writer, Critic agents
    ├── tools/
    │   ├── __init__.py
    │   └── tools.py             # web_search, scrape_url tools
    └── pipelines/
        ├── __init__.py
        └── pipeline.py          # Main research orchestration
```

---

## 🔄 Workflow

1. **User Input**: Enter a research topic via UI or script.
2. **Search Phase**: Search agent queries the web using Tavily.
3. **Reading Phase**: Reader agent extracts content from relevant URLs.
4. **Writing Phase**: Writer chain synthesizes findings into a structured report using the local Ollama model.
5. **Review Phase**: Critic chain evaluates the report and provides scores.
6. **Output**: Display the final report with feedback and scores.

---

## 📊 Example Output

The system generates reports with:

- Comprehensive introduction and background
- Key findings with detailed explanations
- Well-sourced conclusions
- Structured sections and proper formatting
- Quality scores from 1-10

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Local LLM inference powered by [Ollama](https://ollama.com/)
- Web search powered by [Tavily](https://tavily.com/)
- UI built with [Streamlit](https://streamlit.io/)
- Inspired by agentic AI research patterns

---

## 📧 Support

For support, open an issue on GitHub or contact the maintainers.

**Happy Researching! 🚀**
