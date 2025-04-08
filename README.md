# UT-Test

Automated UI testing project using Appium and Pytest.

## 🚀 Overview
This project is built using Python and Appium to automate tests for a sample mobile application. The tests are structured using the **Page Object Model (POM)** pattern to ensure better maintainability and readability. Each page object encapsulates element locators and interactions.

Tests are grouped into different classes and categories like forms testing and drag-and-drop puzzle validation. They cover various types of inputs, toggle behavior, drag-and-drop interactions, and resetting or solving game states.

## 🧪 Tech Stack
- **Python 3.10+**
- **Pytest** (test framework)
- **Appium** (for mobile automation)
- **Allure** (for rich test reporting)
- **Logging** (built-in Python logging with CLI output)

## 📂 Project Structure
```
UT-Test/
│
├── apk/                     # APK files (only one committed)
├── pages/                   # Page object classes
│   ├── base_page.py         # Base page with shared logic
│   ├── forms_page.py        # Forms interaction logic
│   └── drag_page.py         # Drag & drop puzzle logic
│
├── tests/                   # Test classes
│   ├── test_forms_input.py
│   └── test_drag_and_drop.py
│
├── utils/                   # Helpers
│   └── logger.py            # Logger configuration
│
├── requirements.txt         # Project dependencies
├── pytest.ini               # Pytest config with logging and markers
└── README.md                # You're here!
```

## ⚙️ Setup Instructions

1. **Clone the repo**:
```bash
git clone https://github.com/your-user/UT-Test.git
cd UT-Test
```

2. **Place the APK file**:
   - Put your `.apk` file into the `apk/` folder.
   - Rename the file to: `test.apk` (must match the path in `conftest.py`).

3. **Set device/emulator name**:
   - Open `conftest.py`
   - Set the correct `deviceName` (e.g., `emulator-5554` or one from `adb devices` output):
     ```python
     options.set_capability("deviceName", "your_device_id_here")
     ```

4. **Create and activate a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

5. **Install dependencies**:
```bash
pip install -r requirements.txt
```

6. **Run the tests**:
```bash
pytest .
```

7. **Generate Allure report**:
```bash
allure serve allure-results
```

## ✅ ToDo List

1. Add fixtures inside tests for shared setup
2. Dockerize the project
3. Set up BrowserStack execution
4. Add report generation & publishing via GitHub Actions
5. Optional: TestRail integration
6. Expand test coverage: negative paths, performance, edge cases

---

Happy Testing! 🧪
