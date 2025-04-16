bookbit/
├── books/                          # 📚 All uploaded EPUB files will be stored here
│   └── (user uploads go here)
│
├── flask_config/                   # 🔥 All Flask-specific logic and route handling
│   ├── __init__.py                 # Flask app factory: creates and configures the Flask app
│   ├── views/
│   │   ├── index.py                # Route: renders the main book list and search
│   │   └── files.py                # Route: handles file uploads and downloads
│   └── logic/
│       ├── auth.py                 # Authentication helpers (login_required, check_password, etc.)
│       └── fileops.py              # File management: list books, sort, format metadata
│
├── images/                         # 🖼️ Static image assets like logos
│   └── logo.png                    # Bookbit logo (optional, can be omitted)
│
├── internal/                       # 🔒 Internal-only files (do NOT edit manually)
│   ├── constants.py                # Global constants used across the app
│   └── default.ini                 # Optional fallback/default config (used if settings.ini is missing)
│
├── layout/                         # 🧱 UI building blocks: layout and styling
│   ├── header.html                 # Top of the HTML page (title, nav, search form)
│   ├── body.html                   # Main content block (book table and upload toggle)
│   ├── footer.html                 # Bottom of the HTML page (scripts, closing tags)
│   └── style.css                   # All CSS styles (mobile, dark/light, typography, etc.)
│
├── settings.ini                    # 📝 Main config file the user edits (domain, auth, display, etc.)
│
├── setup.sh                        # 🛠️ One-click setup script
│                                   # - Reads settings.ini
│                                   # - Generates nginx + systemd config
│                                   # - Builds templates from layout/
│                                   # - Sets up install paths
│
├── run.py                          # 🚀 Entry point that runs the Flask app
│                                   # Used by systemd (via ExecStart)
│
├── requirements.txt                # 📦 Python dependencies (Flask, bcrypt, etc.)
