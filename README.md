# Portia FastAPI Example

A well-structured FastAPI application integrated with the Portia SDK for building agentic workflows. This project demonstrates FastAPI best practices including proper async handling, Pydantic settings management, and clean architecture.

## Features

- 🚀 **FastAPI** with async support and modern Python features
- 🔧 **Portia SDK** integration for agentic workflows
- ⚙️ **Pydantic Settings** for configuration management
- 📊 **Structured logging** with configurable levels
- 🔍 **Health checks** and monitoring endpoints
- 📚 **Auto-generated OpenAPI documentation**
- 🐳 **Production-ready** with proper error handling and Docker support
- ⚡ **UV** for fast dependency management and project tooling
- 🧵 **Threaded execution** for non-blocking Portia SDK operations
- 🐳 **Docker Compose** with Redis caching support

## Project Structure

```
portia-python-fastapi-example/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application setup
│   ├── config.py               # Pydantic settings and configuration
│   ├── exceptions.py           # Custom exceptions
│   ├── api/
│   │   ├── __init__.py
│   │   ├── health.py           # Health check endpoints
│   │   └── run.py              # Main API endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── health.py           # Health check schemas
│   │   └── run.py              # Run endpoint schemas
│   └── services/
│       ├── __init__.py
│       └── portia_service.py   # Portia SDK integration
├── pyproject.toml              # Project configuration
├── README.md
└── LICENSE
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd portia-python-fastapi-example
   ```

2. **Install [UV](https://docs.astral.sh/uv/) (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

## Environment Setup

1. **Set up environment variables:**
   Create a `.env` file in the root directory with at least one api key:
   ```env
   # LLM Settings (at least one is required)
   PORTIA_CONFIG__OPENAI_API_KEY="your-openai-api-key"
   PORTIA_CONFIG__ANTHROPIC_API_KEY="your-anthropic-api-key"
   PORTIA_CONFIG__PORTIA_API_KEY="your-portia-api-key"
   ```

## Usage

### Running the Application
This will start the FastAPI server locally in dev mode.

```bash
uv run fastapi dev main.py
```

### Using Docker

#### Option 1: Docker Compose (Recommended)

1. **Create environment configuration:**
   Create a `.env` file in the project root with your API keys:
   ```env
   # =============================================================================
   # LLM API Keys (At least one is required)
   # =============================================================================

   # OpenAI API Key
   OPENAI_API_KEY=your-openai-api-key-here

   # Anthropic API Key
   ANTHROPIC_API_KEY=your-anthropic-api-key-here

   # MistralAI API Key
   MISTRALAI_API_KEY=your-mistralai-api-key-here

   # Google Generative AI API Key
   GOOGLE_API_KEY=your-google-api-key-here

   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

   # Portia API Key (optional)
   PORTIA_API_KEY=your-portia-api-key-here

   # =============================================================================
   # Application Configuration (Optional)
   # =============================================================================

   # Server Configuration
   HOST=127.0.0.1
   PORT=8000
   MAX_WORKERS=4

   # Portia Configuration
   PORTIA_CONFIG__LLM_PROVIDER=openai
   PORTIA_CONFIG__DEFAULT_MODEL=openai/gpt-4o
   PORTIA_CONFIG__STORAGE_CLASS=MEMORY
   ```

2. **Run with Docker Compose:**
   ```bash
   # Run the main application
   docker compose up -d

   # Run with Redis cache (optional)
   docker compose --profile cache up -d

   # View logs
   docker compose logs -f portia-api

   # Stop services
   docker compose down
   ```

3. **Access the application:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Redis (if enabled): localhost:6379

#### Option 2: Docker Build and Run

1. **Build the docker image:**
    ```bash
    docker build -t portia-fastapi-example .
    ```

2. **Run the docker image:**
    ```bash
    docker run -p 8000:8000 \
      -e PORTIA_CONFIG__OPENAI_API_KEY="your-openai-key" \
      -e DEBUG="false" \
      portia-fastapi-example
    ```

#### Docker Environment Variables

The Docker setup supports all configuration options via environment variables:

| Environment Variable | Default | Description                                      |
| -------------------- | ------- | ------------------------------------------------ |
| `HOST`               | 0.0.0.0 | Server host                                      |
| `PORT`               | 8000    | Server port                                      |
| `DEBUG`              | false   | Debug mode                                       |
| `LOG_LEVEL`          | INFO    | Logging level                                    |
| `MAX_WORKERS`        | 4       | Thread pool size for Portia execution            |
| `ALLOWED_DOMAINS`    | *       | CORS allowed domains                             |
| `PORTIA_CONFIG__*`   |         | Portia configuration (see Portia Config section) |

#### Production Deployment

For production, consider:

1. **Enable Redis caching:**
   ```bash
   docker compose --profile cache up -d
   ```
   Then set: `PORTIA_CONFIG__LLM_REDIS_CACHE_URL=redis://redis:6379`

2. **Adjust worker threads based on your load:**
   ```env
   MAX_WORKERS=8  # Increase for higher concurrency
   ```

3. **Use proper logging:**
   ```env
   LOG_LEVEL=INFO
   PORTIA_CONFIG__JSON_LOG_SERIALIZE=true
   ```

### API Documentation

Once the application is running, you can access:

- **Interactive Swagger UI API docs**: http://localhost:8000/docs
- **API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### GET /

Welcome endpoint that returns basic application information.

**Response:**
```json
{
  "message": "Welcome to Portia FastAPI Example",
  "version": "0.1.0",
  "docs_url": "/docs"
}
```

### POST /run

Execute a query using the Portia SDK.

**Request:**
```json
{
  "query": "What is 2+2?",
  "tools": ["calculator_tool"]
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "value": "4.0",
    "summary": "The query asked for the result of 2+2, and the expression was evaluated to give the output 4.0."
  },
  "error": null,
  "execution_time": 2.5
}
```

### GET /tools

Get available tools from the Portia SDK.

**Response:**
```json
["calculator_tool", "search_tool", "weather_tool"]
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Configuration

The application uses Pydantic Settings for configuration management. Settings can be configured via:

1. **Environment variables**
2. **`.env` file**
3. **Default values**

### Available Settings

| Setting                            | Default                  | Description                           |
| ---------------------------------- | ------------------------ | ------------------------------------- |
| `APP_NAME`                         | "Portia FastAPI Example" | Application name                      |
| `APPLICATION_VERSION`              | "0.1.0"                  | Application version                   |
| `DEBUG`                            | `false`                  | Debug mode                            |
| `HOST`                             | "127.0.0.1"              | Server host                           |
| `PORT`                             | 8000                     | Server port                           |
| `MAX_WORKERS`                      | 4                        | Thread pool size for Portia execution |
| `ALLOWED_DOMAINS`                  | `["*"]`                  | CORS allowed domains                  |
| `PORTIA_CONFIG__PORTIA_API_KEY`    | `None`                   | Portia API key (optional)             |
| `PORTIA_CONFIG__OPENAI_API_KEY`    | `None`                   | OpenAI API key                        |
| `PORTIA_CONFIG__ANTHROPIC_API_KEY` | `None`                   | Anthropic API key                     |
| `LOG_LEVEL`                        | "INFO"                   | Logging level                         |

## Performance & Concurrency

This application includes several performance optimizations:

### **Threaded Portia Execution**
Portia SDK operations run in a dedicated thread pool to prevent blocking the FastAPI event loop:

```python
# Configured via MAX_WORKERS environment variable (default: 4)
loop = asyncio.get_running_loop()
plan_run = await loop.run_in_executor(
    self._executor, portia_instance.run, query, tools
)
```

### **Benefits:**
- ✅ **Non-blocking**: FastAPI can handle other requests while Portia runs
- ✅ **Configurable concurrency**: Adjust `MAX_WORKERS` based on your needs
- ✅ **Better resource utilization**: Prevents thread starvation
- ✅ **Scalable**: Maintains responsiveness under load

### **LLM Response Caching**
Optional Redis integration for caching LLM responses:

```bash
# Enable Redis caching
docker compose --profile cache up -d
```

Set `PORTIA_CONFIG__LLM_REDIS_CACHE_URL=redis://redis:6379` to enable caching.

## Development

### Architecture

The application follows a clean architecture pattern:

- **API Layer** (`app/api/`): FastAPI route handlers
- **Service Layer** (`app/services/`): Business logic and external integrations
- **Schema Layer** (`app/schemas/`): Pydantic models for request/response validation
- **Configuration** (`app/config.py`): Application settings management
- **Exception Handling** (`app/exceptions.py`): Custom exceptions

### Running Tests

```bash
# Install dev dependencies (included with uv sync)
uv sync --group dev

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app
```

### Code Quality

This project uses `ruff` for linting and formatting:

```bash
# Run linting
uv run ruff check .

# Run formatting
uv run ruff format .
```

### CI/CD

This project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) for testing in the CI pipeline as well.

The workflow is triggered on:
- Push to `main` branch
- Pull requests to `main` branch

To run the same checks locally:

```bash
# Run all CI checks
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/ -v

# Run tests with coverage
uv run pytest tests/ --cov=app --cov-report=term-missing
```

### Adding New Endpoints

1. Create schemas in `app/schemas/`
2. Add business logic in `app/services/`
3. Create API routes in `app/api/`
4. Include the router in `app/main.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Portia SDK Documentation](https://docs.portialabs.ai/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/usage/settings/)