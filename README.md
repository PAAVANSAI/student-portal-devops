# Student Portal — DevOps CI/CD Demo

A beginner-friendly Flask web application designed as a starting point for
learning Docker, CI/CD pipelines, and DevOps best practices.

---

## Project Structure

```
student-portal-devops/
├── app.py                 # Flask application (routes & data)
├── templates/
│   └── index.html         # Jinja2 HTML template (UI)
├── tests/
│   └── test_app.py        # Automated pytest test suite
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container build instructions
├── .dockerignore          # Files excluded from Docker context
└── README.md              # This file
```

## Quick Start (Local)

```bash
# 1. Create & activate a virtual environment
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
# → Open http://localhost:8080

# 4. Run tests
pytest tests/ -v
```

## Docker

```bash
# Build the image
docker build -t student-portal .

# Run the container
docker run -d -p 8080:8080 --name student-portal student-portal

# Verify
curl http://localhost:8080/health
# → {"status":"healthy"}
```

## Endpoints

| Route     | Method | Description                            |
| --------- | ------ | -------------------------------------- |
| `/`       | GET    | Student Portal homepage                |
| `/health` | GET    | Health check — returns `{"status":"healthy"}` |

## License

This project is provided for educational purposes.
