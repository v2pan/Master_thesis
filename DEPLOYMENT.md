# Deployment Guide

This guide provides multiple deployment options for the SQL Query Enhancement Streamlit App.

## 🚀 Quick Start

### Option 1: Simple Script (Recommended for Development)

```bash
# Make the script executable
chmod +x start.sh

# Run the app
./start.sh

# Or specify a custom port
./start.sh 8502
```

### Option 2: Python Deployment Script

```bash
# Run with default settings
python deploy.py

# Custom port and host
python deploy.py --port 8502 --host 0.0.0.0

# Skip installation (if already installed)
python deploy.py --skip-install
```

### Option 3: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p Data saved_json saved_plots temporary

# Run Streamlit
streamlit run app.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Build and run with docker-compose
docker-compose up --build

# Run in background
docker-compose up -d

# Stop the service
docker-compose down
```

### Using Docker Directly

```bash
# Build the image
docker build -t sql-query-enhancement .

# Run the container
docker run -p 8501:8501 sql-query-enhancement

# Run with environment variables
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY=your_key \
  -e OPENAI_API_KEY=your_key \
  sql-query-enhancement
```

## ☁️ Cloud Deployment

### Heroku

1. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

2. **Set environment variables**:
   ```bash
   heroku config:set GOOGLE_API_KEY=your_key
   heroku config:set OPENAI_API_KEY=your_key
   ```

3. **Deploy**:
   ```bash
   git push heroku main
   ```

### Google Cloud Run

1. **Build and push to Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/sql-query-enhancement
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy sql-query-enhancement \
     --image gcr.io/PROJECT_ID/sql-query-enhancement \
     --platform managed \
     --allow-unauthenticated \
     --port 8501
   ```

### AWS ECS

1. **Create ECR repository**:
   ```bash
   aws ecr create-repository --repository-name sql-query-enhancement
   ```

2. **Build and push**:
   ```bash
   aws ecr get-login-password --region region | docker login --username AWS --password-stdin account.dkr.ecr.region.amazonaws.com
   docker build -t sql-query-enhancement .
   docker tag sql-query-enhancement:latest account.dkr.ecr.region.amazonaws.com/sql-query-enhancement:latest
   docker push account.dkr.ecr.region.amazonaws.com/sql-query-enhancement:latest
   ```

3. **Deploy to ECS** (using AWS Console or CLI)

## 🔧 Environment Configuration

### Required Environment Variables

None are strictly required, but the following are recommended:

```bash
# API Keys for LLM services
export GOOGLE_API_KEY="your_google_api_key"
export OPENAI_API_KEY="your_openai_api_key"
export ANTHROPIC_API_KEY="your_anthropic_api_key"

# Optional: Database configuration
export DATABASE_URL="your_database_url"
```

### Configuration Files

Create a `.env` file for local development:

```env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
DATABASE_URL=your_database_url
```

## 📊 Monitoring and Logging

### Health Checks

The application includes health check endpoints:

- **Health Check**: `http://localhost:8501/_stcore/health`
- **Metrics**: Available through Streamlit's built-in monitoring

### Logging

Enable debug logging:

```bash
streamlit run app.py --logger.level debug
```

### Performance Monitoring

Monitor resource usage:

```bash
# CPU and Memory
htop

# Network connections
netstat -tulpn | grep 8501

# Docker stats (if using containers)
docker stats
```

## 🔒 Security Considerations

### Production Security

1. **Use HTTPS**: Always use HTTPS in production
2. **API Key Management**: Store API keys securely
3. **Access Control**: Implement authentication if needed
4. **Rate Limiting**: Consider implementing rate limiting
5. **Input Validation**: Validate all user inputs

### Security Headers

Add security headers to your reverse proxy:

```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Find process using port
   lsof -i :8501
   
   # Kill process
   kill -9 <PID>
   ```

2. **Import Errors**:
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Memory Issues**:
   ```bash
   # Increase memory limit for Docker
   docker run -m 4g sql-query-enhancement
   ```

4. **API Key Issues**:
   ```bash
   # Check environment variables
   echo $GOOGLE_API_KEY
   ```

### Debug Mode

Enable debug mode for detailed error messages:

```bash
streamlit run app.py --logger.level debug --server.headless false
```

## 📈 Scaling

### Horizontal Scaling

For high-traffic applications:

1. **Load Balancer**: Use a load balancer (nginx, HAProxy)
2. **Multiple Instances**: Run multiple app instances
3. **Database**: Use external database (PostgreSQL, MySQL)
4. **Caching**: Implement Redis for caching

### Vertical Scaling

Increase resources:

```bash
# Docker with more resources
docker run -m 8g -c 4 sql-query-enhancement

# Kubernetes resource limits
resources:
  limits:
    memory: "8Gi"
    cpu: "4"
  requests:
    memory: "4Gi"
    cpu: "2"
```

## 📞 Support

For deployment issues:

1. Check the troubleshooting section
2. Review logs and error messages
3. Test with minimal configuration
4. Create an issue on GitHub

---

**Happy Deploying! 🚀**
