
# SQL Query Enhancement with LLM Pipeline

A sophisticated web application that uses advanced Large Language Model (LLM) pipelines to enhance and execute SQL queries. The system combines natural language processing with database operations to provide intelligent query enhancement capabilities.

## 🚀 Features

- **Natural Language to SQL**: Convert natural language queries to SQL
- **Query Enhancement**: Automatically improve and optimize SQL queries
- **Multi-Pipeline Processing**: Combines JOIN and WHERE clause processing pipelines
- **Interactive Web Interface**: Modern Streamlit-based UI
- **CSV Data Upload**: Easy data import and management
- **Real-time Results**: Instant query execution and result display
- **Execution Analytics**: Detailed metadata and performance metrics

## 🏗️ Architecture

The application consists of several key components:

### Backend Pipeline
- **Combined Pipeline** (`Main/combined_pipeline.py`): Main orchestration pipeline
- **Join Pipeline** (`Main/join_pipeline.py`): Handles complex JOIN operations
- **Row Calculus Pipeline** (`Main/row_calculus_pipeline.py`): Processes WHERE clauses
- **Utilities** (`Utilities/`): Database operations, LLM integration, and data processing

### Frontend
- **Streamlit App** (`app.py`): Modern web interface
- **Interactive Components**: File upload, query input, result visualization
- **Configuration Panel**: Pipeline settings and parameters

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Relational
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional but recommended):
   ```bash
   export GOOGLE_API_KEY="your_google_api_key"
   export OPENAI_API_KEY="your_openai_api_key"
   export ANTHROPIC_API_KEY="your_anthropic_api_key"
   ```

4. **Run the deployment script**:
   ```bash
   python deploy.py
   ```

### Manual Deployment

If you prefer manual setup:

```bash
# Install requirements
pip install -r requirements.txt

# Create necessary directories
mkdir -p Data saved_json saved_plots temporary

# Run the Streamlit app
streamlit run app.py
```

## 🎯 Usage

### 1. Upload Data
- Use the sidebar to upload CSV files
- Select appropriate delimiter (comma, semicolon, tab)
- Preview uploaded tables

### 2. Configure Pipeline
- **Similarity Threshold**: Adjust semantic matching sensitivity (0.0-1.0)
- **Two-Step Processing**: Enable for better accuracy (slower)
- **Auxiliary Pipeline**: Use alternative processing components

### 3. Input Queries
- **Natural Language**: Describe what you want to find
- **SQL Query**: Write direct SQL statements
- Examples:
  - Natural: "Show me all dogs from the animalowner table"
  - SQL: `SELECT * FROM animalowner WHERE category = 'dog'`

### 4. View Results
- Interactive data tables with zoom capability
- Download results as CSV
- View execution metadata and statistics

## 🔧 Configuration

### Pipeline Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Similarity Threshold | Controls semantic matching strictness | 0.7 |
| Two-Step Processing | Uses thorough but slower processing | True |
| Auxiliary Pipeline | Alternative processing components | False |

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key | No |
| `OPENAI_API_KEY` | OpenAI API key | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | No |

## 📊 Pipeline Process

1. **Query Analysis**: Detects WHERE and JOIN conditions
2. **Context Retrieval**: Gathers relevant database context
3. **LLM Enhancement**: Processes through combined pipeline
4. **Query Execution**: Executes enhanced query
5. **Result Processing**: Removes duplicates and formats results

## 🗂️ Project Structure

```
Relational/
├── app.py                 # Main Streamlit application
├── deploy.py             # Deployment script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── Main/                # Core pipeline modules
│   ├── combined_pipeline.py
│   ├── join_pipeline.py
│   ├── row_calculus_pipeline.py
│   └── ...
├── Utilities/           # Utility modules
│   ├── database.py
│   ├── llm.py
│   ├── extractor.py
│   └── ...
├── Data/               # Data storage
├── saved_json/         # JSON outputs
├── saved_plots/        # Generated plots
└── temporary/          # Temporary files
```

## 🚀 Deployment Options

### Local Development
```bash
python deploy.py --port 8501 --host localhost
```

### Production Deployment
```bash
python deploy.py --port 80 --host 0.0.0.0
```

### Docker Deployment (Future)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**: Check environment variables
   ```bash
   echo $GOOGLE_API_KEY
   ```

3. **Port Already in Use**: Change port
   ```bash
   python deploy.py --port 8502
   ```

4. **Memory Issues**: Reduce data size or use smaller datasets

### Debug Mode
```bash
streamlit run app.py --logger.level debug
```

## 📈 Performance

- **Query Processing**: Typically 2-10 seconds depending on complexity
- **Memory Usage**: Varies with dataset size
- **Concurrent Users**: Limited by Streamlit's single-threaded nature

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Streamlit for the web framework
- DuckDB for in-memory database operations
- Google AI, OpenAI, and Anthropic for LLM capabilities
- The open-source community for various dependencies

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Built with ❤️ using Streamlit and advanced LLM pipelines**
