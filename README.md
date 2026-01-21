# 🎬 CNVid2Text - Chinese Text Extractor

A powerful, professional web application for extracting Chinese text from video pages using URL or QR code input.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.12-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.51-red)

## ✨ Features

- 🔗 **URL Extraction**: Extract Chinese text directly from video page URLs
- 📸 **QR Code Support**: Upload QR code images containing video URLs
- 📊 **Text Analysis**: Real-time statistics and analysis of extracted text
- 💾 **Multiple Export Formats**: Download as TXT or JSON
- 📜 **History Tracking**: Keep track of all your extractions
- 🎨 **Modern UI**: Professional, user-friendly interface with gradient design
- ⚡ **Fast & Accurate**: Optimized text extraction algorithm
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/kheanvesal/CNVid2Text.git
   cd CNVid2Text
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

### Alternative: Run Flask Version

```bash
python api/app.py
```
Then open `http://127.0.0.1:5000` in your browser.

## 📖 How to Use

### Method 1: URL Input
1. Navigate to the **Extract** tab
2. Paste a video page URL (e.g., from CCTV, news sites)
3. Click **"🚀 Extract from URL"**
4. View the extracted text and statistics
5. Download as TXT or JSON format

### Method 2: QR Code Upload
1. Navigate to the **Extract** tab
2. Upload a QR code image containing a video URL
3. Click **"🔓 Decode & Extract"**
4. The app will decode the QR code and extract text automatically
5. Download or copy the extracted text

### View History
- Click on the **History** tab to view all your previous extractions
- See timestamps, methods used, and text lengths
- Clear history when needed

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python 3.12
- **Web Scraping**: BeautifulSoup4, Requests
- **Image Processing**: Pillow, pyzbar
- **UI Components**: streamlit-option-menu

## 📊 Supported Sources

- 🎬 CCTV Video Pages
- 📰 Chinese News Websites
- 🎥 Video Summary Pages
- 📺 Broadcasting Platforms
- 🔗 Any webpage with Chinese text content

## 🎨 Features Breakdown

### Text Extraction
- Intelligent Chinese character detection
- Removes duplicate content
- Filters out navigation and footer text
- Preserves paragraph structure

### Text Analysis
- Total character count
- Chinese character count
- Line and paragraph count
- Word count statistics

### Export Options
- **TXT Format**: Plain text file with timestamp
- **JSON Format**: Structured data with metadata
  - Source URL
  - Extraction timestamp
  - Full text content
  - Statistics

### History Management
- Automatic tracking of all extractions
- Timestamp for each extraction
- Method used (URL or QR Code)
- Text length information
- Clear history option

## 🔧 Configuration

### Settings (Available in Sidebar)
- **Auto-analyze text**: Automatically analyze extracted text
- **Show statistics**: Display text statistics

## 📝 Project Structure

```
CNVid2Text/
├── api/
│   └── app.py              # Flask application (legacy)
├── streamlit_app.py        # Main Streamlit application
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment config
└── README.md              # This file
```

## 🌟 What's New in Version 2.0

- ✅ Complete Streamlit conversion
- ✅ Enhanced UI with gradient design
- ✅ Real-time text analysis
- ✅ Multiple export formats (TXT, JSON)
- ✅ Extraction history tracking
- ✅ Improved QR code handling with preview
- ✅ Statistics dashboard
- ✅ Professional styling with custom CSS
- ✅ Responsive design
- ✅ Better error handling

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**InsightCode Academy**

## 🙏 Acknowledgments

- Thanks to all contributors
- Built with Streamlit
- Powered by Python

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

<div align="center">
  <p>Made with ❤️ by InsightCode Academy</p>
  <p>© 2026 CNVid2Text - All Rights Reserved</p>
</div>
