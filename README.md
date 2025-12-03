# ReticulumTools
Reticulum Dedicated Python Scripts &amp; Tools to help installing and configure RNS suite packages

# 🌐 Reticulum Network Interactive Installation & Config Tools

Interactive tools for installing and configuring the [Reticulum Network Stack](https://reticulum.network/) ecosystem. Designed for beginners with multi-language support.

![Python 3.7+](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)

## 🎯 Features

- **Multi-language support**: English, Italiano, Español, Deutsch, Русский
- **Beginner-friendly**: Interactive menus with clear descriptions
- **Safe editing**: Automatic backups before any config changes
- **No dependencies**: Pure Python 3.7+ — just download and run
- **Smart installation**: Handles `--break-system-packages` and `--user` flags automatically

## 📦 Included Tools

| Tool | Description |
|------|-------------|
| `reticulum_installer.py` | Install RNS, LXMF, NomadNet, Sideband, and more |
| `reticulum_configurator.py` | Configure `~/.reticulum/config` interactively |
| `nomadnet_configurator.py` | Configure `~/.nomadnetwork/config` interactively |

## ⚡ Quick Start

```bash
# Download the tools
git clone https://github.com/YOUR_USERNAME/reticulum-tools.git
cd reticulum-tools

# Make executable
chmod +x *.py

# Run the installer
./reticulum_installer.py
```

## 📋 Prerequisites

- **Python 3.7** or higher
- **pip** (usually included with Python)
- **Internet connection** for package installation

Check your Python version:
```bash
python3 --version
```

## 🚀 Usage

### 1. Installer — Install Reticulum Packages

```bash
python3 reticulum_installer.py
```

**Available packages:**
- 📡 **RNS** — Core Reticulum Network Stack (required)
- 💬 **LXMF** — Lightweight Extensible Message Format
- 🖥️ **NomadNet** — Terminal-based communicator
- 📱 **Sideband** — GUI messaging app
- 🔧 **RNodeConf** — RNode hardware configuration
- 📻 **LXMF Tools** — Additional utilities

### 2. Reticulum Configurator — Setup Network Interfaces

```bash
python3 reticulum_configurator.py
```

**Features:**
- Edit general settings (log level, transport mode)
- Manage network interfaces
- **Quick Connect** — Add public nodes instantly:
  - `rmap.world:4242` — Reticulum Network Map
  - `dublin.connect.reticulum.network:4965` — Official Testnet
  - `reticulum.betweentheborders.com:4242` — Community Hub
  - And more...

### 3. NomadNet Configurator — Setup Your Node

```bash
python3 nomadnet_configurator.py
```

**Features:**
- Set display name and client options
- Configure text UI (colors, editor, intro)
- **Enable node hosting** to serve pages
- Auto-creates page folders with example homepage

## 📁 Page Hosting (NomadNet)

To host pages on your NomadNet node:

1. Enable node hosting in the configurator (option 4)
2. Place your `.mu` pages in:
   ```
   ~/.nomadnetwork/storage/pages/
   ```
3. Place files to share in:
   ```
   ~/.nomadnetwork/storage/files/
   ```
4. Restart NomadNet

**Example page (`index.mu`):**
```
`!Welcome to My Node

>This is my NomadNet node!

`[About`:/page/about.mu]
`[Files`:/file/]
```

## 🔧 Troubleshooting

**Permission denied during install:**
The installer automatically tries `--user` or `--break-system-packages` flags.

**Config file not found:**
Run the respective application once to generate defaults:
```bash
rnsd      # Creates ~/.reticulum/config
nomadnet  # Creates ~/.nomadnetwork/config
```

**Python not found:**
Try `python` instead of `python3`, or install Python from your package manager.

## 🌍 Public Nodes

Connect to these community nodes to join the Reticulum network:

| Node | Host | Port |
|------|------|------|
| RMAP.world | `rmap.world` | 4242 |
| Dublin Testnet | `dublin.connect.reticulum.network` | 4965 |
| BetweenTheBorders | `reticulum.betweentheborders.com` | 4242 |
| Sydney RNS | `sydney.reticulum.au` | 4242 |

More nodes: [reticulum.network/connect](https://reticulum.network/connect.html)

## 📚 Resources

- [Reticulum Network](https://reticulum.network/) — Official documentation
- [NomadNet](https://github.com/markqvist/NomadNet) — Terminal communicator
- [Sideband](https://github.com/markqvist/Sideband) — GUI messaging app
- [LXMF](https://github.com/markqvist/LXMF) — Message protocol
- [RMAP](https://rmap.world) — Reticulum Network Map

## 📄 License

MIT License — Feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

---

**Made with ❤️ for the Reticulum community**
