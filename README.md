<div align="center">

# 🛡️ Image Moderation API

### Intelligent Content Safety with Azure AI

_A powerful FastAPI service that automatically detects harmful, illegal, or unwanted imagery using Azure Content Safety services._

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Azure](https://img.shields.io/badge/Microsoft_Azure-0089D0?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[🚀 Quick Start](#-quick-start) • [📖 Documentation](#-api-documentation) • [🔧 Setup Guide](#-setup-guide) • [💡 Examples](#-examples)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 **Smart Content Analysis**

- 🚫 Hate symbols & content detection
- ⚠️ Self-harm content identification
- 🔞 Sexual content recognition
- ⚔️ Violence & graphic content analysis

</td>
<td width="50%">

### 🔐 **Security & Management**

- 🔑 Token-based authentication
- 👑 Admin & user role system
- 📊 Complete usage tracking
- 🗄️ MongoDB integration

</td>
</tr>
</table>

### 🏗️ **Additional Benefits**

- 🐳 **Docker Ready** - One-command deployment
- 🌐 **CORS Enabled** - Frontend integration ready
- 📝 **Auto Documentation** - Interactive API docs
- ⚡ **Fast & Scalable** - Built on FastAPI

---

## 🏗️ System Architecture

```mermaid
graph TB
    A[🌐 Frontend UI] --> B[⚡ FastAPI Backend]
    B --> C[🗄️ MongoDB Database]
    B --> D[🧠 Azure Content Safety]
    B --> E[📊 Usage Analytics]

    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fce4ec
```

---

## 🚀 Quick Start

### 🐳 **Option 1: Docker (Recommended)**

```bash
# Clone and run in 3 commands
git clone https://github.com/Txbish/image-moderation.git
cd image-moderation
docker-compose up --build
```

> 🎉 **That's it!** Your API is running at `http://localhost:7000`

### 🐍 **Option 2: Python Development**

```bash
# Setup environment
cd backend
pip install -r requirements.txt

# Launch server
uvicorn app.main:app --host 0.0.0.0 --port 7000 --reload
```

---

## 🔧 Setup Guide

### 📋 **Prerequisites**

<details>
<summary>🖥️ <strong>Required Software</strong></summary>

- ✅ **Python 3.8+**
- ✅ **Docker & Docker Compose**
- ✅ **Git**
- ✅ **MongoDB** (local or Atlas)

</details>

<details>
<summary>☁️ <strong>Cloud Services</strong></summary>

- 🍃 **MongoDB Atlas Account** (free tier available)
- 🔵 **Azure Account** with Content Safety service

</details>

### ⚙️ **Environment Configuration**

1. **Copy environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Fill in your credentials:**

   ```bash
   # MongoDB connection
   MONGO_URI=your_mongodb_connection_string

   # Azure Content Safety
   CONTENT_SAFETY_KEY=your_azure_content_safety_key
   CONTENT_SAFETY_ENDPOINT=your_azure_endpoint_url
   ```

---

## 🔑 Getting API Keys

### 🍃 **MongoDB Atlas Setup**

<details>
<summary>📖 <strong>Step-by-step MongoDB Atlas guide</strong></summary>

1. 🌐 Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
2. 📝 Create free account
3. 🗄️ Create new cluster
4. 👤 **Database Access** → Create database user
5. 🌍 **Network Access** → Add IP (0.0.0.0/0 for development)
6. 🔗 **Clusters** → Connect → **Connect your application**
7. 📋 Copy connection string and replace `<password>`

**Connection string format:**

```
mongodb+srv://username:password@cluster.mongodb.net/image_moderation
```

</details>

### 🔵 **Azure Content Safety Setup**

<details>
<summary>📖 <strong>Step-by-step Azure guide</strong></summary>

1. 🌐 Visit [Azure Portal](https://portal.azure.com)
2. 💳 Sign up (free $200 credit included)
3. ➕ **Create a resource** → Search "Content Safety"
4. 📝 Configure:
   - **Subscription:** Your subscription
   - **Resource Group:** Create new
   - **Region:** Choose nearest
   - **Pricing:** Free tier available
5. 🔑 **Keys and Endpoint** → Copy `Key 1` and `Endpoint`

</details>

---

## 🌐 Access Points

Once running, access these services:

| Service            | URL                         | Description               |
| ------------------ | --------------------------- | ------------------------- |
| 🖥️ **Frontend UI** | http://localhost:80         | Web interface             |
| ⚡ **Backend API** | http://localhost:7000       | Main API server           |
| 📖 **API Docs**    | http://localhost:7000/docs  | Interactive documentation |
| 📚 **ReDoc**       | http://localhost:7000/redoc | Alternative documentation |

---

## 💡 Examples

### 🔑 **Pre-seeded Tokens**

| Token              | Type     | Capabilities                  |
| ------------------ | -------- | ----------------------------- |
| `admin-seed-token` | 👑 Admin | Token management + moderation |
| `user-seed-token`  | 👤 User  | Image moderation only         |

### 📝 **API Examples**

<details>
<summary>🔍 <strong>Check Admin Status</strong></summary>

```bash
curl -X GET "http://localhost:7000/auth/tokens/is_admin" \
     -H "Authorization: Bearer admin-seed-token"
```

**Response:**

```json
{
  "is_admin": true,
  "token": "admin-seed-token"
}
```

</details>

<details>
<summary>➕ <strong>Create New Token</strong></summary>

```bash
curl -X POST "http://localhost:7000/auth/tokens" \
     -H "Authorization: Bearer admin-seed-token" \
     -H "Content-Type: application/json" \
     -d '{"is_admin": false}'
```

**Response:**

```json
{
  "token": "new-uuid-token-here",
  "is_admin": false,
  "created_at": "2025-05-26T10:30:00Z"
}
```

</details>

<details>
<summary>🖼️ <strong>Moderate Image</strong></summary>

```bash
curl -X POST "http://localhost:7000/moderate" \
     -H "Authorization: Bearer user-seed-token" \
     -F "file=@/path/to/your/image.jpg"
```

**Response:**

```json
{
  "result": {
    "hate": 0.14,
    "self_harm": 0.0,
    "sexual": 0.29,
    "violence": 0.43
  },
  "analysis": {
    "timestamp": "2025-05-26T10:30:00Z",
    "filename": "image.jpg",
    "status": "analyzed"
  }
}
```

</details>

---

## 📊 API Reference

### 🔐 **Authentication Endpoints**

| Method   | Endpoint                | Access   | Description        |
| -------- | ----------------------- | -------- | ------------------ |
| `POST`   | `/auth/tokens`          | 👑 Admin | Create new token   |
| `GET`    | `/auth/tokens`          | 👑 Admin | List all tokens    |
| `GET`    | `/auth/tokens/is_admin` | 🔑 Any   | Check admin status |
| `DELETE` | `/auth/tokens/{token}`  | 👑 Admin | Delete token       |

### 🛡️ **Moderation Endpoints**

| Method | Endpoint    | Access | Description           |
| ------ | ----------- | ------ | --------------------- |
| `POST` | `/moderate` | 🔑 Any | Analyze image content |

### 📈 **Score Interpretation**

| Score Range | Meaning                     | Action               |
| ----------- | --------------------------- | -------------------- |
| `0.0 - 0.2` | 🟢 Safe content             | ✅ Allow             |
| `0.2 - 0.5` | 🟡 Potentially questionable | ⚠️ Review            |
| `0.5 - 0.8` | 🟠 Likely harmful           | 🚫 Block             |
| `0.8 - 1.0` | 🔴 High confidence harmful  | 🚨 Block immediately |

---

## 🗄️ Database Schema

<details>
<summary>📋 <strong>Collections Structure</strong></summary>

### `tokens` Collection

```javascript
{
  "_id": ObjectId,
  "token": "uuid-string",
  "isAdmin": boolean,
  "createdAt": datetime
}
```

### `usages` Collection

```javascript
{
  "_id": ObjectId,
  "token": "uuid-string",
  "endpoint": "/moderate",
  "timestamp": datetime,
  "metadata": {
    "filename": "string",
    "filesize": number
  }
}
```

</details>

---

## 🔧 Development

### 📁 **Project Structure**

```
image-moderation/
├── 🚀 backend/
│   ├── 📦 app/
│   │   ├── 🏠 main.py
│   │   ├── 🔐 auth.py
│   │   ├── 🛡️ moderate.py
│   │   ├── ⚙️ middleware.py
│   │   └── 🗄️ db.py
│   ├── 📋 requirements.txt
│   └── 🐳 Dockerfile
├── 🌐 frontend/
│   └── 📄 index.html
├── 🐳 docker-compose.yml
├── ⚙️ .env.example
└── 📖 README.md
```

### 🔧 **Development Commands**

```bash
# Add new dependency
cd backend && pip install new-package
pip freeze > requirements.txt

# Run tests
pytest

# View logs
docker-compose logs backend
```

---

## 🚨 Troubleshooting

<details>
<summary>🔍 <strong>Common Issues & Solutions</strong></summary>

### 🗄️ **MongoDB Connection Failed**

- ✅ Verify `MONGO_URI` format
- ✅ Check MongoDB Atlas network access
- ✅ Ensure database user permissions

### 🔵 **Azure Content Safety Errors**

- ✅ Verify API key and endpoint
- ✅ Check Azure subscription status
- ✅ Ensure service quota isn't exceeded

### 🐳 **Docker Issues**

- ✅ Check if Docker daemon is running
- ✅ Verify ports 7000 and 80 are available
- ✅ Ensure `.env` file exists

### 🔑 **Authentication Errors**

- ✅ Include `Authorization: Bearer <token>` header
- ✅ Verify token exists in database
- ✅ Check if endpoint requires admin privileges

</details>

---

## 🚀 Production Deployment

### 🔒 **Security Checklist**

- [ ] 🔐 Use strong, unique tokens
- [ ] 🌐 Enable HTTPS/TLS
- [ ] ⏱️ Implement rate limiting
- [ ] 🗄️ Use production MongoDB cluster
- [ ] 🌍 Restrict CORS origins
- [ ] 🔐 Use secure secret management

### 📊 **Monitoring**

- [ ] 📈 Application performance monitoring
- [ ] 💰 Azure Content Safety usage tracking
- [ ] 🗄️ Database performance metrics
- [ ] 🚨 Error alerting system

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. 🍴 **Fork** the repository
2. 🌿 **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 **Commit** changes (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** to branch (`git push origin feature/amazing-feature`)
5. 🔃 **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 💬 Support & Community

<div align="center">

### Need Help?

📖 **Documentation** • 💬 **Discussions** • 🐛 **Issues** • 📧 **Contact**

### Useful Resources

- 📚 [Azure Content Safety Docs](https://docs.microsoft.com/en-us/azure/cognitive-services/content-safety/)
- 🍃 [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- ⚡ [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Made with ❤️ for safer digital content**

</div>
