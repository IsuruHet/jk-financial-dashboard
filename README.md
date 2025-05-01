# 📊 JKH Financial Dashboard

![React](https://img.shields.io/badge/Frontend-React-blue?logo=react)
![Tailwind](https://img.shields.io/badge/Style-TailwindCSS-38bdf8?logo=tailwindcss)
![Flask](https://img.shields.io/badge/Backend-Flask-black?logo=flask)
![Chart.js](https://img.shields.io/badge/Charts-Chart.js-fd7e14?logo=chart.js)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

An interactive AI-powered dashboard to visualize and analyze key financial metrics of **John Keells Holdings PLC (2019–2024)** using **React**, **Tailwind CSS**, **Flask**, and **Chart.js**.

## 🎬 Live Demo

## 📽️ [Click to watch the demo video](./2025-05-01%2013-30-55.m4v)

## 🚀 Features

- 📈 Total Revenue (5-Year Curve) with trend analysis
- 📊 Cost of Sales vs Operating Expenses comparison (stacked/grouped bar charts)
- 📉 Gross Profit Margin trend with annotations (e.g., COVID-19, tax policy)
- 💰 EPS and Net Asset Per Share visualized as interactive curves
- 📁 Upload multiple PDF annual reports for automated data extraction
- 🔁 Toggle financial data between LKR and USD
- 🌗 Responsive dark/light mode toggle
- 📦 Download processed data as a CSV
- 👣 Footer with developer credit

---

## ⚙️ Tech Stack

- **Frontend**: React, Tailwind CSS, Chart.js, Vite
- **Backend**: Flask, Camelot, Pandas, Statsmodels (ARIMA)
- **PDF Extraction**: Camelot (stream/lattice modes)
- **Forecasting**: ARIMA time series modeling

---

## 📥 Setup Instructions

### 🔹 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

### 🔹 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Visit the app at: [http://localhost:3000](http://localhost:3000)

---

## 📤 Uploading PDFs

Use the **Upload PDFs** button to select and send multiple annual reports. Once uploaded:

- Financial tables are extracted using Camelot
- Cleaned and structured data is saved as `assets/processed/financial_data.csv`
- Processed data becomes immediately available for charting and forecasting

---

## 📎 API Endpoints

| Method | Endpoint                | Description                         |
| ------ | ----------------------- | ----------------------------------- |
| POST   | `/api/extract`          | Upload and extract financial data   |
| GET    | `/api/financials`       | Fetch processed financial data      |
| GET    | `/api/forecast?metric=` | Predict future values using ARIMA   |
| GET    | `/api/annotations`      | Key financial event annotations     |
| GET    | `/api/download`         | Download processed CSV from backend |

---

## 👨‍💻 Developer

Built with 💙 by **Isuru Hettiarachchi**

[GitHub](#) • [LinkedIn](#)
