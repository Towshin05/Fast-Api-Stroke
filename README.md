## Stroke Prediction System (Dockerized)

This project is a fully Dockerized Stroke Prediction System built using **FastAPI (server)** and **Streamlit (client)**. The app allows users to input health-related details and predicts the risk of a stroke using a trained machine learning model.

- **FastAPI** (Backend API)
- **Streamlit** (Frontend UI)
- **Docker** (Client & Server containers)
- **Pydantic** for data validation
- **Feature Engineering** for preprocessing

##  Architecture

```mermaid
graph LR
A[User Input via Browser] --> B[Client (Streamlit)]
B -->|HTTP POST /predict| C[Server (FastAPI)]
C --> D[Feature Engineering & Validation (Pydantic)]
D --> E[ML Model (.pkl)]
E --> C
C --> F[Return Prediction]
F --> B
```
- Client: Streamlit frontend for collecting input and displaying prediction.
- Server: FastAPI backend for data validation, feature engineering, and prediction.
- ML Model: Trained with scikit-learn and saved as a .pkl file.
- Docker Compose: Runs client and server containers.

## Project Structure
stroke-prediction-app/
├── client/
│   ├── home.py
│   ├── requirements.txt
│   └── Dockerfile
├── server/
│   ├── main.py
│   ├── schema.py
│   ├── feature_engineering.py
│   ├── model.pkl
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md

## Technologies Used
- Frontend: Streamlit
- Backend: FastAPI
- Model: scikit-learn (model.pkl)
- Validation: Pydantic
- Feature Engineering: Custom BMI and encoding logic
- Docker: Client and server containers
- Orchestration: Docker Compose

##  Docker Containers
**client**: Runs Streamlit frontend on port 8501
**server**: Runs FastAPI backend on port 8000

## Getting Started
#### Prerequisites
- Docker
- Docker Compose
- Streamlit
- FastApi
- Machine Learning.

### Model Input Features
- Age
- Weight (kg)
- Height (m)
- Gender
- Smoking status
- Heart Disease
- Hypertension
- Residence Type
- Work Type
- Average Glucose Level.


### Example Request
 ```bash
 {
  "age": 30,
  "weight_kg": 70.0,
  "height_m": 1.75,
  "smoking": "yes",
  "gender": "male",
  "heart_disease": "no",
  "hypertension": "no",
  "Residence_type": "New York",
  "work_type": "Part-time",
  "avg_glucose_level": 100.0
}
```
#### Response
```bash
{
  "stroke_prediction": "No(0)"
}
```
