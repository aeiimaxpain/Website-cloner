# Ethical Website Cloner (Termux Ready)

An **ethical, permission-based website cloning tool** written in Python.  
Built for **offline analysis, UI testing, security labs, and authorized audits**.

> ⚠️ Use **only** on websites you own or have explicit permission to test.

---

## Features

- Clones **public pages only**
- Creates a folder named after the target domain
- Crawls all **internal links**
- Downloads:
  - HTML
  - CSS
  - JavaScript
  - Images
  - Fonts
- Rewrites links for **offline viewing**
- Respects `robots.txt`
- Rate-limited crawling
- Fully compatible with **Termux (Android)**

---

## Requirements

### System (Termux)
```bash
pkg update && pkg upgrade
pkg install python git clang libxml2 libxslt -y


git clone https://github.com/aeiimaxpain/Website-cloner.git
cd ethical-website-cloner
pip install -r requirements.txt

```

### Example 
```bash
example.com/
├── index.html
├── css/
├── js/
└── images/

```

