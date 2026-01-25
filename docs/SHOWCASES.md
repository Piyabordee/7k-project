# 🏆 Character Showcases

Detailed output examples from the 7k Rebirth Damage Calculator.

---

## 👑 Sun Wukong - Castle Mode

*Calculates minimum critical hits needed to clear stages.*

```text
  🎲 Minimum Crits Needed Comparison
---------------------------------------------------------------------------
   Crit |      [Case 1] Base=Weakness      |       [Case 2] Base=Normal      
---------------------------------------------------------------------------
     0  | 14,685 ✅ 🔥 MIN                   | 11,295 ✅ 🔥 MIN
     1  | 24,770 ✅                         | 22,510 ✅
     2  | 35,855 ✅                         | 33,725 ✅
     3  | 46,940 ✅                         | 44,940 ✅
```

---

## 🔥 Espada - HP-Based Damage

*Compares Raw Damage vs HP-Based Damage to find the highest output.*

```text
============================================================
  Espada Special Calculation (4 กรณี)
============================================================

[1] คริ (ไม่มี HP-based):     Final = 37,763
[2] คริ + HP-based:           Final = 42,920
[3] จุดอ่อน (ไม่มี HP-based): Final = 49,092
[4] จุดอ่อน + HP-based:       Final = 55,796 🔥 MAX

============================================================
```

---

## 🌟 Freyja - HP Alteration

*HP Alteration ลด HP มอนโดยตรง (ไม่มี DEF)*

```text
==================================================
  🌟 Freyja - HP Alteration Calculator 🌟
==================================================

  📊 HP Target: 100,000,000
  ⚡ HP Alteration: 39.0% (มอนเหลือ 39.0%)

  HP Alteration Damage: 61,000,000
  จุดอ่อน + HP Alt:     63,450,200 🔥 MAX
```

---

## ⚔️ Ryan - Lost HP Bonus

*ดาเมจเพิ่มตาม HP ที่ศัตรูเสียไป*

```text
============================================================
  ⚔️ Ryan - Gale Slash Calculator ⚔️
============================================================

  📊 HP เป้าหมายเหลือ: 30.00%
  ⚡ Lost HP Bonus: +35.0% (จากสูงสุด 50%)
  🔥 Weakness Extra: +270.00%

  Final: 1,254,880 (5 hits x 250,976/hit) 🔥 MAX
============================================================
```

---

## 🐯 Klahan - HP Condition Bonus

*SKILL_DMG เพิ่มตามเงื่อนไข HP*

```text
============================================================
  🐯 Klahan - Gale Blast Calculator 🐯
============================================================

  📊 Base SKILL_DMG: 160.00%
  ⚡ HP >= 50% Bonus: +135.00%
  🔥 Total SKILL_DMG: 295.00%

  Final: 845,600 (2 hits x 422,800/hit) 🔥 MAX
============================================================
```

---

## 📋 Standard Characters

ตัวละครที่ใช้สูตรคำนวณมาตรฐาน (ต่างกันที่ passive/skill values):

| Character | Class | Special Stat | ติดคริ | ติดคริ+จุดอ่อน |
|:----------|:------|:-------------|-------:|---------------:|
| **Teo** | Attack | CRIT_DMG +85% | 9,396 | 12,216 |
| **Miho** | Magic | WEAK_DMG +23% | 10,373 | 15,871 |
| **Pascal** | Magic | Ignore DEF 65% | 75,093 | 97,621 |
| **Rachel** | Balance | DEF Reduce 29% | 14,881 | 19,345 |
| **Yeonhee** | Magic | Ignore DEF 40% | 16,017 | 20,823 |

> 💡 **หมายเหตุ:** ค่าดาเมจขึ้นอยู่กับ config.json ที่ตั้งไว้

---

[← Back to README](../README.md)
