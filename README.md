# Fake News Detection Web App

A machine learning-powered web application to detect fake news. The backend uses Python for data processing and model inference, while the frontend provides a simple interface for users to input news articles and get predictions.

## 📁 Project Structure

```
VerifyNow/
├── backend/
│   ├── main.py              # FastAPI server entry point
│   ├── model.py             # ML model loading and prediction logic
│   ├── scraper.py           # Web scraping utilities for article extraction
│   ├── requirements.txt     # Python dependencies
│   └── trained_model/
│       ├── model.pkl        # Trained machine learning model
│       └── vectorizer.pkl   # Text vectorizer for feature extraction
├── data/
│   ├── Fake.csv            # Dataset containing fake news articles
│   └── True.csv            # Dataset containing real news articles
└── frontend/
    ├── index.html          # Main web application interface
    ├── script.js           # Frontend JavaScript logic
    ├── style.css           # CSS stylesheet
    └── assets/             # Images and static assets
```

## 🚀 Getting Started

### 1. Install Backend Dependencies

```sh
cd backend
pip install -r requirements.txt
```

### 2. Run the Backend Server

```sh
python main.py
```

### 3. Open the Frontend

Open [frontend/index.html](frontend/index.html) in your browser.

## 🧠 Features

- Detects fake news using a trained machine learning model
- Simple web interface for user input
- Uses real datasets for training ([data/Fake.csv](data/Fake.csv), [data/True.csv](data/True.csv))
- Easily extensible backend and frontend

## 🛠️ Requirements

- Python 3.x
- Required Python packages (see [backend/requirements.txt](backend/requirements.txt))
- Modern web browser

## 📚 Datasets

- [data/Fake.csv](data/Fake.csv): Fake news samples
- [data/True.csv](data/True.csv): True news samples

## 🤝 Contributing

Pull requests and issues are welcome!

## 📄 License

MIT License

---

*This project is for educational purposes only.*