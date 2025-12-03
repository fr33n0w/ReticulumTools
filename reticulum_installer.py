#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           RETICULUM NETWORK SUITE - INTERACTIVE INSTALLER                    ║
║                                                                              ║
║  A beginner-friendly installer for the Reticulum Network Stack ecosystem    ║
║  Supports: RNS, LXMF, NomadNet, Sideband, rnodeconfigtool, and more         ║
║                                                                              ║
║  Languages: English, Italiano, Español, Deutsch, Русский                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import os
import platform
import shutil
import time
import json
from pathlib import Path

# ══════════════════════════════════════════════════════════════════════════════
# LANGUAGE TRANSLATIONS
# ══════════════════════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "en": {
        "lang_name": "English",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RETICULUM NETWORK SUITE INSTALLER                         ║
║                                                                              ║
║  Welcome! This installer will help you set up Reticulum Network Stack       ║
║  software on your system. Everything is automated and beginner-friendly.    ║
║                                                                              ║
║  What is Reticulum?                                                          ║
║  Reticulum is a cryptography-based networking stack for building resilient  ║
║  networks that can operate over any medium - LoRa, WiFi, Internet, and more ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "select_language": "🌐 Please select your language / Seleccione su idioma:",
        "checking_system": "🔍 Checking your system...",
        "system_info": "📋 System Information:",
        "os_label": "   Operating System:",
        "python_version": "   Python Version:",
        "pip_version": "   Pip Version:",
        "checking_deps": "🔧 Checking dependencies...",
        "installing_deps": "📦 Installing required dependencies...",
        "deps_ok": "✅ All dependencies are satisfied!",
        "select_packages": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SELECT PACKAGES TO INSTALL                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Available packages:

  [1] 📡 RNS (Reticulum Network Stack)
      The core networking library - REQUIRED for all other packages
      
  [2] 💬 LXMF (Lightweight Extensible Message Format)
      Message protocol built on Reticulum for async messaging
      
  [3] 🖥️  NomadNet
      Terminal-based communication platform with pages and messaging
      
  [4] 📱 Sideband
      Mobile/desktop app for LXMF messaging (GUI application)
      
  [5] 🔧 RNode Configuration Tool
      Tool for configuring RNode LoRa hardware devices
      
  [6] 📻 LXMF Tools (lxmfd, lxmessaging, etc.)
      Additional LXMF utilities and daemons

  [A] 🎁 Install ALL packages (recommended for beginners)
  
  [Q] ❌ Quit installer
""",
        "enter_choice": "Enter your choice (1-6, A for all, Q to quit): ",
        "invalid_choice": "❌ Invalid choice. Please try again.",
        "installing": "📦 Installing",
        "install_success": "✅ Successfully installed",
        "install_failed": "❌ Failed to install",
        "error_details": "   Error details:",
        "retry_prompt": "Would you like to retry? (y/n): ",
        "fix_attempting": "🔧 Attempting to fix the issue...",
        "installation_complete": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        INSTALLATION COMPLETE! 🎉                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "installed_packages": "📦 Installed packages:",
        "getting_started": """
🚀 GETTING STARTED:

  • To start Reticulum:     rnsd
  • To run NomadNet:        nomadnet
  • To configure RNode:     rnodeconf
  • Configuration folder:   ~/.reticulum/
  
  📚 Documentation: https://reticulum.network/
  💬 Community: https://github.com/markqvist/Reticulum
""",
        "press_enter": "Press Enter to continue...",
        "goodbye": "👋 Thank you for using the Reticulum Installer! Goodbye!",
        "confirm_install": "Install selected packages? (y/n): ",
        "yes": "y",
        "no": "n",
        "upgrading_pip": "📦 Upgrading pip to latest version...",
        "pip_upgraded": "✅ Pip upgraded successfully!",
        "checking_python": "🐍 Checking Python installation...",
        "python_ok": "✅ Python is properly installed!",
        "installing_pip": "📦 Installing pip...",
        "root_warning": """
⚠️  WARNING: Running as root/administrator
    
    It's recommended to run this installer as a normal user.
    Continue anyway? (y/n): """,
        "venv_info": """
💡 TIP: For a cleaner installation, consider using a virtual environment:
   python3 -m venv ~/reticulum-env
   source ~/reticulum-env/bin/activate
   Then run this installer again.
   
   Continue with system-wide installation? (y/n): """,
        "package_descriptions": {
            "rns": "Core Reticulum Network Stack library",
            "lxmf": "Lightweight Extensible Message Format",
            "nomadnet": "Terminal-based Reticulum communicator",
            "sideband": "GUI messaging application",
            "rnodeconf": "RNode hardware configuration tool",
            "lxmf-tools": "LXMF utilities and daemons"
        },
        "already_installed": "ℹ️  Already installed:",
        "will_upgrade": "(will be upgraded)",
        "network_error": "❌ Network error. Please check your internet connection.",
        "permission_error": "❌ Permission denied. Try running with sudo or use --user flag.",
        "unknown_error": "❌ An unknown error occurred.",
        "attempting_user_install": "🔧 Attempting user-level installation...",
        "attempting_break_packages": "🔧 Attempting installation with --break-system-packages...",
        "main_menu": "📋 Main Menu",
        "back_to_menu": "Press Enter to return to main menu...",
        "checking_installed": "🔍 Checking installed packages...",
        "upgrade_available": "⬆️  Upgrade available:",
        "current_version": "   Current:",
        "latest_version": "   Latest:",
        "no_packages_selected": "❌ No packages selected.",
        "select_at_least_one": "Please select at least one package.",
        "dependency_note": "📝 Note: RNS will be installed automatically as it's required by other packages.",
        "install_order": "📋 Installation order (dependencies first):",
        "step": "Step",
        "of": "of",
        "skipping": "⏭️  Skipping (already up to date):",
        "total_time": "⏱️  Total installation time:",
        "seconds": "seconds",
        "minutes": "minutes",
    },
    
    "it": {
        "lang_name": "Italiano",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INSTALLATORE RETICULUM NETWORK SUITE                      ║
║                                                                              ║
║  Benvenuto! Questo installatore ti aiuterà a configurare il software        ║
║  Reticulum Network Stack sul tuo sistema. Tutto è automatizzato.            ║
║                                                                              ║
║  Cos'è Reticulum?                                                            ║
║  Reticulum è uno stack di rete basato su crittografia per costruire reti    ║
║  resilienti che possono operare su qualsiasi mezzo - LoRa, WiFi, Internet   ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "select_language": "🌐 Please select your language / Seleziona la tua lingua:",
        "checking_system": "🔍 Controllo del sistema...",
        "system_info": "📋 Informazioni di Sistema:",
        "os_label": "   Sistema Operativo:",
        "python_version": "   Versione Python:",
        "pip_version": "   Versione Pip:",
        "checking_deps": "🔧 Controllo dipendenze...",
        "installing_deps": "📦 Installazione dipendenze richieste...",
        "deps_ok": "✅ Tutte le dipendenze sono soddisfatte!",
        "select_packages": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SELEZIONA I PACCHETTI DA INSTALLARE                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Pacchetti disponibili:

  [1] 📡 RNS (Reticulum Network Stack)
      La libreria di rete principale - RICHIESTA per tutti gli altri pacchetti
      
  [2] 💬 LXMF (Lightweight Extensible Message Format)
      Protocollo messaggi costruito su Reticulum per messaggistica asincrona
      
  [3] 🖥️  NomadNet
      Piattaforma di comunicazione terminal-based con pagine e messaggistica
      
  [4] 📱 Sideband
      App mobile/desktop per messaggistica LXMF (applicazione GUI)
      
  [5] 🔧 RNode Configuration Tool
      Strumento per configurare dispositivi hardware RNode LoRa
      
  [6] 📻 LXMF Tools (lxmfd, lxmessaging, ecc.)
      Utilità e daemon LXMF aggiuntivi

  [A] 🎁 Installa TUTTI i pacchetti (raccomandato per principianti)
  
  [Q] ❌ Esci dall'installatore
""",
        "enter_choice": "Inserisci la tua scelta (1-6, A per tutti, Q per uscire): ",
        "invalid_choice": "❌ Scelta non valida. Riprova.",
        "installing": "📦 Installazione di",
        "install_success": "✅ Installato con successo",
        "install_failed": "❌ Installazione fallita per",
        "error_details": "   Dettagli errore:",
        "retry_prompt": "Vuoi riprovare? (s/n): ",
        "fix_attempting": "🔧 Tentativo di correzione del problema...",
        "installation_complete": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                       INSTALLAZIONE COMPLETATA! 🎉                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "installed_packages": "📦 Pacchetti installati:",
        "getting_started": """
🚀 COME INIZIARE:

  • Per avviare Reticulum:  rnsd
  • Per eseguire NomadNet:  nomadnet
  • Per configurare RNode:  rnodeconf
  • Cartella configurazione: ~/.reticulum/
  
  📚 Documentazione: https://reticulum.network/
  💬 Community: https://github.com/markqvist/Reticulum
""",
        "press_enter": "Premi Invio per continuare...",
        "goodbye": "👋 Grazie per aver usato l'Installatore Reticulum! Arrivederci!",
        "confirm_install": "Installare i pacchetti selezionati? (s/n): ",
        "yes": "s",
        "no": "n",
        "upgrading_pip": "📦 Aggiornamento pip all'ultima versione...",
        "pip_upgraded": "✅ Pip aggiornato con successo!",
        "checking_python": "🐍 Controllo installazione Python...",
        "python_ok": "✅ Python è installato correttamente!",
        "installing_pip": "📦 Installazione pip...",
        "root_warning": """
⚠️  ATTENZIONE: Esecuzione come root/amministratore
    
    Si raccomanda di eseguire questo installatore come utente normale.
    Continuare comunque? (s/n): """,
        "venv_info": """
💡 SUGGERIMENTO: Per un'installazione più pulita, considera l'uso di un ambiente virtuale:
   python3 -m venv ~/reticulum-env
   source ~/reticulum-env/bin/activate
   Poi esegui di nuovo questo installatore.
   
   Continuare con l'installazione di sistema? (s/n): """,
        "package_descriptions": {
            "rns": "Libreria principale Reticulum Network Stack",
            "lxmf": "Lightweight Extensible Message Format",
            "nomadnet": "Comunicatore Reticulum basato su terminale",
            "sideband": "Applicazione messaggistica GUI",
            "rnodeconf": "Strumento configurazione hardware RNode",
            "lxmf-tools": "Utilità e daemon LXMF"
        },
        "already_installed": "ℹ️  Già installato:",
        "will_upgrade": "(verrà aggiornato)",
        "network_error": "❌ Errore di rete. Controlla la connessione internet.",
        "permission_error": "❌ Permesso negato. Prova con sudo o usa --user.",
        "unknown_error": "❌ Si è verificato un errore sconosciuto.",
        "attempting_user_install": "🔧 Tentativo di installazione a livello utente...",
        "attempting_break_packages": "🔧 Tentativo installazione con --break-system-packages...",
        "main_menu": "📋 Menu Principale",
        "back_to_menu": "Premi Invio per tornare al menu principale...",
        "checking_installed": "🔍 Controllo pacchetti installati...",
        "upgrade_available": "⬆️  Aggiornamento disponibile:",
        "current_version": "   Attuale:",
        "latest_version": "   Ultima:",
        "no_packages_selected": "❌ Nessun pacchetto selezionato.",
        "select_at_least_one": "Seleziona almeno un pacchetto.",
        "dependency_note": "📝 Nota: RNS verrà installato automaticamente perché richiesto dagli altri pacchetti.",
        "install_order": "📋 Ordine di installazione (dipendenze prima):",
        "step": "Passo",
        "of": "di",
        "skipping": "⏭️  Saltato (già aggiornato):",
        "total_time": "⏱️  Tempo totale di installazione:",
        "seconds": "secondi",
        "minutes": "minuti",
    },
    
    "es": {
        "lang_name": "Español",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    INSTALADOR RETICULUM NETWORK SUITE                        ║
║                                                                              ║
║  ¡Bienvenido! Este instalador te ayudará a configurar el software           ║
║  Reticulum Network Stack en tu sistema. Todo está automatizado.             ║
║                                                                              ║
║  ¿Qué es Reticulum?                                                          ║
║  Reticulum es una pila de red basada en criptografía para construir redes   ║
║  resilientes que pueden operar sobre cualquier medio - LoRa, WiFi, Internet ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "select_language": "🌐 Please select your language / Seleccione su idioma:",
        "checking_system": "🔍 Verificando tu sistema...",
        "system_info": "📋 Información del Sistema:",
        "os_label": "   Sistema Operativo:",
        "python_version": "   Versión de Python:",
        "pip_version": "   Versión de Pip:",
        "checking_deps": "🔧 Verificando dependencias...",
        "installing_deps": "📦 Instalando dependencias requeridas...",
        "deps_ok": "✅ ¡Todas las dependencias están satisfechas!",
        "select_packages": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SELECCIONA LOS PAQUETES A INSTALAR                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Paquetes disponibles:

  [1] 📡 RNS (Reticulum Network Stack)
      La biblioteca de red principal - REQUERIDA para todos los demás paquetes
      
  [2] 💬 LXMF (Lightweight Extensible Message Format)
      Protocolo de mensajes construido sobre Reticulum para mensajería asíncrona
      
  [3] 🖥️  NomadNet
      Plataforma de comunicación basada en terminal con páginas y mensajería
      
  [4] 📱 Sideband
      Aplicación móvil/escritorio para mensajería LXMF (aplicación GUI)
      
  [5] 🔧 RNode Configuration Tool
      Herramienta para configurar dispositivos hardware RNode LoRa
      
  [6] 📻 LXMF Tools (lxmfd, lxmessaging, etc.)
      Utilidades y daemons LXMF adicionales

  [A] 🎁 Instalar TODOS los paquetes (recomendado para principiantes)
  
  [Q] ❌ Salir del instalador
""",
        "enter_choice": "Ingresa tu elección (1-6, A para todos, Q para salir): ",
        "invalid_choice": "❌ Elección inválida. Intenta de nuevo.",
        "installing": "📦 Instalando",
        "install_success": "✅ Instalado exitosamente",
        "install_failed": "❌ Falló la instalación de",
        "error_details": "   Detalles del error:",
        "retry_prompt": "¿Deseas reintentar? (s/n): ",
        "fix_attempting": "🔧 Intentando corregir el problema...",
        "installation_complete": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                       ¡INSTALACIÓN COMPLETADA! 🎉                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "installed_packages": "📦 Paquetes instalados:",
        "getting_started": """
🚀 CÓMO EMPEZAR:

  • Para iniciar Reticulum:  rnsd
  • Para ejecutar NomadNet:  nomadnet
  • Para configurar RNode:   rnodeconf
  • Carpeta de configuración: ~/.reticulum/
  
  📚 Documentación: https://reticulum.network/
  💬 Comunidad: https://github.com/markqvist/Reticulum
""",
        "press_enter": "Presiona Enter para continuar...",
        "goodbye": "👋 ¡Gracias por usar el Instalador Reticulum! ¡Adiós!",
        "confirm_install": "¿Instalar los paquetes seleccionados? (s/n): ",
        "yes": "s",
        "no": "n",
        "upgrading_pip": "📦 Actualizando pip a la última versión...",
        "pip_upgraded": "✅ ¡Pip actualizado exitosamente!",
        "checking_python": "🐍 Verificando instalación de Python...",
        "python_ok": "✅ ¡Python está instalado correctamente!",
        "installing_pip": "📦 Instalando pip...",
        "root_warning": """
⚠️  ADVERTENCIA: Ejecutando como root/administrador
    
    Se recomienda ejecutar este instalador como usuario normal.
    ¿Continuar de todos modos? (s/n): """,
        "venv_info": """
💡 CONSEJO: Para una instalación más limpia, considera usar un entorno virtual:
   python3 -m venv ~/reticulum-env
   source ~/reticulum-env/bin/activate
   Luego ejecuta este instalador de nuevo.
   
   ¿Continuar con la instalación del sistema? (s/n): """,
        "package_descriptions": {
            "rns": "Biblioteca principal Reticulum Network Stack",
            "lxmf": "Lightweight Extensible Message Format",
            "nomadnet": "Comunicador Reticulum basado en terminal",
            "sideband": "Aplicación de mensajería GUI",
            "rnodeconf": "Herramienta de configuración hardware RNode",
            "lxmf-tools": "Utilidades y daemons LXMF"
        },
        "already_installed": "ℹ️  Ya instalado:",
        "will_upgrade": "(será actualizado)",
        "network_error": "❌ Error de red. Verifica tu conexión a internet.",
        "permission_error": "❌ Permiso denegado. Intenta con sudo o usa --user.",
        "unknown_error": "❌ Ocurrió un error desconocido.",
        "attempting_user_install": "🔧 Intentando instalación a nivel de usuario...",
        "attempting_break_packages": "🔧 Intentando instalación con --break-system-packages...",
        "main_menu": "📋 Menú Principal",
        "back_to_menu": "Presiona Enter para volver al menú principal...",
        "checking_installed": "🔍 Verificando paquetes instalados...",
        "upgrade_available": "⬆️  Actualización disponible:",
        "current_version": "   Actual:",
        "latest_version": "   Última:",
        "no_packages_selected": "❌ Ningún paquete seleccionado.",
        "select_at_least_one": "Selecciona al menos un paquete.",
        "dependency_note": "📝 Nota: RNS se instalará automáticamente ya que es requerido por otros paquetes.",
        "install_order": "📋 Orden de instalación (dependencias primero):",
        "step": "Paso",
        "of": "de",
        "skipping": "⏭️  Omitido (ya actualizado):",
        "total_time": "⏱️  Tiempo total de instalación:",
        "seconds": "segundos",
        "minutes": "minutos",
    },
    
    "de": {
        "lang_name": "Deutsch",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RETICULUM NETWORK SUITE INSTALLATEUR                      ║
║                                                                              ║
║  Willkommen! Dieser Installateur hilft dir bei der Einrichtung der          ║
║  Reticulum Network Stack Software auf deinem System. Alles ist automatisch. ║
║                                                                              ║
║  Was ist Reticulum?                                                          ║
║  Reticulum ist ein kryptographie-basierter Netzwerk-Stack zum Aufbau        ║
║  widerstandsfähiger Netze über jedes Medium - LoRa, WiFi, Internet, usw.    ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "select_language": "🌐 Please select your language / Bitte wählen Sie Ihre Sprache:",
        "checking_system": "🔍 Überprüfe dein System...",
        "system_info": "📋 Systeminformationen:",
        "os_label": "   Betriebssystem:",
        "python_version": "   Python-Version:",
        "pip_version": "   Pip-Version:",
        "checking_deps": "🔧 Überprüfe Abhängigkeiten...",
        "installing_deps": "📦 Installiere erforderliche Abhängigkeiten...",
        "deps_ok": "✅ Alle Abhängigkeiten sind erfüllt!",
        "select_packages": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    WÄHLE DIE ZU INSTALLIERENDEN PAKETE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Verfügbare Pakete:

  [1] 📡 RNS (Reticulum Network Stack)
      Die Kern-Netzwerkbibliothek - ERFORDERLICH für alle anderen Pakete
      
  [2] 💬 LXMF (Lightweight Extensible Message Format)
      Nachrichtenprotokoll auf Reticulum für asynchrone Nachrichtenübermittlung
      
  [3] 🖥️  NomadNet
      Terminal-basierte Kommunikationsplattform mit Seiten und Messaging
      
  [4] 📱 Sideband
      Mobile/Desktop-App für LXMF-Messaging (GUI-Anwendung)
      
  [5] 🔧 RNode Configuration Tool
      Werkzeug zur Konfiguration von RNode LoRa-Hardware
      
  [6] 📻 LXMF Tools (lxmfd, lxmessaging, usw.)
      Zusätzliche LXMF-Dienstprogramme und Daemons

  [A] 🎁 ALLE Pakete installieren (empfohlen für Anfänger)
  
  [Q] ❌ Installateur beenden
""",
        "enter_choice": "Gib deine Wahl ein (1-6, A für alle, Q zum Beenden): ",
        "invalid_choice": "❌ Ungültige Wahl. Bitte versuche es erneut.",
        "installing": "📦 Installiere",
        "install_success": "✅ Erfolgreich installiert",
        "install_failed": "❌ Installation fehlgeschlagen für",
        "error_details": "   Fehlerdetails:",
        "retry_prompt": "Möchtest du es erneut versuchen? (j/n): ",
        "fix_attempting": "🔧 Versuche das Problem zu beheben...",
        "installation_complete": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                       INSTALLATION ABGESCHLOSSEN! 🎉                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "installed_packages": "📦 Installierte Pakete:",
        "getting_started": """
🚀 ERSTE SCHRITTE:

  • Um Reticulum zu starten:  rnsd
  • Um NomadNet auszuführen:  nomadnet
  • Um RNode zu konfigurieren: rnodeconf
  • Konfigurationsordner: ~/.reticulum/
  
  📚 Dokumentation: https://reticulum.network/
  💬 Community: https://github.com/markqvist/Reticulum
""",
        "press_enter": "Drücke Enter um fortzufahren...",
        "goodbye": "👋 Danke für die Nutzung des Reticulum Installateurs! Auf Wiedersehen!",
        "confirm_install": "Ausgewählte Pakete installieren? (j/n): ",
        "yes": "j",
        "no": "n",
        "upgrading_pip": "📦 Aktualisiere pip auf die neueste Version...",
        "pip_upgraded": "✅ Pip erfolgreich aktualisiert!",
        "checking_python": "🐍 Überprüfe Python-Installation...",
        "python_ok": "✅ Python ist korrekt installiert!",
        "installing_pip": "📦 Installiere pip...",
        "root_warning": """
⚠️  WARNUNG: Ausführung als root/Administrator
    
    Es wird empfohlen, diesen Installateur als normaler Benutzer auszuführen.
    Trotzdem fortfahren? (j/n): """,
        "venv_info": """
💡 TIPP: Für eine sauberere Installation erwäge eine virtuelle Umgebung:
   python3 -m venv ~/reticulum-env
   source ~/reticulum-env/bin/activate
   Dann führe diesen Installateur erneut aus.
   
   Mit systemweiter Installation fortfahren? (j/n): """,
        "package_descriptions": {
            "rns": "Kern Reticulum Network Stack Bibliothek",
            "lxmf": "Lightweight Extensible Message Format",
            "nomadnet": "Terminal-basierter Reticulum-Kommunikator",
            "sideband": "GUI-Messaging-Anwendung",
            "rnodeconf": "RNode-Hardware-Konfigurationswerkzeug",
            "lxmf-tools": "LXMF-Dienstprogramme und Daemons"
        },
        "already_installed": "ℹ️  Bereits installiert:",
        "will_upgrade": "(wird aktualisiert)",
        "network_error": "❌ Netzwerkfehler. Bitte überprüfe deine Internetverbindung.",
        "permission_error": "❌ Zugriff verweigert. Versuche es mit sudo oder verwende --user.",
        "unknown_error": "❌ Ein unbekannter Fehler ist aufgetreten.",
        "attempting_user_install": "🔧 Versuche Installation auf Benutzerebene...",
        "attempting_break_packages": "🔧 Versuche Installation mit --break-system-packages...",
        "main_menu": "📋 Hauptmenü",
        "back_to_menu": "Drücke Enter um zum Hauptmenü zurückzukehren...",
        "checking_installed": "🔍 Überprüfe installierte Pakete...",
        "upgrade_available": "⬆️  Aktualisierung verfügbar:",
        "current_version": "   Aktuell:",
        "latest_version": "   Neueste:",
        "no_packages_selected": "❌ Keine Pakete ausgewählt.",
        "select_at_least_one": "Bitte wähle mindestens ein Paket.",
        "dependency_note": "📝 Hinweis: RNS wird automatisch installiert, da es von anderen Paketen benötigt wird.",
        "install_order": "📋 Installationsreihenfolge (Abhängigkeiten zuerst):",
        "step": "Schritt",
        "of": "von",
        "skipping": "⏭️  Übersprungen (bereits aktuell):",
        "total_time": "⏱️  Gesamte Installationszeit:",
        "seconds": "Sekunden",
        "minutes": "Minuten",
    },
    
    "ru": {
        "lang_name": "Русский",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    УСТАНОВЩИК RETICULUM NETWORK SUITE                        ║
║                                                                              ║
║  Добро пожаловать! Этот установщик поможет вам настроить программное        ║
║  обеспечение Reticulum Network Stack на вашей системе. Всё автоматизировано.║
║                                                                              ║
║  Что такое Reticulum?                                                        ║
║  Reticulum - это сетевой стек на основе криптографии для построения         ║
║  устойчивых сетей, работающих через любую среду - LoRa, WiFi, Интернет      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "select_language": "🌐 Please select your language / Выберите язык:",
        "checking_system": "🔍 Проверка вашей системы...",
        "system_info": "📋 Информация о системе:",
        "os_label": "   Операционная система:",
        "python_version": "   Версия Python:",
        "pip_version": "   Версия Pip:",
        "checking_deps": "🔧 Проверка зависимостей...",
        "installing_deps": "📦 Установка необходимых зависимостей...",
        "deps_ok": "✅ Все зависимости удовлетворены!",
        "select_packages": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      ВЫБЕРИТЕ ПАКЕТЫ ДЛЯ УСТАНОВКИ                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Доступные пакеты:

  [1] 📡 RNS (Reticulum Network Stack)
      Основная сетевая библиотека - ТРЕБУЕТСЯ для всех других пакетов
      
  [2] 💬 LXMF (Lightweight Extensible Message Format)
      Протокол сообщений на основе Reticulum для асинхронной переписки
      
  [3] 🖥️  NomadNet
      Терминальная платформа связи со страницами и сообщениями
      
  [4] 📱 Sideband
      Мобильное/десктопное приложение для LXMF-сообщений (GUI)
      
  [5] 🔧 RNode Configuration Tool
      Инструмент для настройки аппаратных устройств RNode LoRa
      
  [6] 📻 LXMF Tools (lxmfd, lxmessaging и др.)
      Дополнительные утилиты и демоны LXMF

  [A] 🎁 Установить ВСЕ пакеты (рекомендуется для начинающих)
  
  [Q] ❌ Выйти из установщика
""",
        "enter_choice": "Введите ваш выбор (1-6, A для всех, Q для выхода): ",
        "invalid_choice": "❌ Неверный выбор. Попробуйте снова.",
        "installing": "📦 Установка",
        "install_success": "✅ Успешно установлено",
        "install_failed": "❌ Ошибка установки",
        "error_details": "   Подробности ошибки:",
        "retry_prompt": "Хотите попробовать снова? (д/н): ",
        "fix_attempting": "🔧 Попытка исправить проблему...",
        "installation_complete": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        УСТАНОВКА ЗАВЕРШЕНА! 🎉                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "installed_packages": "📦 Установленные пакеты:",
        "getting_started": """
🚀 НАЧАЛО РАБОТЫ:

  • Для запуска Reticulum:   rnsd
  • Для запуска NomadNet:    nomadnet
  • Для настройки RNode:     rnodeconf
  • Папка конфигурации: ~/.reticulum/
  
  📚 Документация: https://reticulum.network/
  💬 Сообщество: https://github.com/markqvist/Reticulum
""",
        "press_enter": "Нажмите Enter для продолжения...",
        "goodbye": "👋 Спасибо за использование установщика Reticulum! До свидания!",
        "confirm_install": "Установить выбранные пакеты? (д/н): ",
        "yes": "д",
        "no": "н",
        "upgrading_pip": "📦 Обновление pip до последней версии...",
        "pip_upgraded": "✅ Pip успешно обновлён!",
        "checking_python": "🐍 Проверка установки Python...",
        "python_ok": "✅ Python установлен правильно!",
        "installing_pip": "📦 Установка pip...",
        "root_warning": """
⚠️  ПРЕДУПРЕЖДЕНИЕ: Запуск от имени root/администратора
    
    Рекомендуется запускать этот установщик как обычный пользователь.
    Продолжить всё равно? (д/н): """,
        "venv_info": """
💡 СОВЕТ: Для более чистой установки рассмотрите использование виртуальной среды:
   python3 -m venv ~/reticulum-env
   source ~/reticulum-env/bin/activate
   Затем запустите этот установщик снова.
   
   Продолжить с системной установкой? (д/н): """,
        "package_descriptions": {
            "rns": "Основная библиотека Reticulum Network Stack",
            "lxmf": "Lightweight Extensible Message Format",
            "nomadnet": "Терминальный коммуникатор Reticulum",
            "sideband": "GUI-приложение для обмена сообщениями",
            "rnodeconf": "Инструмент настройки оборудования RNode",
            "lxmf-tools": "Утилиты и демоны LXMF"
        },
        "already_installed": "ℹ️  Уже установлено:",
        "will_upgrade": "(будет обновлено)",
        "network_error": "❌ Ошибка сети. Проверьте подключение к интернету.",
        "permission_error": "❌ Доступ запрещён. Попробуйте с sudo или используйте --user.",
        "unknown_error": "❌ Произошла неизвестная ошибка.",
        "attempting_user_install": "🔧 Попытка установки на уровне пользователя...",
        "attempting_break_packages": "🔧 Попытка установки с --break-system-packages...",
        "main_menu": "📋 Главное меню",
        "back_to_menu": "Нажмите Enter для возврата в главное меню...",
        "checking_installed": "🔍 Проверка установленных пакетов...",
        "upgrade_available": "⬆️  Доступно обновление:",
        "current_version": "   Текущая:",
        "latest_version": "   Последняя:",
        "no_packages_selected": "❌ Пакеты не выбраны.",
        "select_at_least_one": "Пожалуйста, выберите хотя бы один пакет.",
        "dependency_note": "📝 Примечание: RNS будет установлен автоматически, так как он требуется другим пакетам.",
        "install_order": "📋 Порядок установки (сначала зависимости):",
        "step": "Шаг",
        "of": "из",
        "skipping": "⏭️  Пропущено (уже обновлено):",
        "total_time": "⏱️  Общее время установки:",
        "seconds": "секунд",
        "minutes": "минут",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PACKAGE DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

PACKAGES = {
    "1": {
        "name": "rns",
        "pip_name": "rns",
        "display_name": "RNS (Reticulum Network Stack)",
        "dependencies": [],
        "order": 1,
    },
    "2": {
        "name": "lxmf",
        "pip_name": "lxmf",
        "display_name": "LXMF",
        "dependencies": ["rns"],
        "order": 2,
    },
    "3": {
        "name": "nomadnet",
        "pip_name": "nomadnet",
        "display_name": "NomadNet",
        "dependencies": ["rns", "lxmf"],
        "order": 3,
    },
    "4": {
        "name": "sideband",
        "pip_name": "sbapp",
        "display_name": "Sideband",
        "dependencies": ["rns", "lxmf"],
        "order": 4,
    },
    "5": {
        "name": "rnodeconf",
        "pip_name": "rnodeconf",
        "display_name": "RNode Configuration Tool",
        "dependencies": ["rns"],
        "order": 5,
    },
    "6": {
        "name": "lxmf-tools",
        "pip_name": "lxmf",
        "display_name": "LXMF Tools",
        "dependencies": ["rns", "lxmf"],
        "extra_packages": ["lxmf"],
        "order": 6,
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# INSTALLER CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ReticulumInstaller:
    def __init__(self):
        self.lang = "en"
        self.installed_packages = []
        self.failed_packages = []
        self.python_cmd = sys.executable
        self.pip_cmd = None
        self.use_break_system_packages = False
        self.use_user_install = False
        
    def t(self, key):
        """Get translated string"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_slow(self, text, delay=0.02):
        """Print text with a slight delay for visual effect"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def run_command(self, cmd, capture=True, show_output=False):
        """Run a shell command and return result"""
        try:
            if show_output:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    text=True,
                    capture_output=False
                )
                return result.returncode == 0, "", ""
            else:
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True
                )
                return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)
    
    def select_language(self):
        """Display language selection menu"""
        self.clear_screen()
        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                         🌐 LANGUAGE SELECTION                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🇬🇧 English
  [2] 🇮🇹 Italiano  
  [3] 🇪🇸 Español
  [4] 🇩🇪 Deutsch
  [5] 🇷🇺 Русский

""")
        while True:
            choice = input("  Enter your choice (1-5): ").strip()
            if choice == "1":
                self.lang = "en"
                break
            elif choice == "2":
                self.lang = "it"
                break
            elif choice == "3":
                self.lang = "es"
                break
            elif choice == "4":
                self.lang = "de"
                break
            elif choice == "5":
                self.lang = "ru"
                break
            else:
                print("  ❌ Invalid choice. Please enter 1-5.")
    
    def show_welcome(self):
        """Display welcome message"""
        self.clear_screen()
        print(self.t("welcome"))
        input(f"  {self.t('press_enter')}")
    
    def check_system(self):
        """Check system requirements"""
        self.clear_screen()
        print(f"\n{self.t('checking_system')}\n")
        time.sleep(0.5)
        
        # System info
        print(self.t("system_info"))
        print(f"{self.t('os_label')} {platform.system()} {platform.release()}")
        print(f"{self.t('python_version')} {platform.python_version()}")
        
        # Check pip
        success, stdout, _ = self.run_command(f"{self.python_cmd} -m pip --version")
        if success:
            pip_version = stdout.split()[1] if stdout else "Unknown"
            print(f"{self.t('pip_version')} {pip_version}")
            self.pip_cmd = f"{self.python_cmd} -m pip"
        else:
            print(f"\n{self.t('installing_pip')}")
            self.run_command(f"{self.python_cmd} -m ensurepip --upgrade")
            self.pip_cmd = f"{self.python_cmd} -m pip"
        
        print()
        
        # Check if running as root
        if os.geteuid() == 0 if hasattr(os, 'geteuid') else False:
            response = input(self.t("root_warning")).strip().lower()
            if response != self.t("yes"):
                print(f"\n{self.t('goodbye')}")
                sys.exit(0)
        
        # Check for externally managed environment (PEP 668)
        self._check_externally_managed()
        
        input(f"\n  {self.t('press_enter')}")
    
    def _check_externally_managed(self):
        """Check if we're in an externally managed environment"""
        # Try a test install to see if we need special flags
        success, _, stderr = self.run_command(
            f"{self.pip_cmd} install --dry-run pip 2>&1"
        )
        
        if "externally-managed-environment" in stderr.lower():
            print(f"\n{self.t('attempting_break_packages')}")
            self.use_break_system_packages = True
        elif "permission" in stderr.lower():
            print(f"\n{self.t('attempting_user_install')}")
            self.use_user_install = True
    
    def get_pip_install_cmd(self, package):
        """Get the appropriate pip install command with all necessary flags"""
        cmd = f"{self.pip_cmd} install --upgrade {package}"
        
        if self.use_break_system_packages:
            cmd += " --break-system-packages"
        
        if self.use_user_install:
            cmd += " --user"
        
        return cmd
    
    def check_package_installed(self, pip_name):
        """Check if a package is already installed"""
        success, stdout, _ = self.run_command(f"{self.pip_cmd} show {pip_name}")
        if success:
            # Extract version
            for line in stdout.split('\n'):
                if line.startswith('Version:'):
                    return True, line.split(':')[1].strip()
        return False, None
    
    def upgrade_pip(self):
        """Upgrade pip to latest version"""
        print(f"\n{self.t('upgrading_pip')}")
        cmd = self.get_pip_install_cmd("pip")
        success, _, stderr = self.run_command(cmd, show_output=True)
        if success:
            print(self.t("pip_upgraded"))
        return success
    
    def select_packages(self):
        """Display package selection menu and get user choices"""
        while True:
            self.clear_screen()
            print(self.t("select_packages"))
            
            # Show currently installed packages
            print(f"\n{self.t('checking_installed')}")
            for key, pkg in PACKAGES.items():
                installed, version = self.check_package_installed(pkg["pip_name"])
                if installed:
                    print(f"  {self.t('already_installed')} {pkg['display_name']} (v{version})")
            
            print()
            choice = input(self.t("enter_choice")).strip().upper()
            
            if choice == 'Q':
                print(f"\n{self.t('goodbye')}")
                sys.exit(0)
            elif choice == 'A':
                return list(PACKAGES.keys())
            elif choice in PACKAGES:
                return [choice]
            elif ',' in choice:
                # Allow multiple selections like "1,2,3"
                selections = [c.strip() for c in choice.split(',')]
                if all(s in PACKAGES for s in selections):
                    return selections
            
            print(f"\n{self.t('invalid_choice')}")
            time.sleep(1)
    
    def resolve_dependencies(self, selected_keys):
        """Resolve package dependencies and return installation order"""
        packages_to_install = set()
        
        for key in selected_keys:
            pkg = PACKAGES[key]
            packages_to_install.add(key)
            
            # Add dependencies
            for dep in pkg["dependencies"]:
                for k, p in PACKAGES.items():
                    if p["name"] == dep or p["pip_name"] == dep:
                        packages_to_install.add(k)
        
        # Sort by installation order
        sorted_packages = sorted(
            packages_to_install,
            key=lambda k: PACKAGES[k]["order"]
        )
        
        return sorted_packages
    
    def install_package(self, package_key):
        """Install a single package with error handling and retries"""
        pkg = PACKAGES[package_key]
        pip_name = pkg["pip_name"]
        display_name = pkg["display_name"]
        
        print(f"\n{'─' * 60}")
        print(f"{self.t('installing')} {display_name}...")
        print(f"{'─' * 60}")
        
        # Check if already installed
        installed, version = self.check_package_installed(pip_name)
        if installed:
            print(f"  {self.t('already_installed')} {display_name} (v{version})")
        
        # Install/upgrade the package
        cmd = self.get_pip_install_cmd(pip_name)
        
        max_retries = 3
        for attempt in range(max_retries):
            print(f"\n  📥 {cmd}\n")
            success, stdout, stderr = self.run_command(cmd, show_output=True)
            
            if success:
                print(f"\n  {self.t('install_success')} {display_name}! ✅")
                self.installed_packages.append(display_name)
                return True
            
            # Handle errors
            error_msg = stderr.lower() if stderr else ""
            
            if "externally-managed-environment" in error_msg:
                print(f"\n  {self.t('attempting_break_packages')}")
                self.use_break_system_packages = True
                cmd = self.get_pip_install_cmd(pip_name)
                continue
            
            if "permission" in error_msg:
                print(f"\n  {self.t('attempting_user_install')}")
                self.use_user_install = True
                cmd = self.get_pip_install_cmd(pip_name)
                continue
            
            if "network" in error_msg or "connection" in error_msg:
                print(f"\n  {self.t('network_error')}")
            
            if attempt < max_retries - 1:
                print(f"\n  {self.t('fix_attempting')}")
                time.sleep(2)
            else:
                print(f"\n  {self.t('install_failed')} {display_name}")
                print(f"  {self.t('error_details')}")
                print(f"    {stderr[:200] if stderr else 'Unknown error'}")
                self.failed_packages.append(display_name)
                
                retry = input(f"\n  {self.t('retry_prompt')}").strip().lower()
                if retry == self.t("yes"):
                    return self.install_package(package_key)
                return False
        
        return False
    
    def install_packages(self, package_keys):
        """Install all selected packages"""
        self.clear_screen()
        
        # Resolve dependencies
        install_order = self.resolve_dependencies(package_keys)
        
        print(f"\n{self.t('install_order')}")
        for i, key in enumerate(install_order, 1):
            pkg = PACKAGES[key]
            print(f"  {i}. {pkg['display_name']}")
        
        print()
        confirm = input(self.t("confirm_install")).strip().lower()
        if confirm != self.t("yes"):
            return
        
        # Upgrade pip first
        self.upgrade_pip()
        
        # Install packages
        start_time = time.time()
        total = len(install_order)
        
        for i, key in enumerate(install_order, 1):
            pkg = PACKAGES[key]
            print(f"\n{'═' * 60}")
            print(f"  {self.t('step')} {i} {self.t('of')} {total}: {pkg['display_name']}")
            print(f"{'═' * 60}")
            
            self.install_package(key)
        
        # Calculate total time
        elapsed = time.time() - start_time
        if elapsed > 60:
            time_str = f"{elapsed/60:.1f} {self.t('minutes')}"
        else:
            time_str = f"{elapsed:.0f} {self.t('seconds')}"
        
        # Show completion summary
        self.show_completion_summary(time_str)
    
    def show_completion_summary(self, time_str):
        """Show installation completion summary"""
        self.clear_screen()
        print(self.t("installation_complete"))
        
        if self.installed_packages:
            print(f"{self.t('installed_packages')}")
            for pkg in self.installed_packages:
                print(f"  ✅ {pkg}")
        
        if self.failed_packages:
            print(f"\n❌ Failed packages:")
            for pkg in self.failed_packages:
                print(f"  ❌ {pkg}")
        
        print(f"\n{self.t('total_time')} {time_str}")
        print(self.t("getting_started"))
        
        input(f"\n{self.t('press_enter')}")
    
    def run(self):
        """Main installer loop"""
        try:
            self.select_language()
            self.show_welcome()
            self.check_system()
            
            while True:
                selected = self.select_packages()
                if selected:
                    self.install_packages(selected)
                    
                    # Ask if user wants to install more
                    self.clear_screen()
                    print(f"\n{self.t('main_menu')}")
                    again = input(f"\n  Install more packages? ({self.t('yes')}/{self.t('no')}): ").strip().lower()
                    if again != self.t("yes"):
                        break
            
            print(f"\n{self.t('goodbye')}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n{self.t('goodbye')}\n")
            sys.exit(0)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Your version: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    
    installer = ReticulumInstaller()
    installer.run()


if __name__ == "__main__":
    main()
