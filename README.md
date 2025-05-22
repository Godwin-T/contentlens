# Interactive Blog with AI Chat

A modern blog platform that combines traditional reading with AI-powered chat interactions. Users can either read blog posts normally or engage in conversations with the content, demonstrating advanced prompt versioning and LLM monitoring capabilities.

## Features

- **Traditional Blog Reading**: Browse and read blog posts in a standard format
- **AI Chat Interface**: Chat with blog posts instead of reading them
- **Prompt Versioning**: Managed through PromptLayer for iterative prompt improvement
- **LLM Monitoring**: Comprehensive monitoring and analytics via Opik
- **Vector Search**: Powered by Qdrant for semantic content retrieval
- **RESTful API**: Built with FastAPI for robust backend services

## Architecture

### Core Components

- **Backend**: FastAPI for high-performance API endpoints
- **Vector Database**: Qdrant for semantic search and content retrieval
- **Prompt Management**: PromptLayer for version control and A/B testing
- **Monitoring**: Opik for LLM performance tracking and analytics
- **Deployment**: Docker containerization with manual deployment options

### Project Structure

```
├── .github/workflows/     # CI/CD workflows
├── backend.yaml          # Backend configuration
├── svc/                  # Service configurations
├── alembic/             # Database migrations
├── api/                 # API endpoints
    ├── core/                # Core application logic
    ├── models/              # Data models
    ├── routes/              # API route definitions
    ├── services/            # Business logic services
├── databases/           # Database configurations
├── tests/               # Test suites
└── dockerignore         # Docker ignore patterns
```

## 📚 API Endpoints

### Content Management
- **GET** `/health` - Health check endpoint
- **GET** `/retrieve` - Fetch blog posts
- **GET** `/retrieve/id` - Get specific post by ID
- **POST** `/add_blogpost` - Create new blog post

### AI-Powered Features
- **GET** `/search` - Semantic search through content/ Traditional text-based search
- **POST** `/chat` - Interactive chat with blog content

## 🛠️ Development Workflow

### Local Development

1. **Setup Environment**
   ```bash
   # Clone the repository
   git clone https://github.com/Godwin-T/contentlens.git
   cd content lens

   # Create new environment
   python3 -m venv venv
   source ./venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **Configure Servicee**
   - Set up Qdrant vector database
   - Configure PromptLayer API keys
   - Set up Opik monitoring credentials

3. **Run Development Server**
   ```bash
   uvicorn api.main:app --reload
   ```

### Prompt Development Process

1. **Local Testing**: Develop and test prompts locally
2. **Version Control**: Use the versioning script when satisfied
   ```bash
   python api/ai_core/version_prompt.py
   ```
3. **Deployment**: Deploy using Docker or manual methods

## 🐳 Deployment

### Docker Deployment (Recommended)

```bash
# Build the container
docker build -t blog-app .

# Run the container
docker run -p 8000:8000 blog-app
```

### Manual Deployment

1. **Prepare Environment**
   ```bash
   # Install production dependencies
 
   python3 -m venv venv
   source ./venv/bin/activate
   pip install -r requirements.txt
     
   # Set environment variables
   Create a .env file and add the credentials just like the one in the .env-example.sh
   ```

2. **Run Production Server**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 🔧 Configuration

### Environment Variables

```env
# Vector Database
QDRANT_URL=your_qdrant_instance_url
QDRANT_API_KEY=your_qdrant_api_key

# Prompt Management
PROMPTLAYER_API_KEY=your_promptlayer_key

# LLM Monitoring
OPIK_API_KEY=your_opik_api_key
OPIK_PROJECT_NAME=your_project_name

# Application Settings
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Database Setup

The project uses Alembic for database migrations:

```bash
# Initialize database
chmod +x prepare_db.sh
./prepare_db.sh
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

```

## 📊 Monitoring & Analytics

### PromptLayer Integration
- **Version Control**: Track prompt changes and performance
- **A/B Testing**: Compare different prompt versions
- **Analytics**: Monitor prompt effectiveness

### Opik Monitoring
- **Performance Metrics**: Track response times and accuracy
- **Cost Analysis**: Monitor LLM usage and costs
- **Error Tracking**: Identify and debug issues