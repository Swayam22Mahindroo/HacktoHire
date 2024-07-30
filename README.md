# Flight Notification System
## Overview
This project implements a flight notification system using Flask for the backend, React for the frontend, and Kafka for real-time notifications. SQLite is used for database management. The system allows users to manage flight data and receive real-time updates on flight status changes.
## Project Structure
The repository is organized into three main folders:
1. **Consumer Solution**: Flask application to consume Kafka messages.
2. **Producer Flask**: Flask backend to handle flight data and send notifications to Kafka.
3. **Producer React**: React frontend to display flight data and handle user interactions.
## Folder Details
### 1. Consumer Solution (Flask Application)
**Purpose**: Consumes messages from Kafka and processes flight notifications.
- **Main Features**:
  - Connects to Kafka and listens for flight notifications.
  - Processes and logs incoming messages.
- **Dependencies**:
  - `confluent_kafka`
  - `flask`
  - `sqlite3`
  - `dotenv`
- **Run Instructions**:
  bash
  cd consumer_solution
  pip install -r requirements.txt
  python app.py
  
### 2. Producer Flask (Backend)
**Purpose**: Manages flight data and sends notifications to Kafka.
**Main Features**:
- CRUD operations for flight data using SQLite.
- Sends flight status updates to Kafka.
**Dependencies**:
- `confluent_kafka`
- `flask`
- `sqlite3`
- `dotenv`
**Run Instructions**:
bash
cd producer_flask
pip install -r requirements.txt
python app.py

### 3. Producer React (Frontend)
**Purpose**: Provides a user interface to manage and view flight data.
**Main Features**:
- Form to add and edit flight details.
- Displays list of flights with options to edit or delete.
- Handles real-time updates from Kafka.
**Dependencies**:
- `axios`
- `react`
- `react-dom`
- `react-scripts`
**Run Instructions**:
bash
cd producer_react
npm install
npm start

## Configuration
- **Environment Variables**:
  - Create a `.env` file in the `producer_flask` and `consumer_solution` folders with the following variables:
    env
    KAFKA_BOOTSTRAP_SERVERS=localhost:9092
    DATABASE=flights.db
    
## Usage
### Backend
- **Endpoints**:
  - `GET /flights`: Retrieve all flights.
  - `POST /flights`: Add a new flight.
  - `PUT /flights/{id}`: Edit an existing flight.
  - `DELETE /flights/{id}`: Delete a flight.
### Frontend
- **Features**:
  - Form to add new flights.
  - List to display all flights with edit and delete options.
  - Real-time updates on flight status changes.
## Challenges and Solutions
- **CORS Issues**: Solved by using Flask-CORS middleware.
- **Real-Time Updates**: Implemented Kafka for efficient message streaming.
- **API Error Handling**: Added robust error handling in Flask routes.
## Future Work
- **Adding User Authentication**: Implement JWT or OAuth for secure access.
- **Detailed Notifications**: Include flight delays, cancellations, and gate changes.
- **Scaling for Larger Datasets**: Transition to PostgreSQL/MySQL and optimize Kafka settings.
## Contribution
Feel free to fork the repository, make changes, and submit pull requests. For any questions or issues, open an issue on GitHub.
## License
This project is licensed under the MIT License.
