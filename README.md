# Selenium_Automation 🛍️

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-Latest-green.svg)](https://www.selenium.dev/)
[![POM](https://img.shields.io/badge/Design-PageObjectModel-orange.svg)](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)

A comprehensive testing and web automation suite that combines intelligent web scraping for coupon aggregation and robust API testing capabilities. Built with scalability, modularity, and industry best practices in mind.

## 🌟 Key Features

- **Dual-Purpose Architecture**
  - Web Scraping Engine for coupon data aggregation
  - API Testing Framework for endpoint validation
- **Modern Design Patterns**
  - Page Object Model (POM) implementation
  - Modular and extensible architecture
  - Provider-specific handlers
- **Comprehensive Testing**
  - Automated API endpoint validation
  - Schema and data consistency checks
  - Detailed test reporting
- **Enterprise-Grade Infrastructure**
  - Scalable design for high-volume data processing
  - Isolated development environments
  - Automated setup and configuration

## 📚 Project Components

The project consists of two main components:

### 1. Web Scraping Engine
- Automated coupon data collection
- Multiple provider support
- Custom handler implementation
- [Learn more about the Scraper](./Scraper/README.md)

### 2. API Testing Framework
- Comprehensive endpoint validation
- Data consistency verification
- Automated test reporting
- [View detailed test cases](./TEST_CASES.md)

## 🗂️ Project Structure

```
├── Scraper/
│   ├── pages/
│   │   ├── base/          # Base classes and common functionality
│   │   ├── jemix/         # Jemix provider implementation
│   ├── config/            # Configuration settings
│   └── Selenium_Test.sh   # Environment setup script
├── potter_api/
│   ├── api_get.py         # Books API test implementation
│   ├── api_houses.py      # Houses API test implementation
│   ├── api_modules.py     # Shared configurations
│   ├── execute_tests.py   # Test orchestrator
│   └── test_utils.py      # Testing utilities
└── test_results/          # Generated test reports
```

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.x
- Unix-like environment (WSL for Windows users)
- Chrome/Firefox browser installed

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/Intelli-Shop.git
cd Intelli-Shop

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Unix/Linux/WSL
# OR
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Settings
- Update `Scraper/config/settings.py` with your preferences
- Configure API endpoints in `potter_api/api_modules.py`

### 4. Run Tests
```bash
# Run web scraping tests
cd Scraper
./Selenium_Test.sh

# Run API tests
cd ../potter_api
python execute_tests.py
```

## 🧪 Testing Framework

### API Testing Capabilities
- **Endpoint Coverage**:
  - Books API (`/books`)
  - Houses API (`/houses`)
- **Validation Types**:
  - Schema validation
  - Data consistency
  - Pagination handling
  - Error scenarios
  - Response headers

### Web Scraping Tests
- **Provider Coverage**:
  - Jemix implementation
  - Extensible for additional providers
- **Validation Areas**:
  - Data extraction accuracy
  - Error handling
  - Performance metrics

## 📊 Test Results

Test execution generates detailed reports:
- `API-Test-Result.txt`: API test outcomes
- `Scraper-Test-Result.txt`: Web scraping results

Reports include:
- Test case status (Pass/Fail)
- Detailed error messages
- Execution statistics
- Performance metrics

## 🔗 Additional Resources

- [Detailed Test Cases](./TEST_CASES.md)
- [API Documentation](./Scraper/API_README.md)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Python Best Practices](https://docs.python-guide.org/)
