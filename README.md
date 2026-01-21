<div align="center">

# ⚔️ Seven Knights Rebirth Calculator

  <img src="https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
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

---

## 🛠️ Installation

### Prerequisites
*   Python 3.9 or higher

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
  3. Quick ATK Calc   (Calculates Total Attack only)
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


## 🏆 Character Capability Showcases

See how the calculator handles complex unique mechanics for top-tier characters.

### ⚔️ Ryan - Executioner Logic
*Calculates **Lost HP** bonus, dynamically scaling damage based on enemy remaining health.*

```text
============================================================
  ⚔️ Ryan - Gale Slash Calculator ⚔️
============================================================

  📊 HP เป้าหมายเหลือ: 30.00%
  ⚡ Lost HP Bonus: สูงสุด +50.00%
  🔥 Weakness Extra Damage: +270.00%

------------------------------------------------------------
  [4] ดาเมจติดจุดอ่อน (HP เหลือ 30.00%) 🔥 MAX
------------------------------------------------------------
  Final: 1,254,880
         (+270.00% Weakness Extra, +35.0% Lost HP)
         (5 hits x 250,976/hit)

============================================================
  💀 ดาเมจสูงสุด: 1,254,880
============================================================
```

### 🌟 Freyja - HP Alteration
*Simulates "Divinity" checks to compare absolute HP reduction vs raw damage potential.*

```text
==================================================
  🌟 Freyja - HP Alteration Calculator 🌟
==================================================

  📊 HP Target: 100,000,000
  ⚡ HP Alteration: 39.0% (มอนเหลือ 39.0%)

--------------------------------------------------
  ดาเมจ HP Alteration (ถ้ามี 4 Divinity stacks)
--------------------------------------------------
  HP Alteration:   61,000,000
                   (มอนเหลือ 39.0% จาก 100,000,000 HP)

--------------------------------------------------
  ดาเมจรวม (สกิล + HP Alteration)
--------------------------------------------------
  จุดอ่อน + HP Alt:    63,450,200
```

### 🐯 Klahan - Conditional Bonus
*Automatically applies "+135% Bonus Damage" conditions based on enemy HP threshold.*

```text
============================================================
  🐯 Klahan - Gale Blast Calculator 🐯
============================================================

  📊 Base SKILL_DMG: 160.00%
  ⚡ HP Bonus: +135.00% (เมื่อ HP >= 50%)
  🔥 Total SKILL_DMG: 295.00%

------------------------------------------------------------
  [4] ดาเมจติดจุดอ่อน (HP >= 50%) 🔥 MAX
------------------------------------------------------------
  Final: 845,600 (SKILL_DMG: 295.00%)
         (2 hits x 422,800/hit)
```

### 🔥 Espada - Hybrid Scaling
*Compares Raw Damage vs HP-Based Damage to find the highest output.*

```text
============================================================
  Espada Special Calculation (4 กรณี)
============================================================

[2] คริ + HP-based (HP: 2,752,900):
    RAW_DMG = 3,785,236.80
    Final = 4,497,975

[4] จุดอ่อน (+35%) + HP-based:
    RAW_DMG = 4,428,727.05
    Final = 5,262,630

============================================================
>>> ดาเมจสูงสุด (จุดอ่อน+HP): 5,262,630 <<<
============================================================
```

---

## ⚙️ Configuration

Modify `calculator/config.json` to match your in-game stats.

```json
{
  "Weapon_Set": 3,            // 0=None, 1=Weak, 2=Crit, 3=Hydra
  "Formation": 62.00,         // Formation Bonus (%)
  "ATK_CHAR": 4134.00,        // Character Base Attack
  "CRIT_DMG": 306.00,         // Critical Damage (%)
  "DMG_AMP_BUFF": 0.00,       // Ring/Accessory Bonus
  "ATK_PET": 564.00,          // Pet Attack
  "BUFF_ATK_PET": 21.00       // Pet Buff (%)
}
```

---

## 📂 Project Structure

```bash
calculator/
├── main.py              # Application Entry Point
├── menu.py              # CLI Interface Logic
├── damage_calc.py       # Core Math Engine
├── constants.py         # Static Game Data (Rarity/Class Stats)
├── config.json          # User Settings
├── characters/          # Hero Database (JSON)
│   ├── sun_wukong.json
│   ├── freyja.json
│   └── ...
└── logic/               # Specialized Hero Algorithms
    ├── sun_wukong.py    # Castle Rush Logic
    ├── freyja.py        # HP Alteration Logic
    └── ryan.py          # Lost HP Bonus Logic
```

---

## 👤 Credits

> **In-Game Name:** `snowb4ll`
> **Server:** `19`

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<div align="center">

  **Star ⭐ this repo if it helped you hit a new damage record!**
  
  <small>Built with precision, powered by AI.</small>

</div>
