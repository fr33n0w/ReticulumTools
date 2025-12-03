#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║              NOMADNET - INTERACTIVE CONFIGURATOR                             ║
║                                                                              ║
║  Configure your NomadNet installation interactively                         ║
║  Edit ~/.nomadnetwork/config with proper formatting and validation          ║
║                                                                              ║
║  Languages: English, Italiano, Español, Deutsch, Русский                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import shutil
import time
import re
from pathlib import Path
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# LANGUAGE TRANSLATIONS
# ══════════════════════════════════════════════════════════════════════════════

TRANSLATIONS = {
    "en": {
        "lang_name": "English",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOMADNET - INTERACTIVE CONFIGURATOR                       ║
║                                                                              ║
║  This tool helps you configure NomadNet interactively.                      ║
║  It will edit your ~/.nomadnetwork/config file safely.                      ║
║                                                                              ║
║  A backup will be created before any changes are made.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  NomadNet config not found at:",
        "create_default": "Would you like to create a default config? (y/n): ",
        "creating_default": "📝 Creating default NomadNet configuration...",
        "run_nomadnet_first": "💡 Tip: Run 'nomadnet' once to generate a default config, or let us create one.",
        "config_found": "✅ Found NomadNet config at:",
        "backup_created": "💾 Backup created:",
        "permission_denied": "❌ Permission denied. Try running with sudo or fix permissions.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 View current configuration
  [2] 👤 Edit client settings (display name, propagation, etc.)
  [3] 🖥️  Edit text UI settings (intro time, colors, editor)
  [4] 📡 Edit node settings (enable hosting, announce interval)
  [5] 📄 Page hosting information
  [6] 💾 Save and exit
  [7] ❌ Exit without saving

""",
        "enter_choice": "Enter your choice: ",
        "invalid_choice": "❌ Invalid choice. Please try again.",
        "press_enter": "Press Enter to continue...",
        "yes": "y",
        "no": "n",
        "save_changes": "💾 Save changes to config? (y/n): ",
        "changes_saved": "✅ Configuration saved successfully!",
        "no_changes": "ℹ️  No changes to save.",
        "exit_without_save": "⚠️  Exit without saving changes? (y/n): ",
        "goodbye": "👋 Thank you for using NomadNet Configurator!",
        "current_value": "Current value:",
        "new_value": "New value (press Enter to keep current): ",
        "enabled": "enabled",
        "disabled": "disabled",
        "client_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          CLIENT SETTINGS                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 👤 Display name: {display_name}
  [2] 📧 Enable propagation node: {propagation}
  [3] 🔔 Announce at startup: {announce_startup}
  [4] ⏰ Announce interval (minutes): {announce_interval}
  [5] 🔙 Back to main menu

""",
        "textui_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          TEXT UI SETTINGS                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] ⏱️  Intro screen time (seconds): {intro_time}
  [2] 🖊️  Default editor: {editor}
  [3] 🌈 Colormode (dark/light/mono): {colormode}
  [4] 🌙 Use glyphs (symbols): {glyphs}
  [5] 🔠 Mouse support: {mouse}
  [6] 🔙 Back to main menu

""",
        "node_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                           NODE SETTINGS                                      ║
║                                                                              ║
║  Enable node hosting to serve pages and files to other NomadNet users!      ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📡 Enable node hosting: {enabled}
  [2] 📛 Node name: {name}
  [3] ⏰ Announce interval (minutes): {interval}
  [4] 📄 Default homepage: {homepage}
  [5] 🔙 Back to main menu

""",
        "page_hosting_info": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        📄 PAGE HOSTING INFORMATION                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

To host pages on your NomadNet node, you need to:

1️⃣  ENABLE NODE HOSTING
    Set 'enable_node = yes' in your config (use menu option 4)

2️⃣  CREATE YOUR PAGES
    Your pages should be placed in:
    
    📁 {pages_path}
    
    Create this folder if it doesn't exist!

3️⃣  PAGE FORMAT
    Pages use the Micron markup format (.mu extension)
    Your homepage should be named: index.mu
    
    Example page (index.mu):
    ─────────────────────────────────────────
    `!Welcome to My Node
    
    >This is my NomadNet node!
    
    Here you can find:
    `[Links`:/page/about.mu]
    `[Files`::file/myfile.txt]
    ─────────────────────────────────────────

4️⃣  HOST FILES
    Files to share should be placed in:
    
    📁 {files_path}

5️⃣  AFTER CHANGES
    Restart NomadNet to apply changes:
    $ nomadnet --daemon  (for headless)
    $ nomadnet           (for interactive)

📚 For more info on Micron markup:
   https://github.com/markqvist/NomadNet

""",
        "enter_display_name": "Enter your display name: ",
        "enter_node_name": "Enter node name (shown to visitors): ",
        "enter_editor": "Enter editor command (e.g., nano, vim, editor): ",
        "enter_intro_time": "Enter intro screen time in seconds (0 to skip): ",
        "enter_announce_interval": "Enter announce interval in minutes (0 to disable): ",
        "enter_homepage": "Enter homepage filename (e.g., index.mu): ",
        "select_colormode": "Select color mode:\n  [1] dark\n  [2] light\n  [3] mono\nChoice: ",
        "setting_updated": "✅ Setting updated!",
        "enable_propagation": "Enable LXMF propagation node? (y/n): ",
        "enable_node": "Enable node hosting? (y/n): ",
        "enable_announce_startup": "Announce at startup? (y/n): ",
        "enable_glyphs": "Use glyphs (symbols)? (y/n): ",
        "enable_mouse": "Enable mouse support? (y/n): ",
        "config_location": "📁 Config file location:",
        "view_config": "📋 Current Configuration:",
        "pages_folder": "📁 Pages folder:",
        "files_folder": "📁 Files folder:",
        "folder_exists": "✅ Folder exists",
        "folder_missing": "⚠️  Folder does not exist - will be created when you run NomadNet",
        "create_folders": "Would you like to create the hosting folders now? (y/n): ",
        "folders_created": "✅ Folders created!",
        "example_page_created": "📄 Example homepage created:",
    },
    
    "it": {
        "lang_name": "Italiano",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOMADNET - CONFIGURATORE INTERATTIVO                      ║
║                                                                              ║
║  Questo strumento ti aiuta a configurare NomadNet in modo interattivo.      ║
║  Modificherà il file ~/.nomadnetwork/config in sicurezza.                   ║
║                                                                              ║
║  Verrà creato un backup prima di qualsiasi modifica.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Config NomadNet non trovato in:",
        "create_default": "Vuoi creare una configurazione predefinita? (s/n): ",
        "creating_default": "📝 Creazione configurazione NomadNet predefinita...",
        "run_nomadnet_first": "💡 Suggerimento: Esegui 'nomadnet' una volta per generare un config predefinito.",
        "config_found": "✅ Trovato config NomadNet in:",
        "backup_created": "💾 Backup creato:",
        "permission_denied": "❌ Permesso negato. Prova con sudo o correggi i permessi.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MENU PRINCIPALE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Visualizza configurazione attuale
  [2] 👤 Modifica impostazioni client (nome, propagazione, ecc.)
  [3] 🖥️  Modifica impostazioni UI testo (intro, colori, editor)
  [4] 📡 Modifica impostazioni nodo (abilita hosting, intervallo annunci)
  [5] 📄 Informazioni hosting pagine
  [6] 💾 Salva ed esci
  [7] ❌ Esci senza salvare

""",
        "enter_choice": "Inserisci la tua scelta: ",
        "invalid_choice": "❌ Scelta non valida. Riprova.",
        "press_enter": "Premi Invio per continuare...",
        "yes": "s",
        "no": "n",
        "save_changes": "💾 Salvare le modifiche? (s/n): ",
        "changes_saved": "✅ Configurazione salvata con successo!",
        "no_changes": "ℹ️  Nessuna modifica da salvare.",
        "exit_without_save": "⚠️  Uscire senza salvare le modifiche? (s/n): ",
        "goodbye": "👋 Grazie per aver usato il Configuratore NomadNet!",
        "current_value": "Valore attuale:",
        "new_value": "Nuovo valore (premi Invio per mantenere): ",
        "enabled": "abilitato",
        "disabled": "disabilitato",
        "client_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        IMPOSTAZIONI CLIENT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 👤 Nome visualizzato: {display_name}
  [2] 📧 Abilita nodo propagazione: {propagation}
  [3] 🔔 Annuncia all'avvio: {announce_startup}
  [4] ⏰ Intervallo annunci (minuti): {announce_interval}
  [5] 🔙 Torna al menu principale

""",
        "textui_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        IMPOSTAZIONI UI TESTO                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] ⏱️  Tempo schermata intro (secondi): {intro_time}
  [2] 🖊️  Editor predefinito: {editor}
  [3] 🌈 Modalità colore (dark/light/mono): {colormode}
  [4] 🌙 Usa glifi (simboli): {glyphs}
  [5] 🔠 Supporto mouse: {mouse}
  [6] 🔙 Torna al menu principale

""",
        "node_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         IMPOSTAZIONI NODO                                    ║
║                                                                              ║
║  Abilita l'hosting del nodo per servire pagine e file ad altri utenti!      ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📡 Abilita hosting nodo: {enabled}
  [2] 📛 Nome nodo: {name}
  [3] ⏰ Intervallo annunci (minuti): {interval}
  [4] 📄 Homepage predefinita: {homepage}
  [5] 🔙 Torna al menu principale

""",
        "page_hosting_info": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                     📄 INFORMAZIONI HOSTING PAGINE                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Per ospitare pagine sul tuo nodo NomadNet, devi:

1️⃣  ABILITARE L'HOSTING DEL NODO
    Imposta 'enable_node = yes' nel tuo config (usa opzione menu 4)

2️⃣  CREARE LE TUE PAGINE
    Le tue pagine devono essere in:
    
    📁 {pages_path}
    
    Crea questa cartella se non esiste!

3️⃣  FORMATO PAGINE
    Le pagine usano il formato Micron (.mu)
    La tua homepage dovrebbe chiamarsi: index.mu
    
    Esempio pagina (index.mu):
    ─────────────────────────────────────────
    `!Benvenuto nel Mio Nodo
    
    >Questo è il mio nodo NomadNet!
    
    Qui puoi trovare:
    `[Link`:/page/about.mu]
    `[File`::file/miofile.txt]
    ─────────────────────────────────────────

4️⃣  OSPITARE FILE
    I file da condividere vanno in:
    
    📁 {files_path}

5️⃣  DOPO LE MODIFICHE
    Riavvia NomadNet per applicare le modifiche:
    $ nomadnet --daemon  (per headless)
    $ nomadnet           (per interattivo)

📚 Per maggiori info sul markup Micron:
   https://github.com/markqvist/NomadNet

""",
        "enter_display_name": "Inserisci il tuo nome visualizzato: ",
        "enter_node_name": "Inserisci nome nodo (visibile ai visitatori): ",
        "enter_editor": "Inserisci comando editor (es. nano, vim, editor): ",
        "enter_intro_time": "Inserisci tempo schermata intro in secondi (0 per saltare): ",
        "enter_announce_interval": "Inserisci intervallo annunci in minuti (0 per disabilitare): ",
        "enter_homepage": "Inserisci nome file homepage (es. index.mu): ",
        "select_colormode": "Seleziona modalità colore:\n  [1] dark\n  [2] light\n  [3] mono\nScelta: ",
        "setting_updated": "✅ Impostazione aggiornata!",
        "enable_propagation": "Abilitare nodo propagazione LXMF? (s/n): ",
        "enable_node": "Abilitare hosting nodo? (s/n): ",
        "enable_announce_startup": "Annunciare all'avvio? (s/n): ",
        "enable_glyphs": "Usare glifi (simboli)? (s/n): ",
        "enable_mouse": "Abilitare supporto mouse? (s/n): ",
        "config_location": "📁 Posizione file config:",
        "view_config": "📋 Configurazione Attuale:",
        "pages_folder": "📁 Cartella pagine:",
        "files_folder": "📁 Cartella file:",
        "folder_exists": "✅ Cartella esistente",
        "folder_missing": "⚠️  Cartella non esistente - verrà creata quando esegui NomadNet",
        "create_folders": "Vuoi creare le cartelle hosting ora? (s/n): ",
        "folders_created": "✅ Cartelle create!",
        "example_page_created": "📄 Homepage esempio creata:",
    },
    
    "es": {
        "lang_name": "Español",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOMADNET - CONFIGURADOR INTERACTIVO                       ║
║                                                                              ║
║  Esta herramienta te ayuda a configurar NomadNet interactivamente.          ║
║  Editará tu archivo ~/.nomadnetwork/config de forma segura.                 ║
║                                                                              ║
║  Se creará una copia de seguridad antes de cualquier cambio.                ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Config de NomadNet no encontrado en:",
        "create_default": "¿Deseas crear una configuración predeterminada? (s/n): ",
        "creating_default": "📝 Creando configuración NomadNet predeterminada...",
        "run_nomadnet_first": "💡 Consejo: Ejecuta 'nomadnet' una vez para generar un config predeterminado.",
        "config_found": "✅ Encontrado config NomadNet en:",
        "backup_created": "💾 Copia de seguridad creada:",
        "permission_denied": "❌ Permiso denegado. Intenta con sudo o corrige los permisos.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MENÚ PRINCIPAL                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Ver configuración actual
  [2] 👤 Editar configuración cliente (nombre, propagación, etc.)
  [3] 🖥️  Editar configuración UI texto (intro, colores, editor)
  [4] 📡 Editar configuración nodo (habilitar hosting, intervalo anuncios)
  [5] 📄 Información de hosting de páginas
  [6] 💾 Guardar y salir
  [7] ❌ Salir sin guardar

""",
        "enter_choice": "Ingresa tu elección: ",
        "invalid_choice": "❌ Elección inválida. Intenta de nuevo.",
        "press_enter": "Presiona Enter para continuar...",
        "yes": "s",
        "no": "n",
        "save_changes": "💾 ¿Guardar los cambios? (s/n): ",
        "changes_saved": "✅ ¡Configuración guardada exitosamente!",
        "no_changes": "ℹ️  No hay cambios que guardar.",
        "exit_without_save": "⚠️  ¿Salir sin guardar los cambios? (s/n): ",
        "goodbye": "👋 ¡Gracias por usar el Configurador NomadNet!",
        "current_value": "Valor actual:",
        "new_value": "Nuevo valor (presiona Enter para mantener): ",
        "enabled": "habilitado",
        "disabled": "deshabilitado",
        "client_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CONFIGURACIÓN CLIENTE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 👤 Nombre a mostrar: {display_name}
  [2] 📧 Habilitar nodo propagación: {propagation}
  [3] 🔔 Anunciar al inicio: {announce_startup}
  [4] ⏰ Intervalo de anuncios (minutos): {announce_interval}
  [5] 🔙 Volver al menú principal

""",
        "textui_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CONFIGURACIÓN UI TEXTO                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] ⏱️  Tiempo pantalla intro (segundos): {intro_time}
  [2] 🖊️  Editor predeterminado: {editor}
  [3] 🌈 Modo de color (dark/light/mono): {colormode}
  [4] 🌙 Usar glifos (símbolos): {glyphs}
  [5] 🔠 Soporte de ratón: {mouse}
  [6] 🔙 Volver al menú principal

""",
        "node_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CONFIGURACIÓN DE NODO                                 ║
║                                                                              ║
║  ¡Habilita el hosting de nodo para servir páginas y archivos a otros!       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📡 Habilitar hosting de nodo: {enabled}
  [2] 📛 Nombre del nodo: {name}
  [3] ⏰ Intervalo de anuncios (minutos): {interval}
  [4] 📄 Página de inicio: {homepage}
  [5] 🔙 Volver al menú principal

""",
        "page_hosting_info": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                  📄 INFORMACIÓN DE HOSTING DE PÁGINAS                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Para hospedar páginas en tu nodo NomadNet, necesitas:

1️⃣  HABILITAR EL HOSTING DE NODO
    Configura 'enable_node = yes' en tu config (usa opción de menú 4)

2️⃣  CREAR TUS PÁGINAS
    Tus páginas deben estar en:
    
    📁 {pages_path}
    
    ¡Crea esta carpeta si no existe!

3️⃣  FORMATO DE PÁGINAS
    Las páginas usan el formato Micron (.mu)
    Tu página de inicio debe llamarse: index.mu
    
    Ejemplo de página (index.mu):
    ─────────────────────────────────────────
    `!Bienvenido a Mi Nodo
    
    >¡Este es mi nodo NomadNet!
    
    Aquí puedes encontrar:
    `[Enlaces`:/page/about.mu]
    `[Archivos`::file/miarchivo.txt]
    ─────────────────────────────────────────

4️⃣  HOSPEDAR ARCHIVOS
    Los archivos a compartir van en:
    
    📁 {files_path}

5️⃣  DESPUÉS DE CAMBIOS
    Reinicia NomadNet para aplicar cambios:
    $ nomadnet --daemon  (para headless)
    $ nomadnet           (para interactivo)

📚 Para más info sobre el markup Micron:
   https://github.com/markqvist/NomadNet

""",
        "enter_display_name": "Ingresa tu nombre a mostrar: ",
        "enter_node_name": "Ingresa nombre del nodo (visible para visitantes): ",
        "enter_editor": "Ingresa comando del editor (ej. nano, vim, editor): ",
        "enter_intro_time": "Ingresa tiempo de pantalla intro en segundos (0 para omitir): ",
        "enter_announce_interval": "Ingresa intervalo de anuncios en minutos (0 para deshabilitar): ",
        "enter_homepage": "Ingresa nombre de archivo de inicio (ej. index.mu): ",
        "select_colormode": "Selecciona modo de color:\n  [1] dark\n  [2] light\n  [3] mono\nElección: ",
        "setting_updated": "✅ ¡Configuración actualizada!",
        "enable_propagation": "¿Habilitar nodo de propagación LXMF? (s/n): ",
        "enable_node": "¿Habilitar hosting de nodo? (s/n): ",
        "enable_announce_startup": "¿Anunciar al inicio? (s/n): ",
        "enable_glyphs": "¿Usar glifos (símbolos)? (s/n): ",
        "enable_mouse": "¿Habilitar soporte de ratón? (s/n): ",
        "config_location": "📁 Ubicación del archivo config:",
        "view_config": "📋 Configuración Actual:",
        "pages_folder": "📁 Carpeta de páginas:",
        "files_folder": "📁 Carpeta de archivos:",
        "folder_exists": "✅ Carpeta existe",
        "folder_missing": "⚠️  Carpeta no existe - se creará cuando ejecutes NomadNet",
        "create_folders": "¿Deseas crear las carpetas de hosting ahora? (s/n): ",
        "folders_created": "✅ ¡Carpetas creadas!",
        "example_page_created": "📄 Página de inicio de ejemplo creada:",
    },
    
    "de": {
        "lang_name": "Deutsch",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOMADNET - INTERAKTIVER KONFIGURATOR                      ║
║                                                                              ║
║  Dieses Tool hilft dir, NomadNet interaktiv zu konfigurieren.               ║
║  Es bearbeitet deine ~/.nomadnetwork/config Datei sicher.                   ║
║                                                                              ║
║  Ein Backup wird vor Änderungen erstellt.                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  NomadNet-Konfiguration nicht gefunden unter:",
        "create_default": "Möchtest du eine Standardkonfiguration erstellen? (j/n): ",
        "creating_default": "📝 Erstelle Standard-NomadNet-Konfiguration...",
        "run_nomadnet_first": "💡 Tipp: Führe 'nomadnet' einmal aus, um eine Standardkonfiguration zu generieren.",
        "config_found": "✅ NomadNet-Konfiguration gefunden unter:",
        "backup_created": "💾 Backup erstellt:",
        "permission_denied": "❌ Zugriff verweigert. Versuche es mit sudo oder korrigiere die Berechtigungen.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              HAUPTMENÜ                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Aktuelle Konfiguration anzeigen
  [2] 👤 Client-Einstellungen bearbeiten (Name, Propagierung, etc.)
  [3] 🖥️  Text-UI-Einstellungen bearbeiten (Intro, Farben, Editor)
  [4] 📡 Knoten-Einstellungen bearbeiten (Hosting aktivieren, Ankündigungsintervall)
  [5] 📄 Informationen zum Seiten-Hosting
  [6] 💾 Speichern und beenden
  [7] ❌ Beenden ohne zu speichern

""",
        "enter_choice": "Gib deine Wahl ein: ",
        "invalid_choice": "❌ Ungültige Wahl. Bitte versuche es erneut.",
        "press_enter": "Drücke Enter zum Fortfahren...",
        "yes": "j",
        "no": "n",
        "save_changes": "💾 Änderungen speichern? (j/n): ",
        "changes_saved": "✅ Konfiguration erfolgreich gespeichert!",
        "no_changes": "ℹ️  Keine Änderungen zum Speichern.",
        "exit_without_save": "⚠️  Ohne Speichern beenden? (j/n): ",
        "goodbye": "👋 Danke für die Nutzung des NomadNet-Konfigurators!",
        "current_value": "Aktueller Wert:",
        "new_value": "Neuer Wert (Enter drücken zum Beibehalten): ",
        "enabled": "aktiviert",
        "disabled": "deaktiviert",
        "client_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CLIENT-EINSTELLUNGEN                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 👤 Anzeigename: {display_name}
  [2] 📧 Propagierungsknoten aktivieren: {propagation}
  [3] 🔔 Bei Start ankündigen: {announce_startup}
  [4] ⏰ Ankündigungsintervall (Minuten): {announce_interval}
  [5] 🔙 Zurück zum Hauptmenü

""",
        "textui_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        TEXT-UI-EINSTELLUNGEN                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] ⏱️  Intro-Bildschirmzeit (Sekunden): {intro_time}
  [2] 🖊️  Standard-Editor: {editor}
  [3] 🌈 Farbmodus (dark/light/mono): {colormode}
  [4] 🌙 Glyphen verwenden (Symbole): {glyphs}
  [5] 🔠 Maus-Unterstützung: {mouse}
  [6] 🔙 Zurück zum Hauptmenü

""",
        "node_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        KNOTEN-EINSTELLUNGEN                                  ║
║                                                                              ║
║  Aktiviere Knoten-Hosting, um Seiten und Dateien für andere bereitzustellen!║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📡 Knoten-Hosting aktivieren: {enabled}
  [2] 📛 Knotenname: {name}
  [3] ⏰ Ankündigungsintervall (Minuten): {interval}
  [4] 📄 Standard-Homepage: {homepage}
  [5] 🔙 Zurück zum Hauptmenü

""",
        "page_hosting_info": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    📄 INFORMATIONEN ZUM SEITEN-HOSTING                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Um Seiten auf deinem NomadNet-Knoten zu hosten, musst du:

1️⃣  KNOTEN-HOSTING AKTIVIEREN
    Setze 'enable_node = yes' in deiner Konfiguration (Menüoption 4)

2️⃣  DEINE SEITEN ERSTELLEN
    Deine Seiten sollten hier platziert werden:
    
    📁 {pages_path}
    
    Erstelle diesen Ordner, wenn er nicht existiert!

3️⃣  SEITENFORMAT
    Seiten verwenden das Micron-Markup-Format (.mu)
    Deine Homepage sollte heißen: index.mu
    
    Beispielseite (index.mu):
    ─────────────────────────────────────────
    `!Willkommen auf Meinem Knoten
    
    >Dies ist mein NomadNet-Knoten!
    
    Hier findest du:
    `[Links`:/page/about.mu]
    `[Dateien`::file/meinedatei.txt]
    ─────────────────────────────────────────

4️⃣  DATEIEN HOSTEN
    Zu teilende Dateien gehören in:
    
    📁 {files_path}

5️⃣  NACH ÄNDERUNGEN
    Starte NomadNet neu, um Änderungen anzuwenden:
    $ nomadnet --daemon  (für headless)
    $ nomadnet           (für interaktiv)

📚 Für mehr Infos zum Micron-Markup:
   https://github.com/markqvist/NomadNet

""",
        "enter_display_name": "Gib deinen Anzeigenamen ein: ",
        "enter_node_name": "Gib Knotennamen ein (für Besucher sichtbar): ",
        "enter_editor": "Gib Editor-Befehl ein (z.B. nano, vim, editor): ",
        "enter_intro_time": "Gib Intro-Bildschirmzeit in Sekunden ein (0 zum Überspringen): ",
        "enter_announce_interval": "Gib Ankündigungsintervall in Minuten ein (0 zum Deaktivieren): ",
        "enter_homepage": "Gib Homepage-Dateinamen ein (z.B. index.mu): ",
        "select_colormode": "Wähle Farbmodus:\n  [1] dark\n  [2] light\n  [3] mono\nWahl: ",
        "setting_updated": "✅ Einstellung aktualisiert!",
        "enable_propagation": "LXMF-Propagierungsknoten aktivieren? (j/n): ",
        "enable_node": "Knoten-Hosting aktivieren? (j/n): ",
        "enable_announce_startup": "Bei Start ankündigen? (j/n): ",
        "enable_glyphs": "Glyphen verwenden (Symbole)? (j/n): ",
        "enable_mouse": "Maus-Unterstützung aktivieren? (j/n): ",
        "config_location": "📁 Konfigurationsdatei-Speicherort:",
        "view_config": "📋 Aktuelle Konfiguration:",
        "pages_folder": "📁 Seiten-Ordner:",
        "files_folder": "📁 Dateien-Ordner:",
        "folder_exists": "✅ Ordner existiert",
        "folder_missing": "⚠️  Ordner existiert nicht - wird erstellt, wenn du NomadNet startest",
        "create_folders": "Möchtest du die Hosting-Ordner jetzt erstellen? (j/n): ",
        "folders_created": "✅ Ordner erstellt!",
        "example_page_created": "📄 Beispiel-Homepage erstellt:",
    },
    
    "ru": {
        "lang_name": "Русский",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    NOMADNET - ИНТЕРАКТИВНЫЙ КОНФИГУРАТОР                     ║
║                                                                              ║
║  Этот инструмент поможет вам настроить NomadNet интерактивно.               ║
║  Он безопасно отредактирует ваш файл ~/.nomadnetwork/config.                ║
║                                                                              ║
║  Резервная копия будет создана перед любыми изменениями.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Конфигурация NomadNet не найдена в:",
        "create_default": "Создать конфигурацию по умолчанию? (д/н): ",
        "creating_default": "📝 Создание конфигурации NomadNet по умолчанию...",
        "run_nomadnet_first": "💡 Совет: Запустите 'nomadnet' один раз для генерации конфигурации по умолчанию.",
        "config_found": "✅ Найдена конфигурация NomadNet в:",
        "backup_created": "💾 Резервная копия создана:",
        "permission_denied": "❌ Доступ запрещён. Попробуйте с sudo или исправьте права доступа.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              ГЛАВНОЕ МЕНЮ                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Показать текущую конфигурацию
  [2] 👤 Редактировать настройки клиента (имя, распространение и т.д.)
  [3] 🖥️  Редактировать настройки UI (интро, цвета, редактор)
  [4] 📡 Редактировать настройки узла (хостинг, интервал объявлений)
  [5] 📄 Информация о хостинге страниц
  [6] 💾 Сохранить и выйти
  [7] ❌ Выйти без сохранения

""",
        "enter_choice": "Введите ваш выбор: ",
        "invalid_choice": "❌ Неверный выбор. Попробуйте снова.",
        "press_enter": "Нажмите Enter для продолжения...",
        "yes": "д",
        "no": "н",
        "save_changes": "💾 Сохранить изменения? (д/н): ",
        "changes_saved": "✅ Конфигурация успешно сохранена!",
        "no_changes": "ℹ️  Нет изменений для сохранения.",
        "exit_without_save": "⚠️  Выйти без сохранения изменений? (д/н): ",
        "goodbye": "👋 Спасибо за использование конфигуратора NomadNet!",
        "current_value": "Текущее значение:",
        "new_value": "Новое значение (Enter для сохранения текущего): ",
        "enabled": "включено",
        "disabled": "выключено",
        "client_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        НАСТРОЙКИ КЛИЕНТА                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 👤 Отображаемое имя: {display_name}
  [2] 📧 Включить узел распространения: {propagation}
  [3] 🔔 Объявить при запуске: {announce_startup}
  [4] ⏰ Интервал объявлений (минуты): {announce_interval}
  [5] 🔙 Вернуться в главное меню

""",
        "textui_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        НАСТРОЙКИ ТЕКСТОВОГО UI                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] ⏱️  Время заставки (секунды): {intro_time}
  [2] 🖊️  Редактор по умолчанию: {editor}
  [3] 🌈 Режим цвета (dark/light/mono): {colormode}
  [4] 🌙 Использовать глифы (символы): {glyphs}
  [5] 🔠 Поддержка мыши: {mouse}
  [6] 🔙 Вернуться в главное меню

""",
        "node_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          НАСТРОЙКИ УЗЛА                                      ║
║                                                                              ║
║  Включите хостинг узла для предоставления страниц и файлов другим!          ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📡 Включить хостинг узла: {enabled}
  [2] 📛 Имя узла: {name}
  [3] ⏰ Интервал объявлений (минуты): {interval}
  [4] 📄 Домашняя страница по умолчанию: {homepage}
  [5] 🔙 Вернуться в главное меню

""",
        "page_hosting_info": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   📄 ИНФОРМАЦИЯ О ХОСТИНГЕ СТРАНИЦ                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Для размещения страниц на вашем узле NomadNet, вам нужно:

1️⃣  ВКЛЮЧИТЬ ХОСТИНГ УЗЛА
    Установите 'enable_node = yes' в вашем конфиге (опция меню 4)

2️⃣  СОЗДАТЬ ВАШИ СТРАНИЦЫ
    Ваши страницы должны находиться в:
    
    📁 {pages_path}
    
    Создайте эту папку, если она не существует!

3️⃣  ФОРМАТ СТРАНИЦ
    Страницы используют формат разметки Micron (.mu)
    Ваша домашняя страница должна называться: index.mu
    
    Пример страницы (index.mu):
    ─────────────────────────────────────────
    `!Добро пожаловать на Мой Узел
    
    >Это мой узел NomadNet!
    
    Здесь вы можете найти:
    `[Ссылки`:/page/about.mu]
    `[Файлы`::file/myfile.txt]
    ─────────────────────────────────────────

4️⃣  РАЗМЕЩЕНИЕ ФАЙЛОВ
    Файлы для обмена размещаются в:
    
    📁 {files_path}

5️⃣  ПОСЛЕ ИЗМЕНЕНИЙ
    Перезапустите NomadNet для применения изменений:
    $ nomadnet --daemon  (для headless)
    $ nomadnet           (для интерактивного)

📚 Для информации о разметке Micron:
   https://github.com/markqvist/NomadNet

""",
        "enter_display_name": "Введите ваше отображаемое имя: ",
        "enter_node_name": "Введите имя узла (видимое посетителям): ",
        "enter_editor": "Введите команду редактора (напр. nano, vim, editor): ",
        "enter_intro_time": "Введите время заставки в секундах (0 для пропуска): ",
        "enter_announce_interval": "Введите интервал объявлений в минутах (0 для отключения): ",
        "enter_homepage": "Введите имя файла домашней страницы (напр. index.mu): ",
        "select_colormode": "Выберите режим цвета:\n  [1] dark\n  [2] light\n  [3] mono\nВыбор: ",
        "setting_updated": "✅ Настройка обновлена!",
        "enable_propagation": "Включить узел распространения LXMF? (д/н): ",
        "enable_node": "Включить хостинг узла? (д/н): ",
        "enable_announce_startup": "Объявлять при запуске? (д/н): ",
        "enable_glyphs": "Использовать глифы (символы)? (д/н): ",
        "enable_mouse": "Включить поддержку мыши? (д/н): ",
        "config_location": "📁 Расположение файла конфигурации:",
        "view_config": "📋 Текущая Конфигурация:",
        "pages_folder": "📁 Папка страниц:",
        "files_folder": "📁 Папка файлов:",
        "folder_exists": "✅ Папка существует",
        "folder_missing": "⚠️  Папка не существует - будет создана при запуске NomadNet",
        "create_folders": "Создать папки хостинга сейчас? (д/н): ",
        "folders_created": "✅ Папки созданы!",
        "example_page_created": "📄 Примерная домашняя страница создана:",
    },
}

# Default NomadNet config template
DEFAULT_CONFIG = """# This is the default NomadNet config file.
# You should edit it to suit your needs.

[client]
enable_client = yes
user_interface = text
downloads_path = ~/Downloads

[textui]
intro_time = 1
colormode = dark
editor = editor
glyphs = yes
mouse_enabled = yes

[node]
enable_node = no
node_name = None
announce_at_start = yes
announce_interval = 360

[propagation]
enable_propagation_node = no

"""

# Example Micron page
EXAMPLE_PAGE = """`c`!Welcome to my NomadNet Node`!

`a

`b>center>This node is running on the Reticulum Network`b

`a

Here you can find information and resources.

`F222
`*Menu`*
`[About`:/page/about.mu]
`[Files`:/file/]
`f

`a

`B333`=`cHosted with NomadNet`=`b
"""


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class NomadNetConfigurator:
    def __init__(self):
        self.lang = "en"
        self.config_path = None
        self.nomadnet_dir = None
        self.config_content = ""
        self.original_content = ""
        self.has_changes = False
        self.find_config()
        
    def t(self, key):
        """Get translated string"""
        return TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key, key)
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def find_config(self):
        """Find the NomadNet config file"""
        # Check common locations
        possible_paths = [
            Path.home() / ".nomadnetwork" / "config",
            Path("/etc/nomadnetwork/config"),
            Path.home() / ".config" / "nomadnetwork" / "config",
        ]
        
        for path in possible_paths:
            if path.exists():
                self.config_path = path
                self.nomadnet_dir = path.parent
                return
        
        # Default to standard location
        self.config_path = Path.home() / ".nomadnetwork" / "config"
        self.nomadnet_dir = Path.home() / ".nomadnetwork"
    
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
            lang_map = {"1": "en", "2": "it", "3": "es", "4": "de", "5": "ru"}
            if choice in lang_map:
                self.lang = lang_map[choice]
                break
            print("  ❌ Invalid choice. Please enter 1-5.")
    
    def load_config(self):
        """Load the configuration file"""
        if not self.config_path.exists():
            print(f"\n{self.t('config_not_found')}")
            print(f"  {self.config_path}")
            print(f"\n{self.t('run_nomadnet_first')}")
            
            response = input(f"\n{self.t('create_default')}").strip().lower()
            if response == self.t("yes"):
                self.create_default_config()
            else:
                return False
        
        try:
            with open(self.config_path, 'r') as f:
                self.config_content = f.read()
                self.original_content = self.config_content
            print(f"\n{self.t('config_found')}")
            print(f"  {self.config_path}")
            return True
        except PermissionError:
            print(f"\n{self.t('permission_denied')}")
            return False
        except Exception as e:
            print(f"\n❌ Error loading config: {e}")
            return False
    
    def create_default_config(self):
        """Create a default configuration file"""
        print(f"\n{self.t('creating_default')}")
        
        # Create directory structure
        self.nomadnet_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_path, 'w') as f:
                f.write(DEFAULT_CONFIG)
            self.config_content = DEFAULT_CONFIG
            self.original_content = DEFAULT_CONFIG
            print(f"✅ Created: {self.config_path}")
            
            # Create storage directories
            self.create_hosting_folders()
            
        except PermissionError:
            print(f"\n{self.t('permission_denied')}")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return False
        return True
    
    def create_backup(self):
        """Create a backup of the current config"""
        if self.config_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.config_path.with_suffix(f".backup_{timestamp}")
            shutil.copy2(self.config_path, backup_path)
            print(f"\n{self.t('backup_created')}")
            print(f"  {backup_path}")
    
    def save_config(self):
        """Save the configuration file"""
        if self.config_content == self.original_content:
            print(f"\n{self.t('no_changes')}")
            return True
        
        response = input(f"\n{self.t('save_changes')}").strip().lower()
        if response != self.t("yes"):
            return False
        
        self.create_backup()
        
        try:
            with open(self.config_path, 'w') as f:
                f.write(self.config_content)
            self.original_content = self.config_content
            self.has_changes = False
            print(f"\n{self.t('changes_saved')}")
            return True
        except PermissionError:
            print(f"\n{self.t('permission_denied')}")
            return False
        except Exception as e:
            print(f"\n❌ Error saving config: {e}")
            return False
    
    def get_setting(self, section, key, default=""):
        """Get a setting value from config"""
        section_pattern = rf'\[{section}\](.*?)(?=\[[^\[]|\Z)'
        section_match = re.search(section_pattern, self.config_content, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(1)
            key_pattern = rf'^{key}\s*=\s*(.+)$'
            key_match = re.search(key_pattern, section_content, re.MULTILINE)
            if key_match:
                return key_match.group(1).strip()
        
        return default
    
    def set_setting(self, section, key, value):
        """Set a setting value in config"""
        section_pattern = rf'(\[{section}\])(.*?)(?=\[[^\[]|\Z)'
        section_match = re.search(section_pattern, self.config_content, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(2)
            key_pattern = rf'^({key}\s*=\s*)(.+)$'
            
            if re.search(key_pattern, section_content, re.MULTILINE):
                # Replace existing key
                new_section = re.sub(
                    key_pattern,
                    rf'\g<1>{value}',
                    section_content,
                    flags=re.MULTILINE
                )
                self.config_content = self.config_content.replace(
                    section_match.group(0),
                    section_match.group(1) + new_section
                )
            else:
                # Add new key to section
                new_content = section_match.group(0).rstrip() + f"\n{key} = {value}\n\n"
                self.config_content = self.config_content.replace(
                    section_match.group(0),
                    new_content
                )
        else:
            # Add new section with key
            self.config_content += f"\n[{section}]\n{key} = {value}\n"
        
        self.has_changes = True
    
    def view_config(self):
        """Display current configuration"""
        self.clear_screen()
        print(f"\n{self.t('view_config')}")
        print(f"{self.t('config_location')} {self.config_path}\n")
        print("─" * 78)
        print(self.config_content)
        print("─" * 78)
        input(f"\n{self.t('press_enter')}")
    
    def edit_client_settings(self):
        """Edit client settings"""
        while True:
            self.clear_screen()
            
            # Get current values
            display_name = self.get_setting("client", "user_name", "Anonymous Peer")
            propagation = self.get_setting("propagation", "enable_propagation_node", "no")
            announce_startup = self.get_setting("node", "announce_at_start", "yes")
            announce_interval = self.get_setting("client", "announce_interval", "360")
            
            prop_str = self.t("enabled") if propagation.lower() in ["yes", "true"] else self.t("disabled")
            ann_str = self.t("enabled") if announce_startup.lower() in ["yes", "true"] else self.t("disabled")
            
            print(self.t("client_settings").format(
                display_name=display_name,
                propagation=prop_str,
                announce_startup=ann_str,
                announce_interval=announce_interval
            ))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                new_name = input(self.t("enter_display_name")).strip()
                if new_name:
                    self.set_setting("client", "user_name", new_name)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "2":
                response = input(self.t("enable_propagation")).strip().lower()
                new_value = "yes" if response == self.t("yes") else "no"
                self.set_setting("propagation", "enable_propagation_node", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "3":
                response = input(self.t("enable_announce_startup")).strip().lower()
                new_value = "yes" if response == self.t("yes") else "no"
                self.set_setting("node", "announce_at_start", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "4":
                new_interval = input(self.t("enter_announce_interval")).strip()
                if new_interval.isdigit():
                    self.set_setting("client", "announce_interval", new_interval)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "5":
                break
    
    def edit_textui_settings(self):
        """Edit text UI settings"""
        while True:
            self.clear_screen()
            
            # Get current values
            intro_time = self.get_setting("textui", "intro_time", "1")
            editor = self.get_setting("textui", "editor", "editor")
            colormode = self.get_setting("textui", "colormode", "dark")
            glyphs = self.get_setting("textui", "glyphs", "yes")
            mouse = self.get_setting("textui", "mouse_enabled", "yes")
            
            glyphs_str = self.t("enabled") if glyphs.lower() in ["yes", "true"] else self.t("disabled")
            mouse_str = self.t("enabled") if mouse.lower() in ["yes", "true"] else self.t("disabled")
            
            print(self.t("textui_settings").format(
                intro_time=intro_time,
                editor=editor,
                colormode=colormode,
                glyphs=glyphs_str,
                mouse=mouse_str
            ))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                new_time = input(self.t("enter_intro_time")).strip()
                if new_time.isdigit():
                    self.set_setting("textui", "intro_time", new_time)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "2":
                new_editor = input(self.t("enter_editor")).strip()
                if new_editor:
                    self.set_setting("textui", "editor", new_editor)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "3":
                color_choice = input(self.t("select_colormode")).strip()
                color_map = {"1": "dark", "2": "light", "3": "mono"}
                if color_choice in color_map:
                    self.set_setting("textui", "colormode", color_map[color_choice])
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "4":
                response = input(self.t("enable_glyphs")).strip().lower()
                new_value = "yes" if response == self.t("yes") else "no"
                self.set_setting("textui", "glyphs", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "5":
                response = input(self.t("enable_mouse")).strip().lower()
                new_value = "yes" if response == self.t("yes") else "no"
                self.set_setting("textui", "mouse_enabled", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "6":
                break
    
    def edit_node_settings(self):
        """Edit node hosting settings"""
        while True:
            self.clear_screen()
            
            # Get current values
            enabled = self.get_setting("node", "enable_node", "no")
            name = self.get_setting("node", "node_name", "None")
            interval = self.get_setting("node", "announce_interval", "360")
            homepage = self.get_setting("node", "pages_path", "index.mu")
            
            enabled_str = self.t("enabled") if enabled.lower() in ["yes", "true"] else self.t("disabled")
            
            print(self.t("node_settings").format(
                enabled=enabled_str,
                name=name,
                interval=interval,
                homepage=homepage
            ))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                response = input(self.t("enable_node")).strip().lower()
                new_value = "yes" if response == self.t("yes") else "no"
                self.set_setting("node", "enable_node", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "2":
                new_name = input(self.t("enter_node_name")).strip()
                if new_name:
                    self.set_setting("node", "node_name", new_name)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "3":
                new_interval = input(self.t("enter_announce_interval")).strip()
                if new_interval.isdigit():
                    self.set_setting("node", "announce_interval", new_interval)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "4":
                new_homepage = input(self.t("enter_homepage")).strip()
                if new_homepage:
                    self.set_setting("node", "pages_path", new_homepage)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "5":
                break
    
    def show_page_hosting_info(self):
        """Show page hosting information"""
        self.clear_screen()
        
        pages_path = self.nomadnet_dir / "storage" / "pages"
        files_path = self.nomadnet_dir / "storage" / "files"
        
        print(self.t("page_hosting_info").format(
            pages_path=pages_path,
            files_path=files_path
        ))
        
        # Check if folders exist
        print(f"\n{self.t('pages_folder')} {pages_path}")
        if pages_path.exists():
            print(f"  {self.t('folder_exists')}")
        else:
            print(f"  {self.t('folder_missing')}")
        
        print(f"\n{self.t('files_folder')} {files_path}")
        if files_path.exists():
            print(f"  {self.t('folder_exists')}")
        else:
            print(f"  {self.t('folder_missing')}")
        
        # Offer to create folders
        if not pages_path.exists() or not files_path.exists():
            response = input(f"\n{self.t('create_folders')}").strip().lower()
            if response == self.t("yes"):
                self.create_hosting_folders()
        
        input(f"\n{self.t('press_enter')}")
    
    def create_hosting_folders(self):
        """Create the hosting folder structure"""
        pages_path = self.nomadnet_dir / "storage" / "pages"
        files_path = self.nomadnet_dir / "storage" / "files"
        
        try:
            pages_path.mkdir(parents=True, exist_ok=True)
            files_path.mkdir(parents=True, exist_ok=True)
            print(f"\n{self.t('folders_created')}")
            
            # Create example homepage if doesn't exist
            index_path = pages_path / "index.mu"
            if not index_path.exists():
                with open(index_path, 'w') as f:
                    f.write(EXAMPLE_PAGE)
                print(f"{self.t('example_page_created')} {index_path}")
                
        except Exception as e:
            print(f"\n❌ Error creating folders: {e}")
    
    def main_menu(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            print(self.t("main_menu"))
            
            # Show if there are unsaved changes
            if self.config_content != self.original_content:
                print("  ⚠️  You have unsaved changes!\n")
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                self.view_config()
            elif choice == "2":
                self.edit_client_settings()
            elif choice == "3":
                self.edit_textui_settings()
            elif choice == "4":
                self.edit_node_settings()
            elif choice == "5":
                self.show_page_hosting_info()
            elif choice == "6":
                self.save_config()
                print(f"\n{self.t('goodbye')}")
                break
            elif choice == "7":
                if self.config_content != self.original_content:
                    confirm = input(self.t("exit_without_save")).strip().lower()
                    if confirm != self.t("yes"):
                        continue
                print(f"\n{self.t('goodbye')}")
                break
            else:
                print(f"\n{self.t('invalid_choice')}")
                time.sleep(1)
    
    def run(self):
        """Main entry point"""
        try:
            self.select_language()
            
            self.clear_screen()
            print(self.t("welcome"))
            
            if not self.load_config():
                input(f"\n{self.t('press_enter')}")
                print(f"\n{self.t('goodbye')}")
                return
            
            input(f"\n{self.t('press_enter')}")
            
            self.main_menu()
            
        except KeyboardInterrupt:
            print(f"\n\n{self.t('goodbye')}")
            sys.exit(0)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Main entry point"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        sys.exit(1)
    
    configurator = NomadNetConfigurator()
    configurator.run()


if __name__ == "__main__":
    main()
