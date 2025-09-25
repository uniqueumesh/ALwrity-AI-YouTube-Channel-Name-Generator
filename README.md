# ALwrity AI YouTube Channel Name Generator

A free, open-source Streamlit app that generates creative YouTube channel name ideas using Google's Gemini 2.5 Flash model. Perfect for content creators looking for brandable channel names.

## Features

- **Simple UI**: Single-screen interface with no sidebar - perfect for non-technical users
- **Multilingual Support**: Generate names in English, Hindi, French, Spanish, German, Arabic, Portuguese, Bengali, Japanese, Korean, or any custom language
- **Customizable Options**: 
  - Choose tone (Friendly, Professional, Casual, Educational, Playful, Bold, or custom)
  - Select number of name variants (5, 10, 15, or 20)
  - Optional explanations for each generated name
- **Smart Filtering**: Automatically filters out sentences and long phrases to ensure you get short, brandable names
- **Shortlist Feature**: Save your favorite names and export them
- **Privacy-Focused**: Your API key is only stored in your browser session

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ALwrity-AI-YouTube-Channel-Name-Generator.git
   cd ALwrity-AI-YouTube-Channel-Name-Generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   streamlit run main.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, copy the URL from the terminal

## How to Use

1. **Enter your channel description**
   - Describe what your channel is about (e.g., "Tutorials for beginners on Python and data science")

2. **Select your preferences**
   - Choose the language for your channel names
   - Pick the number of name variants you want (5, 10, 15, or 20)
   - Select the tone that matches your brand
   - Optionally enable explanations to understand the meaning behind each name

3. **Add your Gemini API key**
   - Paste your Google Gemini API key in the password field
   - Your key is only stored in your browser session and never saved

4. **Generate names**
   - Click "Generate Name Ideas" and wait for the AI to create your channel names
   - Each name comes with action buttons to copy or add to your shortlist

5. **Manage your favorites**
   - Use the shortlist feature to save names you like
   - Copy individual names or export your entire shortlist

## Project Structure

```
├── app/
│   ├── ui/           # Streamlit UI components
│   ├── core/         # Business logic and prompt building
│   ├── services/     # Gemini API integration
│   ├── utils/        # Helper functions
│   └── state/        # Session state management
├── .streamlit/       # Streamlit configuration
├── main.py           # Application entry point
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Configuration

The app uses a modular architecture that separates concerns:

- **UI Layer** (`app/ui/`): Pure Streamlit interface with no business logic
- **Core Layer** (`app/core/`): Prompt building, validation, and response parsing
- **Services Layer** (`app/services/`): External API calls and network operations
- **Utils Layer** (`app/utils/`): Helper functions and session management

## API Key Security

- Your Gemini API key is only stored in your browser's session state
- It's never saved to disk or transmitted to any external servers
- The key is only used for the current session and disappears when you close the browser

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'app'"**
   - Make sure you're running from the project root directory
   - Use `streamlit run main.py` (not `streamlit run app/ui/main.py`)

2. **"Generation failed" error**
   - Check that your Gemini API key is valid and has quota remaining
   - Ensure you have an active internet connection

3. **No names generated**
   - Try adjusting your channel description to be more specific
   - Check that your API key has sufficient quota

### Getting Help

- Check the [Issues](https://github.com/your-username/ALwrity-AI-YouTube-Channel-Name-Generator/issues) page for common problems
- Create a new issue if you encounter a bug
- Check the [PLAN.md](PLAN.md) file for detailed technical specifications

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini 2.5 Flash](https://ai.google.dev/)
- Part of the ALwrity open-source AI tools collection

## Roadmap

- [ ] Add more language options
- [ ] Implement domain availability checking
- [ ] Add name history and favorites persistence
- [ ] Create name logo mockups
- [ ] Add team collaboration features

---

**Made with ❤️ by the ALwrity Team**

*Free • Open Source • No Registration Required*