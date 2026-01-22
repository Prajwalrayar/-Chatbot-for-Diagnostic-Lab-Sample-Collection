# 🧪 Chatbot for Diagnostic Lab Sample Collection

A modern, AI-powered chatbot built with **Streamlit** for booking diagnostic lab tests with intelligent PDF Q&A capabilities using semantic search.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## ✨ Features

### 🤖 Smart Chatbot
- Interactive conversational interface for booking lab tests
- Multi-step booking flow with validation
- Real-time slot availability checking

### 📄 PDF Document Q&A
- Upload lab reports/documents and ask questions
- **Semantic search** using Sentence Transformers
- Three response modes:
  - 📖 **Detailed Explanation** - Comprehensive analysis
  - 📝 **Short Summary** - Quick overview
  - ❓ **Ask Questions** - Interactive Q&A

### 📊 Admin Dashboard
- View all bookings with statistics
- Download bookings as CSV
- Password-protected access

### 🎨 Modern UI
- Professional flowing gradient theme
- Animated mesh background
- Glass morphism design
- Fully responsive layout

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web framework |
| **SQLite** | Database |
| **Sentence Transformers** | Semantic embeddings |
| **scikit-learn** | Cosine similarity |
| **PyPDF** | PDF text extraction |

---

## 📁 Project Structure

```
Booking_Chatbot_for_lab/
├── app/
│   ├── main.py              # Main Streamlit application
│   ├── admin_dashboard.py   # Admin panel
│   ├── booking_flow.py      # Booking logic
│   ├── chat_logic.py        # Chat handling
│   ├── config.py            # Configuration
│   ├── rag_pipeline.py      # RAG implementation
│   └── tools.py             # Utility functions
├── db/
│   ├── database.py          # SQLite operations
│   ├── models.py            # Data models
│   └── bookings.db          # SQLite database
├── .streamlit/
│   └── config.toml          # Streamlit config
├── requirements.txt         # Dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Prajwalrayar/-Chatbot-for-Diagnostic-Lab-Sample-Collection.git
cd -Chatbot-for-Diagnostic-Lab-Sample-Collection
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

---

## 📦 Requirements

```txt
streamlit>=1.28.0
pypdf>=3.17.0
sentence-transformers>=2.2.0
scikit-learn>=1.3.0
pandas>=2.0.0
```

---

## 🔧 Configuration

### Available Lab Tests
- Complete Blood Count (CBC)
- Blood Sugar (Fasting/PP)
- HbA1c
- Lipid Profile
- Liver Function Test (LFT)
- Kidney Function Test (KFT)

### Test Centers
- Apollo Diagnostics (Jayanagar, BTM Layout)
- Manipal TRUtest (Yeshwanthpur, Whitefield)
- Dr Lal PathLabs (Indiranagar, BTM Layout)
- Metropolis Healthcare (Jayanagar)
- Neuberg Anand Reference Laboratory (Koramangala)

---

## 📸 Screenshots

### Booking Flow
- Step-by-step test booking with date/time selection
- Real-time slot availability (max 2 per slot)
- Email and phone validation

### Document Q&A
- Upload PDF → Automatic summary generation
- Ask natural language questions
- Semantic search for accurate answers

---

## 👨‍💻 Author

**Prajwal Rayar**

- GitHub: [@Prajwalrayar](https://github.com/Prajwalrayar)

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Sentence Transformers](https://www.sbert.net/) for semantic search
- [Hugging Face](https://huggingface.co/) for ML models

---

⭐ **Star this repo if you find it helpful!**
