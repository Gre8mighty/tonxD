<p align="center">
  <img src="./assets/banner.png" alt="FlexxRichie Banner" width="100%" />
</p>

# TONxDAO - Auto Claim Bot 🚀

A powerful automation tool for TONxDAO tasks and farming, designed for efficiency and ease of use. This bot helps automate your daily tasks and maximize your earnings through intelligent task management and farming strategies.

## 📱 Social Links & Support

Join our growing community:

- 🔔 **Main Channel**: [FlexxRichie Airdrops](https://t.me/airdrop3arn)
- 💬 **Twitter Page**: [FlexxRichie](https://twitter.com/flexxrichie)

## ✨ Features

Our bot comes equipped with powerful features designed to maximize your efficiency:

| Feature       | Description                           | Configuration          |
|--------------|---------------------------------------|----------------------|
| Auto Check-in | Daily login rewards and point collection | `auto-check-in: true` |
| Auto Tasks   | Automated task completion for maximum earnings | `auto-do-task: true`  |
| Auto Farm    | Smart energy-based farming system     | `auto-farm: true`     |

## 🛠️ Installation

### Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Python 3.8 or higher**:
   - Windows: Download and install from [python.org](https://www.python.org/downloads/)
   - Linux: `sudo apt-get install python3 python3-pip`
   - macOS: `brew install python`
   - Termux: `pkg install python`

2. **Git**:
   - Windows: Download and install from [git-scm.com](https://git-scm.com/downloads)
   - Linux: `sudo apt-get install git`
   - macOS: `brew install git`
   - Termux: `pkg install git`

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fl3xxrichie/tonxD.git
   cd tonxD
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Termux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   # Upgrade pip first
   python -m pip install --upgrade pip

   # Install requirements
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   # Check if required packages are installed
   pip list | grep "smart-airdrop-claimer"
   pip list | grep "websocket-client"
   ```

### Termux-Specific Setup

If you're using Termux, follow these additional steps:

1. **Update Termux packages**:
   ```bash
   pkg update && pkg upgrade -y
   ```

2. **Install required packages**:
   ```bash
   pkg install python python-pip git libjpeg-turbo
   ```

3. **Install development tools**:
   ```bash
   pkg install build-essential
   ```

4. **Set storage permissions** (if needed):
   ```bash
   termux-setup-storage
   ```

### Troubleshooting Common Installation Issues

If you encounter any errors during installation:

1. **SSL Certificate errors**:
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

2. **Permission errors on Linux/macOS**:
   ```bash
   sudo pip install -r requirements.txt
   ```

3. **Permission errors on Termux**:
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Missing build tools**:
   - Windows: Install Visual C++ Build Tools
   - Linux: `sudo apt-get install python3-dev build-essential`
   - macOS: `xcode-select --install`
   - Termux: `pkg install clang python-dev`

## 🚀 Usage Guide

Setting up and running the bot is straightforward:

1. **Get Your Auth Data**:
   - Open Telegram Web (https://web.telegram.org)
   - Open Developer Tools (F12)
   - Go to Application tab
   - Find your `query_id` and user data
   - Add to `data.txt`

2. **Configure Settings**:
   ```json
   {
     "auto-check-in": "true",
     "auto-do-task": "true",
     "auto-farm": "true"
   }
   ```

3. **Run the Bot**:
   ```bash
   # Make sure your virtual environment is activated
   python bot.py
   ```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

---

<p align="center">
  Created with ❤️ by <a href="https://t.me/airdrop3arn">FlexxRichie</a>
</p>