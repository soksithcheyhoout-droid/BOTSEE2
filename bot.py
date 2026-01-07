import logging
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8582612703:AAGexifIxTWXRU4dDTMGXxzLmTQVVVjNitE"
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

user_cache = {}

# Complete guides with REAL working methods for everyone
FRAMEWORK_GUIDES = {
    "laravel": {
        "name": "Laravel",
        "description": "PHP Web Framework",
        "windows": [
            "📥 Step 1: Download & Install PHP",
            "https://windows.php.net/download/",
            "Download VS16 x64 Thread Safe ZIP",
            "Extract to C:\\php",
            "Add C:\\php to System PATH",
            "",
            "📥 Step 2: Download & Install Composer",
            "https://getcomposer.org/Composer-Setup.exe",
            "Run installer - it finds PHP automatically",
            "",
            "✅ Step 3: Verify Installation",
            "php --version",
            "composer --version",
            "",
            "🚀 Step 4: Create Laravel Project",
            "composer create-project laravel/laravel my-project",
            "cd my-project",
            "php artisan serve",
            "",
            "⚡ Useful Commands:",
            "php artisan make:controller UserController",
            "php artisan make:model User -m",
            "php artisan migrate",
            "php artisan serve --port=8080"
        ],
        "linux": [
            "📥 Step 1: Install PHP",
            "sudo apt update",
            "sudo apt install php php-cli php-mbstring php-xml php-curl php-zip unzip -y",
            "",
            "📥 Step 2: Install Composer",
            "curl -sS https://getcomposer.org/installer | php",
            "sudo mv composer.phar /usr/local/bin/composer",
            "",
            "✅ Step 3: Verify Installation",
            "php --version",
            "composer --version",
            "",
            "🚀 Step 4: Create Laravel Project",
            "composer create-project laravel/laravel my-project",
            "cd my-project",
            "php artisan serve",
            "",
            "⚡ Useful Commands:",
            "php artisan make:controller UserController",
            "php artisan make:model User -m",
            "php artisan migrate",
            "php artisan serve --port=8080"
        ],
        "docs": "https://laravel.com/docs"
    },
    "composer": {
        "name": "Composer",
        "description": "PHP Package Manager",
        "windows": [
            "📥 Step 1: Install PHP First",
            "https://windows.php.net/download/",
            "Download VS16 x64 Thread Safe ZIP",
            "Extract to C:\\php",
            "Add C:\\php to System PATH",
            "",
            "📥 Step 2: Download Composer Installer",
            "https://getcomposer.org/Composer-Setup.exe",
            "Run the installer",
            "It will find PHP automatically",
            "",
            "✅ Step 3: Verify",
            "composer --version",
            "",
            "⚡ Useful Commands:",
            "composer require <package>",
            "composer install",
            "composer update"
        ],
        "linux": [
            "📥 Step 1: Install PHP",
            "sudo apt update",
            "sudo apt install php php-cli -y",
            "",
            "📥 Step 2: Install Composer",
            "curl -sS https://getcomposer.org/installer | php",
            "sudo mv composer.phar /usr/local/bin/composer",
            "",
            "✅ Step 3: Verify",
            "composer --version",
            "",
            "⚡ Useful Commands:",
            "composer require <package>",
            "composer install",
            "composer update"
        ],
        "docs": "https://getcomposer.org/"
    },
    "php": {
        "name": "PHP",
        "description": "Server-side Language",
        "windows": [
            "📥 Step 1: Download PHP",
            "https://windows.php.net/download/",
            "Choose: VS16 x64 Thread Safe (ZIP)",
            "",
            "📦 Step 2: Extract",
            "Extract ZIP to C:\\php",
            "",
            "⚙️ Step 3: Add to PATH",
            "Open: System Properties > Environment Variables",
            "Edit PATH > Add: C:\\php",
            "",
            "📝 Step 4: Configure (Optional)",
            "Copy php.ini-development to php.ini",
            "Enable extensions in php.ini",
            "",
            "✅ Step 5: Verify",
            "php --version"
        ],
        "linux": [
            "📥 Step 1: Install PHP",
            "sudo apt update",
            "sudo apt install php php-cli php-fpm -y",
            "",
            "📦 Step 2: Install Common Extensions",
            "sudo apt install php-mysql php-mbstring php-xml php-curl -y",
            "",
            "✅ Step 3: Verify",
            "php --version"
        ],
        "docs": "https://www.php.net/"
    },
    "nodejs": {
        "name": "Node.js",
        "description": "JavaScript Runtime",
        "windows": [
            "📥 Step 1: Download Node.js",
            "https://nodejs.org/",
            "Click 'Download LTS' button",
            "Run the .msi installer",
            "",
            "✅ Step 2: Verify Installation",
            "node --version",
            "npm --version",
            "",
            "⚡ Useful Commands:",
            "npm init -y",
            "npm install <package>",
            "npm install -g <package>",
            "npm run <script>"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "Or use NodeSource (newer version):",
            "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -",
            "sudo apt install nodejs -y",
            "",
            "✅ Step 2: Verify",
            "node --version",
            "npm --version",
            "",
            "⚡ Useful Commands:",
            "npm init -y",
            "npm install <package>",
            "sudo npm install -g <package>"
        ],
        "docs": "https://nodejs.org/"
    },
    "react": {
        "name": "React",
        "description": "JavaScript UI Library",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "Download and install LTS version",
            "",
            "✅ Step 2: Verify Node.js",
            "node --version",
            "npm --version",
            "",
            "🚀 Step 3: Create React App",
            "npx create-react-app my-app",
            "cd my-app",
            "npm start",
            "",
            "⚡ Useful Commands:",
            "npm install axios",
            "npm install react-router-dom",
            "npm run build",
            "npm test"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "✅ Step 2: Verify",
            "node --version",
            "npm --version",
            "",
            "🚀 Step 3: Create React App",
            "npx create-react-app my-app",
            "cd my-app",
            "npm start",
            "",
            "⚡ Useful Commands:",
            "npm install axios",
            "npm install react-router-dom",
            "npm run build"
        ],
        "docs": "https://react.dev/"
    },
    "vue": {
        "name": "Vue.js",
        "description": "JavaScript Framework",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "Download and install LTS version",
            "",
            "✅ Step 2: Verify",
            "node --version",
            "",
            "🚀 Step 3: Create Vue App",
            "npm create vue@latest my-app",
            "cd my-app",
            "npm install",
            "npm run dev",
            "",
            "⚡ Useful Commands:",
            "npm install vue-router",
            "npm install pinia",
            "npm run build"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "✅ Step 2: Verify",
            "node --version",
            "",
            "🚀 Step 3: Create Vue App",
            "npm create vue@latest my-app",
            "cd my-app",
            "npm install",
            "npm run dev",
            "",
            "⚡ Useful Commands:",
            "npm install vue-router",
            "npm install pinia",
            "npm run build"
        ],
        "docs": "https://vuejs.org/"
    },
    "angular": {
        "name": "Angular",
        "description": "Web Application Platform",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "Download and install LTS version",
            "",
            "📦 Step 2: Install Angular CLI",
            "npm install -g @angular/cli",
            "",
            "🚀 Step 3: Create Angular App",
            "ng new my-app",
            "cd my-app",
            "ng serve",
            "",
            "⚡ Useful Commands:",
            "ng generate component my-component",
            "ng generate service my-service",
            "ng build",
            "ng test"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "📦 Step 2: Install Angular CLI",
            "sudo npm install -g @angular/cli",
            "",
            "🚀 Step 3: Create Angular App",
            "ng new my-app",
            "cd my-app",
            "ng serve",
            "",
            "⚡ Useful Commands:",
            "ng generate component my-component",
            "ng generate service my-service",
            "ng build"
        ],
        "docs": "https://angular.io/"
    },
    "nextjs": {
        "name": "Next.js",
        "description": "React Framework",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "Download and install LTS version",
            "",
            "🚀 Step 2: Create Next.js App",
            "npx create-next-app@latest my-app",
            "cd my-app",
            "npm run dev",
            "",
            "⚡ Useful Commands:",
            "npm run build",
            "npm start",
            "npm run lint"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "🚀 Step 2: Create Next.js App",
            "npx create-next-app@latest my-app",
            "cd my-app",
            "npm run dev",
            "",
            "⚡ Useful Commands:",
            "npm run build",
            "npm start"
        ],
        "docs": "https://nextjs.org/"
    },
    "express": {
        "name": "Express.js",
        "description": "Node.js Web Framework",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "Download and install LTS version",
            "",
            "📁 Step 2: Create Project",
            "mkdir my-app",
            "cd my-app",
            "npm init -y",
            "",
            "📦 Step 3: Install Express",
            "npm install express",
            "",
            "🚀 Step 4: Create app.js and run",
            "node app.js",
            "",
            "⚡ Useful Packages:",
            "npm install cors",
            "npm install body-parser",
            "npm install mongoose",
            "npm install dotenv"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt update",
            "sudo apt install nodejs npm -y",
            "",
            "📁 Step 2: Create Project",
            "mkdir my-app",
            "cd my-app",
            "npm init -y",
            "",
            "📦 Step 3: Install Express",
            "npm install express",
            "",
            "🚀 Step 4: Create app.js and run",
            "node app.js",
            "",
            "⚡ Useful Packages:",
            "npm install cors",
            "npm install mongoose",
            "npm install dotenv"
        ],
        "docs": "https://expressjs.com/"
    },
    "python": {
        "name": "Python",
        "description": "Programming Language",
        "windows": [
            "📥 Step 1: Download Python",
            "https://www.python.org/downloads/",
            "Click 'Download Python 3.x'",
            "",
            "⚠️ IMPORTANT during install:",
            "✅ Check 'Add Python to PATH'",
            "",
            "✅ Step 2: Verify Installation",
            "python --version",
            "pip --version",
            "",
            "⚡ Useful Commands:",
            "pip install <package>",
            "python -m venv venv",
            "venv\\Scripts\\activate",
            "pip freeze > requirements.txt"
        ],
        "linux": [
            "📥 Step 1: Install Python",
            "sudo apt update",
            "sudo apt install python3 python3-pip python3-venv -y",
            "",
            "✅ Step 2: Verify",
            "python3 --version",
            "pip3 --version",
            "",
            "⚡ Useful Commands:",
            "pip3 install <package>",
            "python3 -m venv venv",
            "source venv/bin/activate",
            "pip freeze > requirements.txt"
        ],
        "docs": "https://www.python.org/"
    },
    "django": {
        "name": "Django",
        "description": "Python Web Framework",
        "windows": [
            "📥 Step 1: Install Python First",
            "https://www.python.org/downloads/",
            "✅ Check 'Add Python to PATH'",
            "",
            "📦 Step 2: Install Django",
            "pip install django",
            "",
            "🚀 Step 3: Create Project",
            "django-admin startproject myproject",
            "cd myproject",
            "python manage.py runserver",
            "",
            "⚡ Useful Commands:",
            "python manage.py startapp myapp",
            "python manage.py makemigrations",
            "python manage.py migrate",
            "python manage.py createsuperuser",
            "python manage.py shell"
        ],
        "linux": [
            "📥 Step 1: Install Python",
            "sudo apt update",
            "sudo apt install python3 python3-pip -y",
            "",
            "📦 Step 2: Install Django",
            "pip3 install django",
            "",
            "🚀 Step 3: Create Project",
            "django-admin startproject myproject",
            "cd myproject",
            "python3 manage.py runserver",
            "",
            "⚡ Useful Commands:",
            "python3 manage.py startapp myapp",
            "python3 manage.py makemigrations",
            "python3 manage.py migrate",
            "python3 manage.py createsuperuser"
        ],
        "docs": "https://docs.djangoproject.com/"
    },
    "flask": {
        "name": "Flask",
        "description": "Python Micro Framework",
        "windows": [
            "📥 Step 1: Install Python First",
            "https://www.python.org/downloads/",
            "✅ Check 'Add Python to PATH'",
            "",
            "📦 Step 2: Install Flask",
            "pip install flask",
            "",
            "🚀 Step 3: Create app.py and run",
            "python app.py",
            "",
            "⚡ Useful Packages:",
            "pip install flask-sqlalchemy",
            "pip install flask-login",
            "pip install flask-wtf"
        ],
        "linux": [
            "📥 Step 1: Install Python",
            "sudo apt update",
            "sudo apt install python3 python3-pip -y",
            "",
            "📦 Step 2: Install Flask",
            "pip3 install flask",
            "",
            "🚀 Step 3: Create app.py and run",
            "python3 app.py",
            "",
            "⚡ Useful Packages:",
            "pip3 install flask-sqlalchemy",
            "pip3 install flask-login"
        ],
        "docs": "https://flask.palletsprojects.com/"
    },
    "fastapi": {
        "name": "FastAPI",
        "description": "Modern Python API Framework",
        "windows": [
            "📥 Step 1: Install Python First",
            "https://www.python.org/downloads/",
            "✅ Check 'Add Python to PATH'",
            "",
            "📦 Step 2: Install FastAPI",
            "pip install fastapi uvicorn",
            "",
            "🚀 Step 3: Create main.py and run",
            "uvicorn main:app --reload",
            "",
            "⚡ Useful Packages:",
            "pip install sqlalchemy",
            "pip install python-multipart"
        ],
        "linux": [
            "📥 Step 1: Install Python",
            "sudo apt update",
            "sudo apt install python3 python3-pip -y",
            "",
            "📦 Step 2: Install FastAPI",
            "pip3 install fastapi uvicorn",
            "",
            "🚀 Step 3: Create main.py and run",
            "uvicorn main:app --reload",
            "",
            "⚡ Useful Packages:",
            "pip3 install sqlalchemy"
        ],
        "docs": "https://fastapi.tiangolo.com/"
    },
    "flutter": {
        "name": "Flutter",
        "description": "UI Toolkit for Mobile/Web/Desktop",
        "windows": [
            "📥 Step 1: Download Flutter SDK",
            "https://docs.flutter.dev/get-started/install/windows",
            "Download the ZIP file",
            "Extract to C:\\flutter",
            "",
            "⚙️ Step 2: Add to PATH",
            "Add C:\\flutter\\bin to System PATH",
            "",
            "📥 Step 3: Install Android Studio",
            "https://developer.android.com/studio",
            "",
            "✅ Step 4: Verify",
            "flutter doctor",
            "",
            "🚀 Step 5: Create App",
            "flutter create my_app",
            "cd my_app",
            "flutter run",
            "",
            "⚡ Useful Commands:",
            "flutter pub get",
            "flutter build apk",
            "flutter build web"
        ],
        "linux": [
            "📥 Step 1: Install Flutter",
            "sudo snap install flutter --classic",
            "",
            "📥 Step 2: Install Android Studio",
            "sudo snap install android-studio --classic",
            "",
            "✅ Step 3: Verify",
            "flutter doctor",
            "",
            "🚀 Step 4: Create App",
            "flutter create my_app",
            "cd my_app",
            "flutter run",
            "",
            "⚡ Useful Commands:",
            "flutter pub get",
            "flutter build apk",
            "flutter build web"
        ],
        "docs": "https://flutter.dev/"
    },
    "mongodb": {
        "name": "MongoDB",
        "description": "NoSQL Database",
        "windows": [
            "📥 Step 1: Download MongoDB",
            "https://www.mongodb.com/try/download/community",
            "Download MSI installer",
            "Run installer (Complete setup)",
            "",
            "📥 Step 2: Download MongoDB Shell",
            "https://www.mongodb.com/try/download/shell",
            "",
            "✅ Step 3: Start MongoDB",
            "MongoDB runs as Windows Service automatically",
            "",
            "🚀 Step 4: Connect",
            "mongosh",
            "",
            "⚡ Useful Commands:",
            "show dbs",
            "use mydb",
            "db.users.insertOne({name: 'John'})",
            "db.users.find()"
        ],
        "linux": [
            "📥 Step 1: Install MongoDB",
            "sudo apt update",
            "sudo apt install mongodb -y",
            "",
            "🚀 Step 2: Start MongoDB",
            "sudo systemctl start mongodb",
            "sudo systemctl enable mongodb",
            "",
            "✅ Step 3: Connect",
            "mongosh",
            "",
            "⚡ Useful Commands:",
            "show dbs",
            "use mydb",
            "db.users.insertOne({name: 'John'})",
            "db.users.find()"
        ],
        "docs": "https://www.mongodb.com/docs/"
    },
    "mysql": {
        "name": "MySQL",
        "description": "Relational Database",
        "windows": [
            "📥 Step 1: Download MySQL",
            "https://dev.mysql.com/downloads/installer/",
            "Download MySQL Installer",
            "Run installer > Choose Full or Custom",
            "",
            "✅ Step 2: Connect",
            "mysql -u root -p",
            "",
            "⚡ Useful Commands:",
            "SHOW DATABASES;",
            "CREATE DATABASE mydb;",
            "USE mydb;",
            "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));",
            "SELECT * FROM users;"
        ],
        "linux": [
            "📥 Step 1: Install MySQL",
            "sudo apt update",
            "sudo apt install mysql-server -y",
            "",
            "🚀 Step 2: Start & Secure",
            "sudo systemctl start mysql",
            "sudo mysql_secure_installation",
            "",
            "✅ Step 3: Connect",
            "sudo mysql -u root -p",
            "",
            "⚡ Useful Commands:",
            "SHOW DATABASES;",
            "CREATE DATABASE mydb;",
            "USE mydb;",
            "SELECT * FROM users;"
        ],
        "docs": "https://dev.mysql.com/doc/"
    },
    "postgresql": {
        "name": "PostgreSQL",
        "description": "Advanced Database",
        "windows": [
            "📥 Step 1: Download PostgreSQL",
            "https://www.postgresql.org/download/windows/",
            "Download installer",
            "Run installer",
            "",
            "✅ Step 2: Connect",
            "psql -U postgres",
            "",
            "⚡ Useful Commands:",
            "\\l  (list databases)",
            "CREATE DATABASE mydb;",
            "\\c mydb  (connect to db)",
            "\\dt  (list tables)",
            "SELECT * FROM users;"
        ],
        "linux": [
            "📥 Step 1: Install PostgreSQL",
            "sudo apt update",
            "sudo apt install postgresql postgresql-contrib -y",
            "",
            "🚀 Step 2: Start",
            "sudo systemctl start postgresql",
            "",
            "✅ Step 3: Connect",
            "sudo -u postgres psql",
            "",
            "⚡ Useful Commands:",
            "\\l  (list databases)",
            "CREATE DATABASE mydb;",
            "\\c mydb  (connect to db)",
            "\\dt  (list tables)"
        ],
        "docs": "https://www.postgresql.org/docs/"
    },
    "docker": {
        "name": "Docker",
        "description": "Container Platform",
        "windows": [
            "📥 Step 1: Download Docker Desktop",
            "https://www.docker.com/products/docker-desktop/",
            "Download and install",
            "Restart computer",
            "",
            "✅ Step 2: Verify",
            "docker --version",
            "docker run hello-world",
            "",
            "⚡ Useful Commands:",
            "docker pull <image>",
            "docker run -d -p 8080:80 nginx",
            "docker ps",
            "docker images",
            "docker stop <container>",
            "docker-compose up -d"
        ],
        "linux": [
            "📥 Step 1: Install Docker",
            "sudo apt update",
            "sudo apt install docker.io -y",
            "",
            "🚀 Step 2: Start & Enable",
            "sudo systemctl start docker",
            "sudo systemctl enable docker",
            "sudo usermod -aG docker $USER",
            "",
            "✅ Step 3: Verify (logout/login first)",
            "docker --version",
            "docker run hello-world",
            "",
            "⚡ Useful Commands:",
            "docker pull <image>",
            "docker run -d -p 8080:80 nginx",
            "docker ps",
            "docker-compose up -d"
        ],
        "docs": "https://docs.docker.com/"
    },
    "git": {
        "name": "Git",
        "description": "Version Control",
        "windows": [
            "📥 Step 1: Download Git",
            "https://git-scm.com/download/win",
            "Download and run installer",
            "Use default options",
            "",
            "⚙️ Step 2: Configure",
            "git config --global user.name \"Your Name\"",
            "git config --global user.email \"your@email.com\"",
            "",
            "✅ Step 3: Verify",
            "git --version",
            "",
            "⚡ Useful Commands:",
            "git init",
            "git clone <url>",
            "git add .",
            "git commit -m \"message\"",
            "git push origin main",
            "git pull origin main",
            "git branch",
            "git checkout -b new-branch"
        ],
        "linux": [
            "📥 Step 1: Install Git",
            "sudo apt update",
            "sudo apt install git -y",
            "",
            "⚙️ Step 2: Configure",
            "git config --global user.name \"Your Name\"",
            "git config --global user.email \"your@email.com\"",
            "",
            "✅ Step 3: Verify",
            "git --version",
            "",
            "⚡ Useful Commands:",
            "git init",
            "git clone <url>",
            "git add .",
            "git commit -m \"message\"",
            "git push origin main",
            "git pull origin main"
        ],
        "docs": "https://git-scm.com/doc"
    },
    "vscode": {
        "name": "VS Code",
        "description": "Code Editor",
        "windows": [
            "📥 Step 1: Download VS Code",
            "https://code.visualstudio.com/",
            "Click Download button",
            "Run installer",
            "",
            "⚡ Useful Extensions:",
            "Prettier - Code formatter",
            "ESLint - JavaScript linter",
            "Python - Python support",
            "Live Server - Local server",
            "GitLens - Git integration"
        ],
        "linux": [
            "📥 Step 1: Install VS Code",
            "sudo snap install code --classic",
            "",
            "Or download .deb from:",
            "https://code.visualstudio.com/",
            "sudo dpkg -i code_*.deb",
            "",
            "⚡ Useful Extensions:",
            "Prettier - Code formatter",
            "ESLint - JavaScript linter",
            "Python - Python support"
        ],
        "docs": "https://code.visualstudio.com/docs"
    },
    "tailwind": {
        "name": "Tailwind CSS",
        "description": "CSS Framework",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "",
            "📦 Step 2: Install Tailwind",
            "npm install -D tailwindcss postcss autoprefixer",
            "npx tailwindcss init -p",
            "",
            "⚙️ Step 3: Configure tailwind.config.js",
            "Add your template paths to content array",
            "",
            "📝 Step 4: Add to CSS file",
            "@tailwind base;",
            "@tailwind components;",
            "@tailwind utilities;",
            "",
            "🚀 Step 5: Build",
            "npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt install nodejs npm -y",
            "",
            "📦 Step 2: Install Tailwind",
            "npm install -D tailwindcss postcss autoprefixer",
            "npx tailwindcss init -p",
            "",
            "⚙️ Step 3: Configure tailwind.config.js",
            "Add your template paths to content array",
            "",
            "📝 Step 4: Add to CSS file",
            "@tailwind base;",
            "@tailwind components;",
            "@tailwind utilities;",
            "",
            "🚀 Step 5: Build",
            "npx tailwindcss -i ./src/input.css -o ./dist/output.css --watch"
        ],
        "docs": "https://tailwindcss.com/"
    },
    "typescript": {
        "name": "TypeScript",
        "description": "Typed JavaScript",
        "windows": [
            "📥 Step 1: Install Node.js First",
            "https://nodejs.org/",
            "",
            "📦 Step 2: Install TypeScript",
            "npm install -g typescript",
            "",
            "✅ Step 3: Verify",
            "tsc --version",
            "",
            "🚀 Step 4: Compile",
            "tsc file.ts",
            "tsc --init  (create tsconfig.json)",
            "tsc --watch"
        ],
        "linux": [
            "📥 Step 1: Install Node.js",
            "sudo apt install nodejs npm -y",
            "",
            "📦 Step 2: Install TypeScript",
            "sudo npm install -g typescript",
            "",
            "✅ Step 3: Verify",
            "tsc --version",
            "",
            "🚀 Step 4: Compile",
            "tsc file.ts",
            "tsc --init",
            "tsc --watch"
        ],
        "docs": "https://www.typescriptlang.org/"
    },
    "java": {
        "name": "Java",
        "description": "Programming Language",
        "windows": [
            "📥 Step 1: Download Java JDK",
            "https://adoptium.net/",
            "Download Temurin JDK",
            "Run installer",
            "",
            "✅ Step 2: Verify",
            "java --version",
            "javac --version",
            "",
            "🚀 Step 3: Compile & Run",
            "javac MyApp.java",
            "java MyApp"
        ],
        "linux": [
            "📥 Step 1: Install Java",
            "sudo apt update",
            "sudo apt install openjdk-21-jdk -y",
            "",
            "✅ Step 2: Verify",
            "java --version",
            "javac --version",
            "",
            "🚀 Step 3: Compile & Run",
            "javac MyApp.java",
            "java MyApp"
        ],
        "docs": "https://dev.java/"
    },
    "golang": {
        "name": "Go",
        "description": "Programming Language",
        "windows": [
            "📥 Step 1: Download Go",
            "https://go.dev/dl/",
            "Download MSI installer",
            "Run installer",
            "",
            "✅ Step 2: Verify",
            "go version",
            "",
            "🚀 Step 3: Create & Run",
            "mkdir myapp",
            "cd myapp",
            "go mod init myapp",
            "go run main.go",
            "",
            "⚡ Useful Commands:",
            "go build",
            "go test",
            "go get <package>"
        ],
        "linux": [
            "📥 Step 1: Install Go",
            "sudo apt update",
            "sudo apt install golang -y",
            "",
            "✅ Step 2: Verify",
            "go version",
            "",
            "🚀 Step 3: Create & Run",
            "mkdir myapp",
            "cd myapp",
            "go mod init myapp",
            "go run main.go",
            "",
            "⚡ Useful Commands:",
            "go build",
            "go test"
        ],
        "docs": "https://go.dev/"
    },
    "rust": {
        "name": "Rust",
        "description": "Systems Language",
        "windows": [
            "📥 Step 1: Download Rustup",
            "https://rustup.rs/",
            "Download and run rustup-init.exe",
            "",
            "✅ Step 2: Verify",
            "rustc --version",
            "cargo --version",
            "",
            "🚀 Step 3: Create & Run",
            "cargo new myapp",
            "cd myapp",
            "cargo run",
            "",
            "⚡ Useful Commands:",
            "cargo build",
            "cargo build --release",
            "cargo test"
        ],
        "linux": [
            "📥 Step 1: Install Rust",
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            "source $HOME/.cargo/env",
            "",
            "✅ Step 2: Verify",
            "rustc --version",
            "cargo --version",
            "",
            "🚀 Step 3: Create & Run",
            "cargo new myapp",
            "cd myapp",
            "cargo run",
            "",
            "⚡ Useful Commands:",
            "cargo build",
            "cargo test"
        ],
        "docs": "https://www.rust-lang.org/"
    }
}


# Aliases
ALIASES = {
    "node": "nodejs", "js": "nodejs", "npm": "nodejs",
    "py": "python", "pip": "python",
    "dj": "django", "ng": "angular",
    "mongo": "mongodb", "pg": "postgresql", "postgres": "postgresql",
    "ts": "typescript", "go": "golang",
    "tw": "tailwind", "tailwindcss": "tailwind",
    "code": "vscode", "vs": "vscode"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """👋 *Dev Install Bot*

I show you *complete step-by-step* guides with:
✅ Download links (no winget/choco needed!)
✅ Installation steps
✅ How to create project
✅ How to run
✅ Useful commands

*Available:*
`laravel` `django` `flask` `fastapi`
`react` `vue` `angular` `nextjs` `express`
`nodejs` `python` `php` `java` `golang` `rust`
`mongodb` `mysql` `postgresql`
`docker` `git` `flutter` `tailwind` `typescript`

Just type the name! 🚀
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip().lower()
    user_id = update.effective_user.id
    
    if len(query) < 2:
        return
    
    # Check aliases
    if query in ALIASES:
        query = ALIASES[query]
    
    # Check if framework exists
    if query in FRAMEWORK_GUIDES:
        user_cache[user_id] = query
        
        fw = FRAMEWORK_GUIDES[query]
        msg = f"🛠️ *{fw['name']}*\n_{fw['description']}_\n\n"
        msg += f"📚 {fw['docs']}\n\n"
        msg += "Select your OS 👇"
        
        keyboard = [
            [
                InlineKeyboardButton("🪟 Windows", callback_data=f"win_{user_id}"),
                InlineKeyboardButton("🐧 Linux/Mac", callback_data=f"linux_{user_id}")
            ]
        ]
        
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        # Show available options
        available = ", ".join([f"`{k}`" for k in list(FRAMEWORK_GUIDES.keys())[:15]])
        await update.message.reply_text(
            f"❌ `{query}` not found.\n\n*Try:*\n{available}...",
            parse_mode='Markdown'
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    parts = data.split("_")
    os_type = parts[0]
    user_id = int(parts[1])
    
    if user_id not in user_cache:
        await query.message.reply_text("Please search again.")
        return
    
    fw_name = user_cache[user_id]
    fw = FRAMEWORK_GUIDES[fw_name]
    
    os_key = "windows" if os_type == "win" else "linux"
    commands = fw.get(os_key, [])
    
    os_label = "Windows" if os_type == "win" else "Linux/Mac"
    msg = f"📋 *{fw['name']} - {os_label}*\n\n"
    
    for line in commands:
        if line == "":
            msg += "\n"
        elif line.startswith("📥") or line.startswith("⚙️") or line.startswith("✅") or line.startswith("🚀") or line.startswith("⚡") or line.startswith("📦") or line.startswith("📁") or line.startswith("📝") or line.startswith("⚠️"):
            msg += f"*{line}*\n"
        elif line.startswith("http"):
            msg += f"{line}\n"
        else:
            msg += f"`{line}`\n"
    
    msg += f"\n📚 {fw['docs']}\n"
    msg += "\n👆 Tap commands to copy!"
    
    await query.message.reply_text(msg, parse_mode='Markdown', disable_web_page_preview=True)

def main():
    print("🤖 Bot starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("✅ Bot running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
