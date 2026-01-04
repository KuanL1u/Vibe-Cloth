# ✨ Aura & Threads

An AI-powered personal styling application that analyzes your selfie using GPT-4o Vision and recommends personalized fashion items from your favorite brands.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)

## 🌟 Features

- **AI-Powered Analysis**: Uses GPT-4o Vision to analyze your features including skin tone, face shape, and body build
- **Personalized Recommendations**: Get tailored outfit suggestions consisting of 3 cohesive items (Top, Bottom, Shoes/Accessory)
- **Brand-Specific Search**: Search for items from your favorite brands (Zara, Uniqlo, Gucci, etc.)
- **Real Product Results**: Automatically searches and displays actual products with images and shopping links
- **Beautiful UI**: Modern, elegant interface with smooth animations and responsive design

## 🚀 Demo

1. Upload a clear selfie
2. Enter your preferred fashion brand
3. Let the AI stylist create your personalized look!

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/KuanL1u/gemini.git
cd gemini
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:

Create a `.streamlit/secrets.toml` file in the project root:
```toml
OPENAI_API_KEY = "your-api-key-here"
```

Or enter it directly in the app's sidebar when running.

## 🎯 Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to the provided URL (typically `http://localhost:8501`)

3. Follow the on-screen instructions:
   - Upload a selfie
   - Enter your favorite brand
   - Click "Generate Recommendations"

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4o Vision
- **Image Search**: DuckDuckGo Image Search (DDGS)
- **Image Processing**: Pillow

## 📁 Project Structure

```
gemini/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore         # Git ignore rules
├── .streamlit/        # Streamlit configuration
│   └── secrets.toml   # API keys (not tracked)
└── README.md          # This file
```

## 🎨 How It Works

1. **Image Analysis**: Your selfie is encoded and sent to GPT-4o Vision
2. **AI Styling**: The AI analyzes your features and suggests a cohesive outfit
3. **Product Search**: Each recommendation is searched using DuckDuckGo
4. **Display**: Results are displayed with product images and shopping links

## ⚙️ Configuration

The app uses GPT-5.2 model (line 124 in `app.py`). You can modify this by changing:
```python
model="gpt-5.2-2025-12-11"  # Change to your preferred model
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI for GPT-4o Vision API
- Streamlit for the amazing web framework
- DuckDuckGo for image search capabilities

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ using AI

