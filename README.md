<div align="center">

# ⚔️ Seven Knights Rebirth Calculator

  <img src="https://img.shields.io/badge/Version-2.1.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Type_Hints-100%25-blueviolet?style=for-the-badge" alt="Type Hints">
  <img src="https://img.shields.io/badge/AI_Powered-90%25-purple?style=for-the-badge&logo=openai&logoColor=white" alt="AI Powered">

  <h3>Advanced Damage Optimization Tool for End-Game Players</h3>
  
  <p>
    Reverse-engineered damage formulas • Castle Rush Simulator • Precision CLI
  </p>

</div>

---

## 📑 Table of Contents
- [🤖 AI Development Disclaimer](#-ai-development-disclaimer)
- [🚀 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🛠️ Installation](#-installation)
- [🎮 Usage Guide](#-usage-guide)
- [⚙️ Configuration](#-configuration)
- [📂 Project Structure](#-project-structure)
- [📜 License](#-license)

---

## 🤖 AI Development Disclaimer

> [!CAUTION]
> **DEVELOPED WITH 90% AI ASSISTANCE**
>
> Please be aware that this project was significantly constructed using Artificial Intelligence.
>
> *   **Author's Role**: Logic formulation, game mechanics research, and result verification (Quality Assurance).
> *   **AI's Role**: Code architecture, Python implementation, refactoring, and documentation generation.
> 
> *The author possesses zero manual coding capability in Python. This tool demonstrates the power of AI-Human collaboration.*

---

## 🚀 Overview

**7k Rebirth Damage Calculator** is a precision engineering tool for *Seven Knights Rebirth*. Unlike basic spreadsheets, this CLI application executes complex damage equations using `Decimal` floating-point precision to match in-game values exactly.

It is specifically designed for:
*   **Min-Maxers** looking to optimize every digit of damage.
*   **Guild Castle Rush** strategists planning clear requirements.
*   **Theorycrafters** testing rigorous "what-if" scenarios.

---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **🎯 High-Precision Math** | Uses `Decimal` types to prevent floating-point errors, ensuring 1:1 parity with game numbers. |
| **🏰 Castle Mode Simulator** | Exclusive **Sun Wukong** algorithms to calculate the *exact* minimum critical hits needed to clear stages. |
| **📊 Multi-Scenario Analysis** | Automatically simulates "Best Case" (Crit + Weakness) vs. "Worst Case" (Normal) scenarios side-by-side. |
| **⚡ Total ATK Calculator** | Instant calculation of effective Attack Power including Pet, Formation, and hidden multipliers. |
| **📝 Customizable Config** | Persistent `config.json` allows for rapid iteration of stats without code changes. |
| **🧩 Extensible Architecture** | Modular JSON-based character system makes adding new heroes effortless. |
| **🔒 Type-Safe Code** | 100% type-annotated codebase for better IDE support and error detection. |

---

## 🛠️ Installation

### Prerequisites
*   Python 3.10 or higher (for modern type hints support)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Piyabordee/7k-rebirth-calculator.git

# 2. Navigate to directory
cd 7k-rebirth-calculator

# 3. (Optional) Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

---

## 🎮 Usage Guide

Launch the calculator via command line:

```bash
cd calculator
python main.py
```

### 🖥️ Menu System

```text
--- Select Mode ---
  1. Standard Mode    (Uses local config.json)
  2. Castle Mode      (Loads Room 1/2 Monster Presets)
  3. ATK Compare      (Compare ATK between configs)
```

### 👑 Castle Mode Example
Select **Sun Wukong** in Castle Mode to see the breakdown:

```text
  🎲 Minimum Crits Needed Comparison
---------------------------------------------------------------------------
   Crit |      [Case 1] Base=Weakness      |       [Case 2] Base=Normal      
---------------------------------------------------------------------------
     0  | 14,685 ✅ 🔥 MIN                   | 11,295 ✅ 🔥 MIN
     1  | 24,770 ✅                         | 22,510 ✅
```

---


## 🏆 Character Showcases

See detailed output examples for all characters: **[📄 SHOWCASES.md](docs/SHOWCASES.md)**

---

## 👾 Supported Characters

| Character | _class | Special Mechanics |
|:----------|:-------|:------------------|
| Sun Wukong | Balance | Castle Mode (คริขั้นต่ำ) |
| Espada | Magic | HP-Based Damage |
| Freyja | Magic | HP Alteration |
| Ryan | Attack | Lost HP Bonus |
| Klahan | Attack | HP Condition Bonus |
| Teo | Attack | Bonus Crit DMG |
| Miho | Magic | Standard |
| Pascal | Magic | Standard |
| Rachel | Magic | DEF Reduce |
| Yeonhee | Magic | HP-Based |

---

## ⚙️ Configuration

Modify `calculator/config.json` to match your in-game stats. See [config.json](calculator/config.json) for full template.

---

<details>
<summary><b>📂 Project Structure</b> (click to expand)</summary>

```bash
calculator/
├── main.py              # Entry Point
├── menu.py              # CLI Interface
├── atk_compare_mode.py  # ATK Comparison Logic
├── damage_calc.py       # Core Math Engine
├── config.json          # User Settings
├── characters/          # Hero Database (JSON)
└── logic/               # Specialized Algorithms
```

</details>

---

## 👤 Credits

> **In-Game Name:** `snowb4ll`
> **Server:** `19`

### 🧠 Formula Credits
> Damage calculation formulas by **BelXenonZ** and **AcidAqua**

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

  **Star ⭐ this repo if it helped you hit a new damage record!**
  
  <small>Built with precision, powered by AI.</small>

</div>
