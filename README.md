# Intelli-Shop

A web scraping solution for aggregating and managing coupon data from multiple providers. 
Built with scalability and modularity in mind.

## 🚀 Features

- **Modular Architecture**: Easy to extend and add new coupon providers
- **Scalable Design**: Built to handle increasing numbers of sources and data volume
- **Provider-Specific Handlers**: Custom handlers for each coupon provider's unique structure
- **Data Validation**: Ensures consistency and reliability of collected coupon data

## 🛠️ Technology Stack

- **Python**: Core programming language
- **Selenium**: Web automation and data extraction
- **Object-Oriented Design**: Modular and maintainable code structure
- **Virtual Environment**: Isolated development environment

## 📁 Project Structure

```
Intelli-Shop/
├── Scraper/
│   ├── pages/
│   │   ├── base/         # Base classes and common functionality
│   │   ├── jemix/        # Jemix provider implementation
│   ├── config/           # Configuration settings
│   ├── Selenium_Test.sh  # Development environment setup script
│   └── venv/            # Virtual environment
```

## 🚦 Getting Started

1. **Set Up Development Environment**
   ```bash
   cd Scraper
   # For Unix/Linux/WSL users:
   ./Selenium_Test.sh    # Sets up required dependencies and environment
   
   # For Windows users:
   python -m venv venv
   venv\Scripts\activate
   pip install selenium webdriver-manager
   ```

2. **Configure Settings**
   - Update `config/settings.py` with your preferred configuration
   - Set up provider-specific parameters if needed

## 🔧 Usage

The project is structured to handle different coupon providers through dedicated modules:

```python
from Scraper.pages.jemix.HomePage import HomePage
# Initialize and use the scraper for specific providers
```

## 🌱 Adding New Providers

1. Create a new directory under `pages/` for the provider
2. Implement provider-specific classes extending the base functionality
3. Add configuration in `config/settings.py`

## 💻 Development

The project includes development scripts to ensure proper setup:

- `Selenium_Test.sh`: Automates environment setup and dependency management
  - Creates isolated virtual environment
  - Installs required packages
  - Sets up necessary browser configurations
  - Ensures consistent development environment across team members
