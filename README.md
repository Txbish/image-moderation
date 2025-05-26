# Image Moderation FastAPI

A secure REST API built with FastAPI that automatically detects and analyzes harmful, illegal, or unwanted imagery using Azure Content Safety services. The system provides content moderation capabilities with token-based authentication and comprehensive usage tracking.

## Features

- **Image Content Analysis**: Automatically detect and score harmful content including:
  - Hate symbols and content
  - Self-harm depictions
  - Sexual content
  - Violence and graphic content
- **Token-based Authentication**: Secure bearer token system with admin and user roles
- **Usage Tracking**: Complete audit trail of API usage per token
- **Admin Management**: Full token lifecycle management for administrators
- **MongoDB Integration**: Efficient data storage and retrieval
- **Docker Containerization**: Easy deployment with Docker and Docker Compose
- **CORS Support**: Cross-origin requests enabled for frontend integration

## System Architecture

The system consists of:

- **FastAPI Backend**: Main API server handling authentication and moderation
- **MongoDB Database**: Stores tokens and usage logs
- **Azure Content Safety**: External service for image analysis
- **Nginx Frontend**: Simple web interface for API interaction

## Prerequisites

Before running the application, ensure you have:

### Required Software

- **Python 3.8+**
- **Docker & Docker Compose**
- **Git**
- **MongoDB** (if running locally without Docker)

### Required Accounts & Services

- **MongoDB Atlas Account** (for cloud database) OR local MongoDB installation
- **Azure Account** with Content Safety service enabled

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Txbish/image-moderation.git
cd image-moderation-api
```

### 2. Environment Configuration

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit the `.env` file and replace the placeholder values with your actual credentials:

- `MONGO_URI` - Your MongoDB connection string
- `CONTENT_SAFETY_KEY` - Your Azure Content Safety API key
- `CONTENT_SAFETY_ENDPOINT` - Your Azure Content Safety endpoint URL

## Getting Required API Keys & Services

### MongoDB Setup

#### Option 1: MongoDB Atlas (Recommended)

1. Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account
3. Create a new cluster
4. Go to "Database Access" → Create database user
5. Go to "Network Access" → Add IP address (0.0.0.0/0 for development)
6. Go to "Clusters" → Click "Connect" → "Connect your application"
7. Copy the connection string and replace `<password>` with your database user password
8. Use this as your `MONGO_URI`

#### Option 2: Local MongoDB

1. Install MongoDB locally
2. Start MongoDB service
3. Use `MONGO_URI=mongodb://localhost:27017/image_moderation`

### Azure Content Safety Setup

1. **Create Azure Account**

   - Visit [Azure Portal](https://portal.azure.com)
   - Sign up for free account (includes $200 credit)

2. **Create Content Safety Resource**

   - In Azure Portal, click "Create a resource"
   - Search for "Content Safety"
   - Click "Create" → "Content Safety"
   - Fill in required details:
     - Subscription: Your subscription
     - Resource Group: Create new or use existing
     - Region: Choose nearest region
     - Name: Unique name for your resource
     - Pricing Tier: Free tier available

3. **Get Keys and Endpoint**
   - After deployment, go to your Content Safety resource
   - Navigate to "Keys and Endpoint" section
   - Copy `Key 1` as your `CONTENT_SAFETY_KEY`
   - Copy `Endpoint` as your `CONTENT_SAFETY_ENDPOINT`

## Running the Application

### Method 1: Using Docker (Recommended)

1. **Build and start all services:**

```bash
docker-compose up --build
```

2. **Access the services:**
   - Backend API: http://localhost:7000
   - Frontend UI: http://localhost:80
   - API Documentation: http://localhost:7000/docs

### Method 2: Using Uvicorn (Development)

1. **Install Python dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

2. **Start the FastAPI server:**

```bash
# From the backend directory
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
```

3. **Access the API:**
   - API Server: http://localhost:7000
   - Interactive Documentation: http://localhost:7000/docs
   - ReDoc Documentation: http://localhost:7000/redoc

## API Usage

### Authentication

The system includes pre-seeded tokens for immediate testing:

- **Admin Token**: `admin-seed-token` (can manage other tokens)
- **User Token**: `user-seed-token` (can only moderate images)

### Available Endpoints

#### Authentication Endpoints (Admin Only)

- `POST /auth/tokens` - Create new token
- `GET /auth/tokens` - List all tokens
- `GET /auth/tokens/is_admin` - Check if token has admin privileges
- `DELETE /auth/tokens/{token}` - Delete specific token

#### Moderation Endpoint

- `POST /moderate` - Upload and analyze image content

### Example API Calls

#### Check Admin Status

```bash
curl -X GET "http://localhost:7000/auth/tokens/is_admin" \
     -H "Authorization: Bearer admin-seed-token"
```

#### Create New Token

```bash
curl -X POST "http://localhost:7000/auth/tokens" \
     -H "Authorization: Bearer admin-seed-token" \
     -H "Content-Type: application/json" \
     -d '{"is_admin": false}'
```

#### Moderate Image

```bash
curl -X POST "http://localhost:7000/moderate" \
     -H "Authorization: Bearer user-seed-token" \
     -F "file=@/path/to/your/image.jpg"
```

## API Response Format

### Moderation Response

```json
{
  "result": {
    "hate": 0.14,
    "self_harm": 0.0,
    "sexual": 0.29,
    "violence": 0.43
  }
}
```

Scores range from 0.0 to 1.0, where:

- 0.0 = No harmful content detected
- 1.0 = High confidence of harmful content

## Database Collections

### tokens Collection

```javascript
{
  "_id": ObjectId,
  "token": "uuid-string",
  "isAdmin": boolean,
  "createdAt": datetime
}
```

### usages Collection

```javascript
{
  "_id": ObjectId,
  "token": "uuid-string",
  "endpoint": "/moderate",
  "timestamp": datetime
}
```

## Development

### Project Structure

```
image-moderation-api/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── moderate.py
│   │   ├── middleware.py
│   │   └── db.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── index.html
├── docker-compose.yml
├── .env.example
└── README.md
```

### Adding Dependencies

```bash
cd backend
pip install new-package
pip freeze > requirements.txt
```

### Running Tests

```bash
cd backend
pytest
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**

   - Verify `MONGO_URI` is correct
   - Check network access settings in MongoDB Atlas
   - Ensure database user has proper permissions

2. **Azure Content Safety Errors**

   - Verify `CONTENT_SAFETY_KEY` and `CONTENT_SAFETY_ENDPOINT` are correct
   - Check Azure subscription status
   - Ensure Content Safety service is active

3. **Docker Issues**

   - Ensure Docker daemon is running
   - Check port conflicts (7000, 80)
   - Verify `.env` file exists and is properly formatted

4. **Token Authentication Errors**
   - Ensure `Authorization: Bearer <token>` header is included
   - Verify token exists in database
   - Check if endpoint requires admin privileges

### Logs and Debugging

View application logs:

```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend

# Direct uvicorn logs
# Logs appear in terminal when running with --reload
```

## Production Deployment

For production deployment:

1. **Security Considerations**

   - Use strong, unique tokens
   - Enable HTTPS/TLS
   - Implement rate limiting
   - Use production MongoDB cluster
   - Restrict CORS origins

2. **Environment Variables**

   - Use secure secret management
   - Never commit `.env` to version control
   - Use environment-specific configurations

3. **Monitoring**
   - Set up application monitoring
   - Monitor Azure Content Safety usage/quotas
   - Track database performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For support and questions:

- Review Azure Content Safety documentation
- MongoDB Atlas documentation for database issues
