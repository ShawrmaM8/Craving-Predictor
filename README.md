# Personal Urge Predictor + Alert System



A free, zero-config system to predict urges before they happen, log daily reports, and alert users in real-time. Built with Python (FastAPI + scikit-learn) and React for the frontend.



---



## Features



\* Predict urge risk based on sleep, stress, productivity, exercise, and past events.

\* Real-time alerts using a rule-based tier system.

\* Local ML training with logistic regression (no paid services).

\* Stores reports and events in a lightweight SQLite database.

\* React dashboard to submit reports and view predictions.

\* Background scheduler to automatically evaluate risk every 15 minutes.



---



## Repo Structure



```

urge-predictor/

│── README.md

│── requirements.txt

│── .gitignore

│

├── backend/

│   │── main.py              # FastAPI app + scheduler

│   │── database.py          # SQLite DB init + helpers

│   │── predictor.py         # ML model wrapper

│   │── utils.py             # Paths, preprocessing, logging

│   ├── models/

│   │   │── trainer.py       # Train and save ML model

│   │   └── default\_model.joblib (auto-generated)

│   └── urge\_data.db         # SQLite DB (auto-generated)

│

└── frontend/

&nbsp;   │── package.json         # React dependencies

&nbsp;   │── src/

&nbsp;   │   │── App.jsx          # Main dashboard

&nbsp;   │   │── api.js           # Axios calls to backend

&nbsp;   │   └── components/      # UI components (ReportForm, RiskCard, HistoryList)

```



---



## Setup Instructions



### Backend



1\. Create a Python virtual environment and activate it:



```bash

python -m venv .venv

source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

```



2\. Install dependencies:



```bash

pip install -r requirements.txt

```



3\. Initialize the database (optional, will auto-create on first run):



```bash

python -c "from backend.db.database import init\_db; init\_db()"

```



4\. Train the ML model with existing reports (or synthetic if none):



```bash

python backend/models/trainer.py

```



5\. Start the backend server:



```bash

uvicorn backend.main:app --reload

```



\### Frontend



1\. Navigate to frontend directory:



```bash

cd frontend

```



2\. Install dependencies:



```bash

npm install

```



3\. Start the development server:



```bash

npm run dev

```



4\. Open your browser at `http://localhost:5173` (or whatever Vite prints).



---



## Usage



1\. Enter your `anon\_id` (unique identifier) in the frontend.

2\. Fill daily report: sleep hours, stress, and any urge events.

3\. Submit report → prediction updates automatically.

4\. Prediction shows:



&nbsp;  \* Feature values

&nbsp;  \* Probability of urge

&nbsp;  \* Risk tier (rule-based alert)

5\. Alerts are logged and optionally can trigger notifications.



---



## Extending the System



\* \*\*New features\*\*: add app usage, notes, or sensor data in `ReportIn` model.

\* \*\*Alerts\*\*: expand `backend/alerts/notifier.py` to email, desktop, or mobile push notifications.

\* \*\*Models\*\*: swap logistic regression for any scikit-learn compatible model.

\* \*\*Frontend\*\*: add charts or history lists to visualize past reports and predictions.



---



## Notes



\* Fully zero-cost; no paid APIs required.

\* All paths auto-resolve via `backend/utils.py`, no customization needed.

\* Database and models auto-create on first run.

\* Scheduler runs every 15 minutes to check all users and trigger alerts.



---



A free, zero-config system to predict urges before they happen, log daily reports, and alert users in real-time. Built with Python (FastAPI + scikit-learn) and React for the frontend.



---



## Features



\* Predict urge risk based on sleep, stress, productivity, exercise, and past events.

\* Real-time alerts using a rule-based tier system.

\* Local ML training with logistic regression (no paid services).

\* Stores reports and events in a lightweight SQLite database.

\* React dashboard to submit reports and view predictions.

\* Background scheduler to automatically evaluate risk every 15 minutes.



---



## Repo Structure



```

urge-predictor/

│── README.md

│── requirements.txt

│── .gitignore

│

├── backend/

│   │── main.py              # FastAPI app + scheduler

│   │── database.py          # SQLite DB init + helpers

│   │── predictor.py         # ML model wrapper

│   │── utils.py             # Paths, preprocessing, logging

│   ├── models/

│   │   │── trainer.py       # Train and save ML model

│   │   └── default\_model.joblib (auto-generated)

│   └── urge\_data.db         # SQLite DB (auto-generated)

│

└── frontend/

&nbsp;   │── package.json         # React dependencies

&nbsp;   │── src/

&nbsp;   │   │── App.jsx          # Main dashboard

&nbsp;   │   │── api.js           # Axios calls to backend

&nbsp;   │   └── components/      # UI components (ReportForm, RiskCard, HistoryList)

```



---



## Setup Instructions



### Backend



1\. Create a Python virtual environment and activate it:



```bash

python -m venv .venv

source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

```



2\. Install dependencies:



```bash

pip install -r requirements.txt

```



3\. Initialize the database (optional, will auto-create on first run):



```bash

python -c "from backend.db.database import init\_db; init\_db()"

```



4\. Train the ML model with existing reports (or synthetic if none):



```bash

python backend/models/trainer.py

```



5\. Start the backend server:



```bash

uvicorn backend.main:app --reload

```



### Frontend



1\. Navigate to frontend directory:



```bash

cd frontend

```



2\. Install dependencies:



```bash

npm install

```



3\. Start the development server:



```bash

npm run dev

```



4\. Open your browser at `http://localhost:5173` (or whatever Vite prints).



---



## Usage



1\. Enter your `anon\_id` (unique identifier) in the frontend.

2\. Fill daily report: sleep hours, stress, and any urge events.

3\. Submit report → prediction updates automatically.

4\. Prediction shows:



&nbsp;  \* Feature values

&nbsp;  \* Probability of urge

&nbsp;  \* Risk tier (rule-based alert)

5\. Alerts are logged and optionally can trigger notifications.



---



## Extending the System



\* \*\*New features\*\*: add app usage, notes, or sensor data in `ReportIn` model.

\* \*\*Alerts\*\*: expand `backend/alerts/notifier.py` to email, desktop, or mobile push notifications.

\* \*\*Models\*\*: swap logistic regression for any scikit-learn compatible model.

\* \*\*Frontend\*\*: add charts or history lists to visualize past reports and predictions.



---



## Notes



\* Fully zero-cost; no paid APIs required.

\* All paths auto-resolve via `backend/utils.py`, no customization needed.

\* Database and models auto-create on first run.

\* Scheduler runs every 15 minutes to check all users and trigger alerts.



---






