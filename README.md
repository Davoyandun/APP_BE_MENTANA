# APP_BE_MENTANA

Backend API built with FastAPI and hexagonal architecture, designed to work with AWS cloud services.

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Architecture](#️-architecture)
- [Technologies](#-technologies)
- [Installation and Configuration](#️-installation-and-configuration)
- [API Usage](#-api-usage)
- [Testing](#-testing)
- [Execution Scripts](#-execution-scripts)
- [Logging](#-logging)
- [Development](#-development)
- [Deployment](#-deployment)
- [Security](#-security)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Support](#-support)

## ⚡ Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd APP_BE_MENTANA

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your AWS credentials

# Run the application
python run.py dev

# Access the API
curl http://localhost:8000/health
```

## 🏗️ Architecture

This project follows the principles of **Hexagonal Architecture** (also known as Ports and Adapters Architecture):

```
┌─────────────────────────────────────────────────────────────┐
│                        API Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Controllers   │  │     DTOs        │  │  Routers    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    Entities     │  │   Use Cases     │  │ Repositories│ │
│  │                 │  │                 │  │ (Interfaces)│ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Adapters Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ AWS DynamoDB    │  │   AWS S3        │  │   Other     │ │
│  │ Repository      │  │   Service       │  │  Adapters   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
APP_BE_MENTANA/
├── api/                    # API Layer (input adapters)
│   └── src/
│       ├── dtos/          # Data Transfer Objects
│       ├── exceptions/    # API Exceptions
│       └── routers/       # FastAPI Controllers
├── domain/                # Domain Layer (business core)
│   └── src/
│       ├── entities/      # Domain Entities
│       ├── repositories/  # Repository Interfaces
│       └── use_cases/     # Use Cases
├── adapters/              # Adapters Layer (implementations)
│   ├── repositories/      # Repository Implementations
│   └── services/          # External Services (AWS, etc.)
├── factories/             # Factories for dependency injection
│   ├── repository_factory.py    # Repository instances
│   ├── service_factory.py       # Service instances
│   ├── use_case_factory.py      # Use case instances
│   └── user_factory.py          # User entity creation
├── config.py             # Application configuration
├── main.py               # FastAPI entry point
├── requirements.txt      # Python dependencies
├── run.py                # Execution script
└── env.example           # Environment variables example
```

## 🚀 Technologies

- **FastAPI**: Modern and fast web framework for APIs
- **Python 3.11**: Programming language
- **AWS SDK (boto3)**: AWS services integration
- **DynamoDB**: Main NoSQL database
- **S3**: File storage
- **Redis**: Cache and sessions (optional)
- **Pydantic**: Data validation
- **Structlog**: Structured logging

## 🛠️ Installation and Configuration

### Prerequisites

- Python 3.11+
- AWS credentials configured
- AWS CLI (optional, for configuration)

### Local Configuration

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd APP_BE_MENTANA
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configurations
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Or use the execution script**
   ```bash
   python run.py dev
   ```

### Virtual Environment Management

#### Creating a new virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

#### Deactivating virtual environment
```bash
deactivate
```

#### Updating dependencies
```bash
# Activate virtual environment first
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Install/update dependencies
pip install -r requirements.txt

# Generate new requirements.txt (if needed)
pip freeze > requirements.txt
```

#### Using different Python versions
```bash
# Create virtual environment with specific Python version
python3.11 -m venv venv

# Or use pyenv (if installed)
pyenv local 3.11.0
python -m venv venv
```

### AWS Configuration

1. **Configure AWS credentials**
   ```bash
   aws configure
   ```

2. **Create required AWS resources**
   - DynamoDB Table
   - S3 Bucket
   - IAM Roles and policies

3. **Update environment variables**
   ```env
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   AWS_DYNAMODB_TABLE=your-table-name
   AWS_S3_BUCKET=your-bucket-name
   ```

### Local Development with DynamoDB

For local development, you can use DynamoDB local:

1. **Start DynamoDB local**
   ```bash
   docker run -p 8000:8000 amazon/dynamodb-local
   ```

2. **Configure for local development**
   ```env
   AWS_ENDPOINT_URL=http://localhost:8000
   AWS_DYNAMODB_TABLE=users
   ```

3. **Setup local table**
   ```bash
   python scripts/setup_dynamodb_local.py
   ```

## 📚 API Usage

### API Documentation

Once the application is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI schema**: `http://localhost:8000/openapi.json`

### Available Endpoints

#### Health Checks
- `GET /health` - Basic health check
- `GET /api/v1/health` - Detailed health check
- `GET /api/v1/health/ready` - Readiness check
- `GET /api/v1/health/live` - Liveness check

#### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users` - List all users

#### Test Endpoints (Development)
- `GET /api/v1/test/health` - Comprehensive health check with AWS services
- `POST /api/v1/test/user` - Test user creation with hexagonal architecture demo
- `GET /api/v1/test/users` - Test user retrieval with repository pattern demo
- `POST /api/v1/test/s3` - Test S3 operations with AWS service demo
- `GET /api/v1/test/architecture` - Hexagonal architecture demonstration
- `GET /api/v1/test/factories` - Factory pattern demonstration
- `GET /api/v1/test/performance` - Performance monitoring demo
- `DELETE /api/v1/test/cleanup` - Test cleanup operations

### Request/Response Examples

#### Create User
```bash
# Request
curl -X POST "http://localhost:8000/api/v1/users" \
     -H "Content-Type: application/json" \
     -d '{"email": "user@example.com", "name": "John Doe"}'

# Response
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Get User
```bash
# Request
curl "http://localhost:8000/api/v1/users/123e4567-e89b-12d3-a456-426614174000"

# Response
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Health Check
```bash
# Request
curl "http://localhost:8000/health"

# Response
{
  "status": "healthy",
  "app_name": "APP_BE_MENTANA",
  "version": "1.0.0"
}
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_users.py -v

# Run tests with specific marker
pytest -m unit

# Run tests and generate HTML coverage report
pytest --cov=. --cov-report=html
```

### API Endpoint Testing

The project includes comprehensive test endpoints that demonstrate all functionality:

```bash
# Test all API endpoints
python run.py test-api

# Or run manually
python scripts/test_endpoints.py
```

#### Test Endpoints Overview

1. **Comprehensive Health Check** (`GET /api/v1/test/health`)
   - Tests AWS credentials, DynamoDB, and S3 connectivity
   - Provides detailed service status information
   - Shows AWS account and user information

2. **Hexagonal Architecture Demo** (`POST /api/v1/test/user`)
   - Creates test users using the complete hexagonal architecture
   - Demonstrates domain layer, use cases, and adapters
   - Shows dependency injection in action

3. **Repository Pattern Demo** (`GET /api/v1/test/users`)
   - Retrieves users using the repository pattern
   - Demonstrates data persistence with DynamoDB
   - Shows interface and implementation separation

4. **AWS S3 Service Demo** (`POST /api/v1/test/s3`)
   - Uploads test files to S3
   - Demonstrates AWS service integration
   - Shows service pattern implementation

5. **Architecture Documentation** (`GET /api/v1/test/architecture`)
   - Provides detailed information about hexagonal architecture
   - Explains layers, components, and benefits
   - Educational endpoint for understanding the architecture

6. **Factory Pattern Demo** (`GET /api/v1/test/factories`)
   - Demonstrates Factory pattern implementation
   - Shows centralized object creation
   - Explains dependency injection management

7. **Performance Monitoring** (`GET /api/v1/test/performance`)
   - Demonstrates performance measurement
   - Provides optimization recommendations
   - Shows monitoring best practices

8. **Cleanup Operations** (`DELETE /api/v1/test/cleanup`)
   - Demonstrates cleanup strategies
   - Provides production recommendations
   - Shows data management best practices

### Test Structure

```
tests/
├── unit/              # Unit tests
├── integration/       # Integration tests
├── conftest.py       # Test configuration
└── fixtures/         # Test fixtures
```

### Writing Tests

Follow the hexagonal architecture pattern:
- **Unit tests**: Test use cases and domain logic in isolation
- **Integration tests**: Test adapters and external services
- **End-to-end tests**: Test complete API endpoints

## 🚀 Execution Scripts

### Setup virtual environment
```bash
python run.py venv
```

### Setup DynamoDB table
```bash
python run.py dynamodb
```

### Check dependencies
```bash
python run.py check
```

### Install dependencies
```bash
python run.py install
```

### Run tests
```bash
python run.py test
```

### Test API endpoints
```bash
python run.py test-api
```

### Check AWS
```bash
python run.py aws
```

### Complete setup
```bash
python run.py all
```

### Manual virtual environment setup
```bash
# Run the setup script directly
python scripts/setup_venv.py
```

### Manual API testing
```bash
# Run the test script directly
python scripts/test_endpoints.py

# Test with custom URL
python scripts/test_endpoints.py --url http://localhost:8000
```

## 📝 Logging

The project uses `structlog` for structured logging. Logs include:

- ISO timestamp
- Log level
- Structured context
- Stack traces for errors

### Log Configuration

```python
import structlog

logger = structlog.get_logger()
logger.info("Operation successful", user_id="123", action="create")
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about application flow
- **WARNING**: Warning messages for potentially harmful situations
- **ERROR**: Error messages for error conditions
- **CRITICAL**: Critical errors that may prevent the application from running

### Log Format

Logs are output in JSON format for easy parsing:
```json
{
  "timestamp": "2024-01-01T00:00:00.000Z",
  "level": "info",
  "logger": "api.routers.user_router",
  "message": "User created successfully",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com"
}
```

## 🔧 Development

### Add New Endpoints

1. **Create DTOs** in `api/src/dtos/`
2. **Create use cases** in `domain/src/use_cases/`
3. **Implement repositories** in `adapters/repositories/`
4. **Create routers** in `api/src/routers/`
5. **Register router** in `main.py`

### Add New AWS Services

1. **Create service** in `adapters/services/`
2. **Configure in** `config.py`
3. **Inject dependencies** in routers

### Add New Entities

1. **Create entity** in `domain/src/entities/`
2. **Create repository interface** in `domain/src/repositories/`
3. **Implement repository** in `adapters/repositories/`
4. **Create use cases** in `domain/src/use_cases/`
5. **Add factory methods** in `factories/` (if needed)

### Factory Pattern

The project uses the Factory pattern to centralize object creation and dependency management:

#### RepositoryFactory
```python
# Get user repository instance
user_repo = RepositoryFactory.get_user_repository()

# Create repository by type
user_repo = RepositoryFactory.create_repository_by_type("dynamodb")
```

#### ServiceFactory
```python
# Get S3 service instance
s3_service = ServiceFactory.get_s3_service()

# Create service by type
s3_service = ServiceFactory.create_service_by_type("s3")
```

#### UseCaseFactory
```python
# Get use case instance
create_user_uc = UseCaseFactory.get_create_user_use_case()

# Create use case with specific repository
create_user_uc = UseCaseFactory.create_use_case_with_repository("create_user", "dynamodb")
```

#### UserFactory
```python
# Create user entity
user = UserFactory.create_user(email="user@example.com", name="John Doe")

# Create test user
test_user = UserFactory.create_test_user()

# Validate user data
cleaned_data = UserFactory.validate_user_data(user_data)
```

#### Benefits of Factory Pattern
- **Centralized Configuration**: All object creation logic in one place
- **Easy Testing**: Simple to mock and test dependencies
- **Dependency Management**: Clear dependency injection
- **Consistency**: Uniform object creation across the application
- **Flexibility**: Easy to switch implementations

## 🚀 Deployment

### Environment Variables

Make sure to set the following environment variables in production:

```env
# Application
DEBUG=false
APP_NAME=APP_BE_MENTANA
VERSION=1.0.0

# AWS Configuration
AWS_ACCESS_KEY_ID=your_production_access_key
AWS_SECRET_ACCESS_KEY=your_production_secret_key
AWS_REGION=us-east-1
AWS_DYNAMODB_TABLE=your_production_table
AWS_S3_BUCKET=your_production_bucket

# Security
SECRET_KEY=your_production_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### AWS ECS/Fargate

1. **Prepare application**
   - Build Docker image
   - Push to ECR
   - Create task definition

2. **Create task definition**
   - Configure environment variables
   - Set resource limits
   - Configure networking

3. **Deploy to ECS**
   - Create service
   - Configure load balancer
   - Set up auto-scaling

### AWS Lambda

1. **Configure for Lambda**
   - Install dependencies
   - Create deployment package
   - Configure handler

2. **Create deployment package**
   ```bash
   pip install -r requirements.txt -t package/
   cp main.py package/
   cd package && zip -r ../lambda-deployment.zip .
   ```

3. **Configure API Gateway**
   - Create REST API
   - Configure routes
   - Set up CORS

### AWS App Runner

1. **Connect repository**
   - Link GitHub/GitLab repository
   - Configure branch

2. **Configure build settings**
   - Set build command
   - Configure environment variables
   - Set port configuration

3. **Deploy automatically**
   - App Runner handles deployment
   - Automatic scaling
   - Built-in monitoring

### Monitoring and Observability

- **CloudWatch Logs**: Application logs
- **CloudWatch Metrics**: Performance metrics
- **X-Ray**: Distributed tracing
- **Health Checks**: Application health monitoring

## 🔒 Security

### Best Practices

- **Environment Variables**: Never commit sensitive data to version control
- **AWS IAM**: Use least privilege principle for AWS permissions
- **Input Validation**: All inputs are validated using Pydantic
- **HTTPS**: Always use HTTPS in production
- **CORS**: Configure CORS properly for your domains

### Security Headers

The application includes security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

## 🐛 Troubleshooting

### Common Issues

1. **AWS Credentials Not Found**
   ```bash
   # Solution: Configure AWS credentials
   aws configure
   ```

2. **DynamoDB Table Not Found**
   ```bash
   # Solution: Create table or check table name
   aws dynamodb create-table --table-name users --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
   ```

3. **Port Already in Use**
   ```bash
   # Solution: Use different port
   uvicorn main:app --port 8001
   ```

4. **Import Errors**
   ```bash
   # Solution: Install dependencies
   pip install -r requirements.txt
   ```

### Debug Mode

Enable debug mode for detailed error messages:
```env
DEBUG=true
```

## 📄 License

This project is under the MIT License.

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Use conventional commit messages
- Ensure all tests pass before submitting PR

## 📞 Support

For support, contact the development team or create an issue in the repository.

## 📊 Project Status

- **Version**: 1.0.0
- **Status**: Development
- **Python**: 3.11+
- **Architecture**: Hexagonal (Clean Architecture)
- **Database**: AWS DynamoDB
- **Cloud**: AWS