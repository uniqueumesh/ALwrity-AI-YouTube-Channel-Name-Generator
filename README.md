# 🎬 ALwrity AI YouTube Channel Name Generator

A free and open-source AI-powered tool for generating unique YouTube channel names and logos. Built with Streamlit and powered by Gemini 2.5 Flash.

## ✨ Features

- **Smart Name Generation**: AI-powered YouTube channel name suggestions
- **Logo Creation**: Generate professional logos with multiple styles
- **Multi-language Support**: Generate names in various languages
- **Export Options**: Download names as CSV or Excel files
- **Fallback System**: Always generates names, even when API is unavailable
- **No API Required**: Works with or without Gemini API key

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ALwrity-AI-YouTube-Channel-Name-Generator.git
   cd ALwrity-AI-YouTube-Channel-Name-Generator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run youtube_name_generator.py
   ```

4. **Open your browser:**
   - Navigate to `http://localhost:8501`
   - Start generating YouTube channel names!

## 📁 Project Structure

```
ALwrity-AI-YouTube-Channel-Name-Generator/
├── youtube_name_generator.py    # Main application
├── logo_generator.py            # Logo generation module
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── LICENSE                      # MIT License
```

## 🎯 How to Use

### 1. **Generate Channel Names**
- Enter your channel description
- Select language and tone
- Choose number of names (5-20)
- Click "Generate YouTube Channel Names"

### 2. **Create Logos** (Optional)
- Select names from generated list
- Choose logo style (Minimal, Bold, Playful, etc.)
- Pick color palette and font
- Generate and download SVG logos

### 3. **Export Results**
- Download names as CSV or Excel
- Download individual logos as SVG files

## 🔧 Configuration

### API Configuration
- **Default**: Uses built-in fallback system (no API key needed)
- **Enhanced**: Add your Gemini API key for AI-powered generation
- **Get API Key**: [Google AI Studio](https://aistudio.google.com/app/apikey)

### Logo Styles
- **Minimal**: Clean, simple design
- **Bold**: Strong typography with effects
- **Playful**: Colorful elements and gradients
- **Professional**: Structured layout with borders
- **Modern**: Geometric shapes and gradients
- **Retro**: Vintage styling with patterns
- **Gradient**: Beautiful color transitions

## 🛠️ Technical Details

### Dependencies
- `streamlit`: Web application framework
- `google-generativeai`: Gemini API integration
- `pandas`: Data manipulation
- `orjson`: Fast JSON processing
- `tenacity`: Retry logic for API calls

### Architecture
- **Single-file design**: Easy to understand and modify
- **Modular logo system**: Separate logo generation module
- **Robust fallback**: Always generates results
- **Session persistence**: Maintains state across interactions

## 🎨 Logo Generation

### Template-based Logos
- **7 different styles** with customizable options
- **Color palettes**: Monochrome, Warm, Cool, Vibrant
- **Font options**: Inter, Poppins, Montserrat, Roboto Slab, Abril Fatface
- **SVG output**: Scalable vector graphics

### AI-assisted Logos
- **Gemini 2.5 Flash integration** for creative logos
- **Fallback to templates** if AI generation fails
- **User-controlled API usage** with custom API keys

## 📤 Export Options

### Name Export
- **CSV format**: Spreadsheet-compatible
- **Excel format**: Professional formatting
- **Bulk download**: All names in one file

### Logo Export
- **SVG format**: Scalable vector graphics
- **Individual downloads**: Per-name logo files
- **High resolution**: 1024px or 2048px options

## 🔒 Privacy & Security

- **No data storage**: Names and logos generated locally
- **API key security**: Keys stored only in session state
- **No tracking**: Completely private usage
- **Open source**: Full transparency

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ALwrity Team**: For creating this amazing tool
- **Google**: For the Gemini AI API
- **Streamlit**: For the excellent web framework
- **Open Source Community**: For inspiration and support

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ALwrity-AI-YouTube-Channel-Name-Generator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ALwrity-AI-YouTube-Channel-Name-Generator/discussions)
- **Email**: support@alwrity.com

## 🗺️ Roadmap

- [ ] **Multi-language logo support**
- [ ] **Advanced logo customization**
- [ ] **Name availability checking**
- [ ] **Social media integration**
- [ ] **Team collaboration features**

---

**Made with ❤️ by the ALwrity Team**

*Free • Open Source • AI-Powered*