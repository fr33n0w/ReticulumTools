#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           RETICULUM NETWORK STACK - INTERACTIVE CONFIGURATOR                ║
║                                                                              ║
║  Configure your Reticulum installation interactively                        ║
║  Edit ~/.reticulum/config with proper formatting and validation             ║
║                                                                              ║
║  Languages: English, Italiano, Español, Deutsch, Русский                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import shutil
import time
import re
import subprocess
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
║              RETICULUM NETWORK STACK - INTERACTIVE CONFIGURATOR             ║
║                                                                              ║
║  This tool helps you configure Reticulum interactively.                     ║
║  It will edit your ~/.reticulum/config file safely.                         ║
║                                                                              ║
║  A backup will be created before any changes are made.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Reticulum config not found at:",
        "create_default": "Would you like to create a default config? (y/n): ",
        "creating_default": "📝 Creating default Reticulum configuration...",
        "run_rnsd_first": "💡 Tip: Run 'rnsd' once to generate a default config, or let us create one.",
        "config_found": "✅ Found Reticulum config at:",
        "backup_created": "💾 Backup created:",
        "permission_denied": "❌ Permission denied. Try running with sudo or fix permissions.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 View current configuration
  [2] ⚙️  Edit general settings (loglevel, transport, etc.)
  [3] 🌐 Manage interfaces
  [4] 📡 Add TCP Client Interfaces (connect to network)
  [5] 🔌 Quick Connect - Add recommended public nodes
  [6] 🔧 Check & Fix configuration
  [7] 💾 Save and exit
  [8] ❌ Exit without saving

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
        "goodbye": "👋 Thank you for using Reticulum Configurator!",
        "current_value": "Current value:",
        "new_value": "New value (press Enter to keep current): ",
        "enabled": "enabled",
        "disabled": "disabled",
        "interface_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          INTERFACE MANAGEMENT                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 List all interfaces
  [2] ✏️  Enable/Disable an interface
  [3] ❌ Remove an interface
  [4] ➕ Add new interface manually
  [5] 🔙 Back to main menu

""",
        "no_interfaces": "ℹ️  No interfaces found in configuration.",
        "interface_list": "📡 Current Interfaces:",
        "select_interface": "Select interface number: ",
        "interface_enabled": "✅ Interface enabled:",
        "interface_disabled": "🔴 Interface disabled:",
        "interface_removed": "🗑️  Interface removed:",
        "confirm_remove": "⚠️  Remove this interface? (y/n): ",
        "tcp_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      ADD TCP CLIENT INTERFACE                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🌍 RMAP.world (Reticulum Map - recommended)
  [2] 🇮🇪 Dublin Testnet Hub (official)
  [3] 🌐 BetweenTheBorders Hub (community)
  [4] 🇦🇺 Sydney RNS (community)
  [5] 🇩🇪 Germany Node (community)
  [6] ➕ Add custom TCP interface
  [7] 📦 Add ALL recommended nodes
  [8] 🔙 Back to main menu

""",
        "quick_connect": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         QUICK CONNECT SETUP                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

This will add a selection of reliable public nodes to get you connected
to the Reticulum network quickly.

Recommended nodes to add:
  • RMAP.world (port 4242) - Reticulum network map
  • Dublin Testnet Hub (port 4965) - Official testnet
  • BetweenTheBorders (port 4242) - Community hub

""",
        "add_all_confirm": "Add all recommended nodes? (y/n): ",
        "nodes_added": "✅ Nodes added successfully!",
        "interface_name": "Interface name (e.g., 'My Node'): ",
        "target_host": "Target host/IP: ",
        "target_port": "Target port (default 4242): ",
        "interface_added": "✅ Interface added:",
        "already_exists": "⚠️  An interface with similar settings already exists.",
        "general_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          GENERAL SETTINGS                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📊 Log level (0-7, current: {loglevel})
  [2] 🚀 Enable transport ({transport})
  [3] 🔒 Panic on unrecoverable error ({panic})
  [4] 🔙 Back to main menu

""",
        "loglevel_help": """
Log levels:
  0 = Critical only
  1 = Errors
  2 = Warnings  
  3 = Notices
  4 = Info (default)
  5 = Verbose
  6 = Debug
  7 = Extreme debug
""",
        "transport_help": """
Transport mode allows your node to route traffic for other nodes.
Enable this if you want to help the network or need to bridge interfaces.
""",
        "enter_loglevel": "Enter log level (0-7): ",
        "enable_transport": "Enable transport mode? (y/n): ",
        "setting_updated": "✅ Setting updated!",
        "view_config": "📋 Current Configuration:",
        "config_location": "📁 Config file location:",
        "check_fix_title": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CHECK & FIX CONFIGURATION                               ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "checking_config": "🔍 Checking configuration...",
        "config_valid": "✅ Configuration is valid!",
        "config_issues": "⚠️  Found {count} issue(s):",
        "fix_issues": "🔧 Would you like to fix these issues? (y/n): ",
        "fixing_issues": "🔧 Fixing issues...",
        "issues_fixed": "✅ All issues fixed!",
        "issue_section_missing": "Missing required section: [{section}]",
        "issue_key_missing": "Missing key '{key}' in [{section}]",
        "issue_bad_indentation": "Bad indentation in interface '{name}'",
        "issue_invalid_value": "Invalid value for '{key}': {value}",
        "issue_duplicate_interface": "Duplicate interface: {name}",
        "issue_empty_section": "Empty [interfaces] section",
        "testing_with_rnsd": "🧪 Testing with rnsd...",
        "rnsd_not_found": "⚠️  rnsd not found - cannot validate config",
        "rnsd_test_passed": "✅ rnsd validation passed!",
        "rnsd_test_failed": "❌ rnsd validation failed:",
    },
    
    "it": {
        "lang_name": "Italiano",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║              RETICULUM NETWORK STACK - CONFIGURATORE INTERATTIVO             ║
║                                                                              ║
║  Questo strumento ti aiuta a configurare Reticulum in modo interattivo.     ║
║  Modificherà il file ~/.reticulum/config in sicurezza.                      ║
║                                                                              ║
║  Verrà creato un backup prima di qualsiasi modifica.                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Config Reticulum non trovato in:",
        "create_default": "Vuoi creare una configurazione predefinita? (s/n): ",
        "creating_default": "📝 Creazione configurazione Reticulum predefinita...",
        "run_rnsd_first": "💡 Suggerimento: Esegui 'rnsd' una volta per generare un config predefinito.",
        "config_found": "✅ Trovato config Reticulum in:",
        "backup_created": "💾 Backup creato:",
        "permission_denied": "❌ Permesso negato. Prova con sudo o correggi i permessi.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MENU PRINCIPALE                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Visualizza configurazione attuale
  [2] ⚙️  Modifica impostazioni generali (loglevel, transport, ecc.)
  [3] 🌐 Gestisci interfacce
  [4] 📡 Aggiungi interfacce TCP Client (connetti alla rete)
  [5] 🔌 Connessione Rapida - Aggiungi nodi pubblici consigliati
  [6] 🔧 Controlla e Correggi configurazione
  [7] 💾 Salva ed esci
  [8] ❌ Esci senza salvare

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
        "goodbye": "👋 Grazie per aver usato il Configuratore Reticulum!",
        "current_value": "Valore attuale:",
        "new_value": "Nuovo valore (premi Invio per mantenere): ",
        "enabled": "abilitato",
        "disabled": "disabilitato",
        "interface_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        GESTIONE INTERFACCE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Elenca tutte le interfacce
  [2] ✏️  Abilita/Disabilita un'interfaccia
  [3] ❌ Rimuovi un'interfaccia
  [4] ➕ Aggiungi nuova interfaccia manualmente
  [5] 🔙 Torna al menu principale

""",
        "no_interfaces": "ℹ️  Nessuna interfaccia trovata nella configurazione.",
        "interface_list": "📡 Interfacce Attuali:",
        "select_interface": "Seleziona numero interfaccia: ",
        "interface_enabled": "✅ Interfaccia abilitata:",
        "interface_disabled": "🔴 Interfaccia disabilitata:",
        "interface_removed": "🗑️  Interfaccia rimossa:",
        "confirm_remove": "⚠️  Rimuovere questa interfaccia? (s/n): ",
        "tcp_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AGGIUNGI INTERFACCIA TCP CLIENT                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🌍 RMAP.world (Mappa Reticulum - consigliato)
  [2] 🇮🇪 Dublin Testnet Hub (ufficiale)
  [3] 🌐 BetweenTheBorders Hub (community)
  [4] 🇦🇺 Sydney RNS (community)
  [5] 🇩🇪 Nodo Germania (community)
  [6] ➕ Aggiungi interfaccia TCP personalizzata
  [7] 📦 Aggiungi TUTTI i nodi consigliati
  [8] 🔙 Torna al menu principale

""",
        "quick_connect": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CONFIGURAZIONE CONNESSIONE RAPIDA                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Questo aggiungerà una selezione di nodi pubblici affidabili per connetterti
rapidamente alla rete Reticulum.

Nodi consigliati da aggiungere:
  • RMAP.world (porta 4242) - Mappa rete Reticulum
  • Dublin Testnet Hub (porta 4965) - Testnet ufficiale
  • BetweenTheBorders (porta 4242) - Hub community

""",
        "add_all_confirm": "Aggiungere tutti i nodi consigliati? (s/n): ",
        "nodes_added": "✅ Nodi aggiunti con successo!",
        "interface_name": "Nome interfaccia (es. 'Mio Nodo'): ",
        "target_host": "Host/IP di destinazione: ",
        "target_port": "Porta di destinazione (predefinita 4242): ",
        "interface_added": "✅ Interfaccia aggiunta:",
        "already_exists": "⚠️  Un'interfaccia con impostazioni simili esiste già.",
        "general_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         IMPOSTAZIONI GENERALI                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📊 Livello log (0-7, attuale: {loglevel})
  [2] 🚀 Abilita transport ({transport})
  [3] 🔒 Panic su errore irreversibile ({panic})
  [4] 🔙 Torna al menu principale

""",
        "loglevel_help": """
Livelli di log:
  0 = Solo critici
  1 = Errori
  2 = Avvisi  
  3 = Notifiche
  4 = Info (predefinito)
  5 = Verbose
  6 = Debug
  7 = Debug estremo
""",
        "transport_help": """
La modalità transport permette al tuo nodo di instradare traffico per altri nodi.
Abilitala se vuoi aiutare la rete o devi collegare interfacce.
""",
        "enter_loglevel": "Inserisci livello log (0-7): ",
        "enable_transport": "Abilitare modalità transport? (s/n): ",
        "setting_updated": "✅ Impostazione aggiornata!",
        "view_config": "📋 Configurazione Attuale:",
        "config_location": "📁 Posizione file config:",
        "check_fix_title": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CONTROLLA E CORREGGI CONFIGURAZIONE                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "checking_config": "🔍 Controllo configurazione...",
        "config_valid": "✅ La configurazione è valida!",
        "config_issues": "⚠️  Trovati {count} problema/i:",
        "fix_issues": "🔧 Vuoi correggere questi problemi? (s/n): ",
        "fixing_issues": "🔧 Correzione in corso...",
        "issues_fixed": "✅ Tutti i problemi sono stati corretti!",
        "issue_section_missing": "Sezione mancante: [{section}]",
        "issue_key_missing": "Chiave '{key}' mancante in [{section}]",
        "issue_bad_indentation": "Indentazione errata nell'interfaccia '{name}'",
        "issue_invalid_value": "Valore non valido per '{key}': {value}",
        "issue_duplicate_interface": "Interfaccia duplicata: {name}",
        "issue_empty_section": "Sezione [interfaces] vuota",
        "testing_with_rnsd": "🧪 Test con rnsd...",
        "rnsd_not_found": "⚠️  rnsd non trovato - impossibile validare il config",
        "rnsd_test_passed": "✅ Validazione rnsd superata!",
        "rnsd_test_failed": "❌ Validazione rnsd fallita:",
    },
    
    "es": {
        "lang_name": "Español",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║              RETICULUM NETWORK STACK - CONFIGURADOR INTERACTIVO              ║
║                                                                              ║
║  Esta herramienta te ayuda a configurar Reticulum interactivamente.         ║
║  Editará tu archivo ~/.reticulum/config de forma segura.                    ║
║                                                                              ║
║  Se creará una copia de seguridad antes de cualquier cambio.                ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Config de Reticulum no encontrado en:",
        "create_default": "¿Deseas crear una configuración predeterminada? (s/n): ",
        "creating_default": "📝 Creando configuración Reticulum predeterminada...",
        "run_rnsd_first": "💡 Consejo: Ejecuta 'rnsd' una vez para generar un config predeterminado.",
        "config_found": "✅ Encontrado config Reticulum en:",
        "backup_created": "💾 Copia de seguridad creada:",
        "permission_denied": "❌ Permiso denegado. Intenta con sudo o corrige los permisos.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MENÚ PRINCIPAL                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Ver configuración actual
  [2] ⚙️  Editar configuración general (loglevel, transport, etc.)
  [3] 🌐 Gestionar interfaces
  [4] 📡 Añadir interfaces TCP Client (conectar a la red)
  [5] 🔌 Conexión Rápida - Añadir nodos públicos recomendados
  [6] 🔧 Verificar y Corregir configuración
  [7] 💾 Guardar y salir
  [8] ❌ Salir sin guardar

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
        "goodbye": "👋 ¡Gracias por usar el Configurador Reticulum!",
        "current_value": "Valor actual:",
        "new_value": "Nuevo valor (presiona Enter para mantener): ",
        "enabled": "habilitado",
        "disabled": "deshabilitado",
        "interface_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         GESTIÓN DE INTERFACES                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Listar todas las interfaces
  [2] ✏️  Habilitar/Deshabilitar una interfaz
  [3] ❌ Eliminar una interfaz
  [4] ➕ Añadir nueva interfaz manualmente
  [5] 🔙 Volver al menú principal

""",
        "no_interfaces": "ℹ️  No se encontraron interfaces en la configuración.",
        "interface_list": "📡 Interfaces Actuales:",
        "select_interface": "Selecciona número de interfaz: ",
        "interface_enabled": "✅ Interfaz habilitada:",
        "interface_disabled": "🔴 Interfaz deshabilitada:",
        "interface_removed": "🗑️  Interfaz eliminada:",
        "confirm_remove": "⚠️  ¿Eliminar esta interfaz? (s/n): ",
        "tcp_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AÑADIR INTERFAZ TCP CLIENT                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🌍 RMAP.world (Mapa Reticulum - recomendado)
  [2] 🇮🇪 Dublin Testnet Hub (oficial)
  [3] 🌐 BetweenTheBorders Hub (comunidad)
  [4] 🇦🇺 Sydney RNS (comunidad)
  [5] 🇩🇪 Nodo Alemania (comunidad)
  [6] ➕ Añadir interfaz TCP personalizada
  [7] 📦 Añadir TODOS los nodos recomendados
  [8] 🔙 Volver al menú principal

""",
        "quick_connect": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   CONFIGURACIÓN DE CONEXIÓN RÁPIDA                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

Esto añadirá una selección de nodos públicos confiables para conectarte
rápidamente a la red Reticulum.

Nodos recomendados a añadir:
  • RMAP.world (puerto 4242) - Mapa de red Reticulum
  • Dublin Testnet Hub (puerto 4965) - Testnet oficial
  • BetweenTheBorders (puerto 4242) - Hub comunitario

""",
        "add_all_confirm": "¿Añadir todos los nodos recomendados? (s/n): ",
        "nodes_added": "✅ ¡Nodos añadidos exitosamente!",
        "interface_name": "Nombre de interfaz (ej. 'Mi Nodo'): ",
        "target_host": "Host/IP de destino: ",
        "target_port": "Puerto de destino (predeterminado 4242): ",
        "interface_added": "✅ Interfaz añadida:",
        "already_exists": "⚠️  Ya existe una interfaz con configuración similar.",
        "general_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CONFIGURACIÓN GENERAL                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📊 Nivel de log (0-7, actual: {loglevel})
  [2] 🚀 Habilitar transport ({transport})
  [3] 🔒 Panic en error irrecuperable ({panic})
  [4] 🔙 Volver al menú principal

""",
        "loglevel_help": """
Niveles de log:
  0 = Solo críticos
  1 = Errores
  2 = Advertencias  
  3 = Avisos
  4 = Info (predeterminado)
  5 = Verbose
  6 = Debug
  7 = Debug extremo
""",
        "transport_help": """
El modo transport permite a tu nodo enrutar tráfico para otros nodos.
Habilítalo si quieres ayudar a la red o necesitas conectar interfaces.
""",
        "enter_loglevel": "Ingresa nivel de log (0-7): ",
        "enable_transport": "¿Habilitar modo transport? (s/n): ",
        "setting_updated": "✅ ¡Configuración actualizada!",
        "view_config": "📋 Configuración Actual:",
        "config_location": "📁 Ubicación del archivo config:",
        "check_fix_title": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   VERIFICAR Y CORREGIR CONFIGURACIÓN                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "checking_config": "🔍 Verificando configuración...",
        "config_valid": "✅ ¡La configuración es válida!",
        "config_issues": "⚠️  Se encontraron {count} problema(s):",
        "fix_issues": "🔧 ¿Deseas corregir estos problemas? (s/n): ",
        "fixing_issues": "🔧 Corrigiendo problemas...",
        "issues_fixed": "✅ ¡Todos los problemas han sido corregidos!",
        "issue_section_missing": "Sección faltante: [{section}]",
        "issue_key_missing": "Clave '{key}' faltante en [{section}]",
        "issue_bad_indentation": "Indentación incorrecta en interfaz '{name}'",
        "issue_invalid_value": "Valor inválido para '{key}': {value}",
        "issue_duplicate_interface": "Interfaz duplicada: {name}",
        "issue_empty_section": "Sección [interfaces] vacía",
        "testing_with_rnsd": "🧪 Probando con rnsd...",
        "rnsd_not_found": "⚠️  rnsd no encontrado - no se puede validar el config",
        "rnsd_test_passed": "✅ ¡Validación rnsd exitosa!",
        "rnsd_test_failed": "❌ Validación rnsd falló:",
    },
    
    "de": {
        "lang_name": "Deutsch",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║              RETICULUM NETWORK STACK - INTERAKTIVER KONFIGURATOR             ║
║                                                                              ║
║  Dieses Tool hilft dir, Reticulum interaktiv zu konfigurieren.              ║
║  Es bearbeitet deine ~/.reticulum/config Datei sicher.                      ║
║                                                                              ║
║  Ein Backup wird vor Änderungen erstellt.                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Reticulum-Konfiguration nicht gefunden unter:",
        "create_default": "Möchtest du eine Standardkonfiguration erstellen? (j/n): ",
        "creating_default": "📝 Erstelle Standard-Reticulum-Konfiguration...",
        "run_rnsd_first": "💡 Tipp: Führe 'rnsd' einmal aus, um eine Standardkonfiguration zu generieren.",
        "config_found": "✅ Reticulum-Konfiguration gefunden unter:",
        "backup_created": "💾 Backup erstellt:",
        "permission_denied": "❌ Zugriff verweigert. Versuche es mit sudo oder korrigiere die Berechtigungen.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              HAUPTMENÜ                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Aktuelle Konfiguration anzeigen
  [2] ⚙️  Allgemeine Einstellungen bearbeiten (loglevel, transport, etc.)
  [3] 🌐 Schnittstellen verwalten
  [4] 📡 TCP-Client-Schnittstellen hinzufügen (mit Netzwerk verbinden)
  [5] 🔌 Schnellverbindung - Empfohlene öffentliche Knoten hinzufügen
  [6] 🔧 Konfiguration prüfen und reparieren
  [7] 💾 Speichern und beenden
  [8] ❌ Beenden ohne zu speichern

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
        "goodbye": "👋 Danke für die Nutzung des Reticulum-Konfigurators!",
        "current_value": "Aktueller Wert:",
        "new_value": "Neuer Wert (Enter drücken zum Beibehalten): ",
        "enabled": "aktiviert",
        "disabled": "deaktiviert",
        "interface_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        SCHNITTSTELLENVERWALTUNG                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Alle Schnittstellen auflisten
  [2] ✏️  Schnittstelle aktivieren/deaktivieren
  [3] ❌ Schnittstelle entfernen
  [4] ➕ Neue Schnittstelle manuell hinzufügen
  [5] 🔙 Zurück zum Hauptmenü

""",
        "no_interfaces": "ℹ️  Keine Schnittstellen in der Konfiguration gefunden.",
        "interface_list": "📡 Aktuelle Schnittstellen:",
        "select_interface": "Wähle Schnittstellennummer: ",
        "interface_enabled": "✅ Schnittstelle aktiviert:",
        "interface_disabled": "🔴 Schnittstelle deaktiviert:",
        "interface_removed": "🗑️  Schnittstelle entfernt:",
        "confirm_remove": "⚠️  Diese Schnittstelle entfernen? (j/n): ",
        "tcp_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TCP-CLIENT-SCHNITTSTELLE HINZUFÜGEN                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🌍 RMAP.world (Reticulum-Karte - empfohlen)
  [2] 🇮🇪 Dublin Testnet Hub (offiziell)
  [3] 🌐 BetweenTheBorders Hub (Community)
  [4] 🇦🇺 Sydney RNS (Community)
  [5] 🇩🇪 Deutschland-Knoten (Community)
  [6] ➕ Benutzerdefinierte TCP-Schnittstelle hinzufügen
  [7] 📦 ALLE empfohlenen Knoten hinzufügen
  [8] 🔙 Zurück zum Hauptmenü

""",
        "quick_connect": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      SCHNELLVERBINDUNGS-EINRICHTUNG                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Dies fügt eine Auswahl zuverlässiger öffentlicher Knoten hinzu, um dich
schnell mit dem Reticulum-Netzwerk zu verbinden.

Empfohlene Knoten:
  • RMAP.world (Port 4242) - Reticulum-Netzwerkkarte
  • Dublin Testnet Hub (Port 4965) - Offizielles Testnet
  • BetweenTheBorders (Port 4242) - Community-Hub

""",
        "add_all_confirm": "Alle empfohlenen Knoten hinzufügen? (j/n): ",
        "nodes_added": "✅ Knoten erfolgreich hinzugefügt!",
        "interface_name": "Schnittstellenname (z.B. 'Mein Knoten'): ",
        "target_host": "Ziel-Host/IP: ",
        "target_port": "Ziel-Port (Standard 4242): ",
        "interface_added": "✅ Schnittstelle hinzugefügt:",
        "already_exists": "⚠️  Eine Schnittstelle mit ähnlichen Einstellungen existiert bereits.",
        "general_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        ALLGEMEINE EINSTELLUNGEN                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📊 Log-Level (0-7, aktuell: {loglevel})
  [2] 🚀 Transport aktivieren ({transport})
  [3] 🔒 Panic bei nicht behebbarem Fehler ({panic})
  [4] 🔙 Zurück zum Hauptmenü

""",
        "loglevel_help": """
Log-Level:
  0 = Nur kritisch
  1 = Fehler
  2 = Warnungen  
  3 = Hinweise
  4 = Info (Standard)
  5 = Ausführlich
  6 = Debug
  7 = Extremes Debug
""",
        "transport_help": """
Der Transport-Modus ermöglicht deinem Knoten, Verkehr für andere Knoten zu routen.
Aktiviere dies, wenn du dem Netzwerk helfen oder Schnittstellen verbinden möchtest.
""",
        "enter_loglevel": "Gib Log-Level ein (0-7): ",
        "enable_transport": "Transport-Modus aktivieren? (j/n): ",
        "setting_updated": "✅ Einstellung aktualisiert!",
        "view_config": "📋 Aktuelle Konfiguration:",
        "config_location": "📁 Konfigurationsdatei-Speicherort:",
        "check_fix_title": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                   KONFIGURATION PRÜFEN UND REPARIEREN                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "checking_config": "🔍 Prüfe Konfiguration...",
        "config_valid": "✅ Die Konfiguration ist gültig!",
        "config_issues": "⚠️  {count} Problem(e) gefunden:",
        "fix_issues": "🔧 Möchtest du diese Probleme beheben? (j/n): ",
        "fixing_issues": "🔧 Behebe Probleme...",
        "issues_fixed": "✅ Alle Probleme wurden behoben!",
        "issue_section_missing": "Fehlender Abschnitt: [{section}]",
        "issue_key_missing": "Fehlender Schlüssel '{key}' in [{section}]",
        "issue_bad_indentation": "Falsche Einrückung bei Schnittstelle '{name}'",
        "issue_invalid_value": "Ungültiger Wert für '{key}': {value}",
        "issue_duplicate_interface": "Doppelte Schnittstelle: {name}",
        "issue_empty_section": "Leerer [interfaces] Abschnitt",
        "testing_with_rnsd": "🧪 Teste mit rnsd...",
        "rnsd_not_found": "⚠️  rnsd nicht gefunden - Konfiguration kann nicht validiert werden",
        "rnsd_test_passed": "✅ rnsd Validierung bestanden!",
        "rnsd_test_failed": "❌ rnsd Validierung fehlgeschlagen:",
    },
    
    "ru": {
        "lang_name": "Русский",
        "welcome": """
╔══════════════════════════════════════════════════════════════════════════════╗
║              RETICULUM NETWORK STACK - ИНТЕРАКТИВНЫЙ КОНФИГУРАТОР            ║
║                                                                              ║
║  Этот инструмент поможет вам настроить Reticulum интерактивно.              ║
║  Он безопасно отредактирует ваш файл ~/.reticulum/config.                   ║
║                                                                              ║
║  Резервная копия будет создана перед любыми изменениями.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "config_not_found": "⚠️  Конфигурация Reticulum не найдена в:",
        "create_default": "Создать конфигурацию по умолчанию? (д/н): ",
        "creating_default": "📝 Создание конфигурации Reticulum по умолчанию...",
        "run_rnsd_first": "💡 Совет: Запустите 'rnsd' один раз для генерации конфигурации по умолчанию.",
        "config_found": "✅ Найдена конфигурация Reticulum в:",
        "backup_created": "💾 Резервная копия создана:",
        "permission_denied": "❌ Доступ запрещён. Попробуйте с sudo или исправьте права доступа.",
        "main_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              ГЛАВНОЕ МЕНЮ                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Показать текущую конфигурацию
  [2] ⚙️  Редактировать общие настройки (loglevel, transport и т.д.)
  [3] 🌐 Управление интерфейсами
  [4] 📡 Добавить TCP Client интерфейсы (подключиться к сети)
  [5] 🔌 Быстрое подключение - Добавить рекомендуемые публичные узлы
  [6] 🔧 Проверить и исправить конфигурацию
  [7] 💾 Сохранить и выйти
  [8] ❌ Выйти без сохранения

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
        "goodbye": "👋 Спасибо за использование конфигуратора Reticulum!",
        "current_value": "Текущее значение:",
        "new_value": "Новое значение (Enter для сохранения текущего): ",
        "enabled": "включено",
        "disabled": "выключено",
        "interface_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        УПРАВЛЕНИЕ ИНТЕРФЕЙСАМИ                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📋 Список всех интерфейсов
  [2] ✏️  Включить/Выключить интерфейс
  [3] ❌ Удалить интерфейс
  [4] ➕ Добавить новый интерфейс вручную
  [5] 🔙 Вернуться в главное меню

""",
        "no_interfaces": "ℹ️  Интерфейсы не найдены в конфигурации.",
        "interface_list": "📡 Текущие Интерфейсы:",
        "select_interface": "Выберите номер интерфейса: ",
        "interface_enabled": "✅ Интерфейс включён:",
        "interface_disabled": "🔴 Интерфейс выключен:",
        "interface_removed": "🗑️  Интерфейс удалён:",
        "confirm_remove": "⚠️  Удалить этот интерфейс? (д/н): ",
        "tcp_menu": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ДОБАВИТЬ TCP CLIENT ИНТЕРФЕЙС                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 🌍 RMAP.world (Карта Reticulum - рекомендуется)
  [2] 🇮🇪 Dublin Testnet Hub (официальный)
  [3] 🌐 BetweenTheBorders Hub (сообщество)
  [4] 🇦🇺 Sydney RNS (сообщество)
  [5] 🇩🇪 Узел Германия (сообщество)
  [6] ➕ Добавить свой TCP интерфейс
  [7] 📦 Добавить ВСЕ рекомендуемые узлы
  [8] 🔙 Вернуться в главное меню

""",
        "quick_connect": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                      НАСТРОЙКА БЫСТРОГО ПОДКЛЮЧЕНИЯ                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

Это добавит подборку надёжных публичных узлов для быстрого подключения
к сети Reticulum.

Рекомендуемые узлы для добавления:
  • RMAP.world (порт 4242) - Карта сети Reticulum
  • Dublin Testnet Hub (порт 4965) - Официальный тестнет
  • BetweenTheBorders (порт 4242) - Хаб сообщества

""",
        "add_all_confirm": "Добавить все рекомендуемые узлы? (д/н): ",
        "nodes_added": "✅ Узлы успешно добавлены!",
        "interface_name": "Имя интерфейса (например, 'Мой Узел'): ",
        "target_host": "Целевой хост/IP: ",
        "target_port": "Целевой порт (по умолчанию 4242): ",
        "interface_added": "✅ Интерфейс добавлен:",
        "already_exists": "⚠️  Интерфейс с похожими настройками уже существует.",
        "general_settings": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ОБЩИЕ НАСТРОЙКИ                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

  [1] 📊 Уровень логов (0-7, текущий: {loglevel})
  [2] 🚀 Включить transport ({transport})
  [3] 🔒 Panic при неустранимой ошибке ({panic})
  [4] 🔙 Вернуться в главное меню

""",
        "loglevel_help": """
Уровни логов:
  0 = Только критические
  1 = Ошибки
  2 = Предупреждения  
  3 = Уведомления
  4 = Информация (по умолчанию)
  5 = Подробно
  6 = Отладка
  7 = Максимальная отладка
""",
        "transport_help": """
Режим transport позволяет вашему узлу маршрутизировать трафик для других узлов.
Включите, если хотите помочь сети или нужно соединить интерфейсы.
""",
        "enter_loglevel": "Введите уровень логов (0-7): ",
        "enable_transport": "Включить режим transport? (д/н): ",
        "setting_updated": "✅ Настройка обновлена!",
        "view_config": "📋 Текущая Конфигурация:",
        "config_location": "📁 Расположение файла конфигурации:",
        "check_fix_title": """
╔══════════════════════════════════════════════════════════════════════════════╗
║                  ПРОВЕРИТЬ И ИСПРАВИТЬ КОНФИГУРАЦИЮ                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
""",
        "checking_config": "🔍 Проверка конфигурации...",
        "config_valid": "✅ Конфигурация корректна!",
        "config_issues": "⚠️  Найдено {count} проблем(а):",
        "fix_issues": "🔧 Исправить эти проблемы? (д/н): ",
        "fixing_issues": "🔧 Исправление проблем...",
        "issues_fixed": "✅ Все проблемы исправлены!",
        "issue_section_missing": "Отсутствует секция: [{section}]",
        "issue_key_missing": "Отсутствует ключ '{key}' в [{section}]",
        "issue_bad_indentation": "Неправильный отступ в интерфейсе '{name}'",
        "issue_invalid_value": "Недопустимое значение для '{key}': {value}",
        "issue_duplicate_interface": "Дублирующийся интерфейс: {name}",
        "issue_empty_section": "Пустая секция [interfaces]",
        "testing_with_rnsd": "🧪 Тестирование с rnsd...",
        "rnsd_not_found": "⚠️  rnsd не найден - невозможно проверить конфигурацию",
        "rnsd_test_passed": "✅ Проверка rnsd пройдена!",
        "rnsd_test_failed": "❌ Проверка rnsd не пройдена:",
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# PREDEFINED TCP INTERFACES
# ══════════════════════════════════════════════════════════════════════════════

TCP_INTERFACES = {
    "rmap": {
        "name": "RMAP.world",
        "host": "rmap.world",
        "port": "4242",
        "description": "Reticulum Network Map - Community Hub"
    },
    "dublin": {
        "name": "RNS Testnet Dublin",
        "host": "dublin.connect.reticulum.network",
        "port": "4965",
        "description": "Official Dublin Testnet Hub"
    },
    "btb": {
        "name": "RNS Testnet BetweenTheBorders",
        "host": "reticulum.betweentheborders.com",
        "port": "4242",
        "description": "Community Hub - BetweenTheBorders"
    },
    "sydney": {
        "name": "Sydney RNS",
        "host": "sydney.reticulum.au",
        "port": "4242",
        "description": "Community Hub - Sydney Australia"
    },
    "germany": {
        "name": "RNS TCP Node Germany",
        "host": "202.61.243.41",
        "port": "4965",
        "description": "Community Hub - Germany"
    },
}

# Default config template - matches rnsd expected format
DEFAULT_CONFIG = """[reticulum]
enable_transport = False
share_instance = Yes
shared_instance_port = 37428
instance_control_port = 37429
panic_on_interface_error = No

[logging]
loglevel = 4

[interfaces]

  [[Default Interface]]
    type = AutoInterface
    enabled = yes

"""


# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATOR CLASS
# ══════════════════════════════════════════════════════════════════════════════

class ReticulumConfigurator:
    def __init__(self):
        self.lang = "en"
        self.config_path = None
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
        """Find the Reticulum config file"""
        # Check common locations
        possible_paths = [
            Path.home() / ".reticulum" / "config",
            Path("/etc/reticulum/config"),
            Path.home() / ".config" / "reticulum" / "config",
        ]
        
        for path in possible_paths:
            if path.exists():
                self.config_path = path
                return
        
        # Default to standard location
        self.config_path = Path.home() / ".reticulum" / "config"
    
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
            print(f"\n{self.t('run_rnsd_first')}")
            
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
        
        # Create directory if needed
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(self.config_path, 'w') as f:
                f.write(DEFAULT_CONFIG)
            self.config_content = DEFAULT_CONFIG
            self.original_content = DEFAULT_CONFIG
            print(f"✅ Created: {self.config_path}")
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
    
    def parse_interfaces(self):
        """Parse interfaces from config content"""
        interfaces = []
        
        # Find all interface blocks [[name]]
        pattern = r'\[\[([^\]]+)\]\](.*?)(?=\[\[|\[(?!\[)|$)'
        matches = re.findall(pattern, self.config_content, re.DOTALL)
        
        for name, content in matches:
            # Parse interface properties
            iface = {"name": name.strip(), "content": content, "properties": {}}
            
            for line in content.split('\n'):
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    iface["properties"][key.strip()] = value.strip()
            
            interfaces.append(iface)
        
        return interfaces
    
    def get_setting(self, section, key, default=""):
        """Get a setting value from config"""
        # Pattern to find section and key (not interface subsections)
        section_pattern = rf'\[{re.escape(section)}\]\s*\n(.*?)(?=\n\[[^\[]|\Z)'
        section_match = re.search(section_pattern, self.config_content, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(1)
            # Match key with optional leading whitespace
            key_pattern = rf'^\s*{re.escape(key)}\s*=\s*(.+)$'
            key_match = re.search(key_pattern, section_content, re.MULTILINE)
            if key_match:
                return key_match.group(1).strip()
        
        return default
    
    def set_setting(self, section, key, value):
        """Set a setting value in config"""
        # Check if section exists (but not [interfaces] subsections)
        section_pattern = rf'(\[{re.escape(section)}\])(\s*\n)(.*?)(?=\n\[[^\[]|\Z)'
        section_match = re.search(section_pattern, self.config_content, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(3)
            # Match key with optional leading whitespace
            key_pattern = rf'^(\s*)({re.escape(key)}\s*=\s*)(.+)$'
            
            if re.search(key_pattern, section_content, re.MULTILINE):
                # Replace existing key, preserving indentation
                new_section = re.sub(
                    key_pattern,
                    rf'\g<1>\g<2>{value}',
                    section_content,
                    flags=re.MULTILINE
                )
                self.config_content = self.config_content.replace(
                    section_match.group(0),
                    section_match.group(1) + section_match.group(2) + new_section
                )
            else:
                # Add new key to section (no indentation for main sections)
                section_end = section_match.group(0).rstrip()
                new_content = section_end + f"\n{key} = {value}\n"
                self.config_content = self.config_content.replace(
                    section_match.group(0),
                    new_content
                )
        else:
            # Section doesn't exist, add it
            self.config_content = self.config_content.rstrip() + f"\n\n[{section}]\n{key} = {value}\n"
        
        self.has_changes = True
    
    def add_tcp_interface(self, name, host, port):
        """Add a TCP Client Interface to the config"""
        # Check if interface already exists
        if f"target_host = {host}" in self.config_content:
            return False
        
        # Create interface block with proper indentation (2 spaces for [[]], 4 for properties)
        # Using explicit spacing to ensure correct format
        interface_block = "\n  [[" + name + "]]\n"
        interface_block += "    type = TCPClientInterface\n"
        interface_block += "    enabled = yes\n"
        interface_block += "    target_host = " + host + "\n"
        interface_block += "    target_port = " + port + "\n"
        
        # Find [interfaces] section and append properly
        if "[interfaces]" in self.config_content:
            # Find the position after [interfaces] section to insert
            # We need to find where the interfaces section content ends
            interfaces_match = re.search(r'(\[interfaces\].*?)(?=\n\[[^\[]|\Z)', 
                                         self.config_content, re.DOTALL)
            if interfaces_match:
                # Insert at the end of the interfaces section
                insert_pos = interfaces_match.end()
                self.config_content = (
                    self.config_content[:insert_pos].rstrip() + 
                    interface_block + 
                    self.config_content[insert_pos:]
                )
            else:
                # Fallback: append to end
                self.config_content = self.config_content.rstrip() + interface_block
        else:
            # Add interfaces section
            self.config_content = self.config_content.rstrip() + "\n\n[interfaces]" + interface_block
        
        self.has_changes = True
        return True
    
    def remove_interface(self, name):
        """Remove an interface from config"""
        # Pattern to match the entire interface block
        pattern = rf'\s*\[\[{re.escape(name)}\]\].*?(?=\[\[|\[(?!\[)|$)'
        self.config_content = re.sub(pattern, '', self.config_content, flags=re.DOTALL)
        self.has_changes = True
    
    def toggle_interface(self, name, enable):
        """Enable or disable an interface"""
        # Find the interface block and toggle enabled
        pattern = rf'(\[\[{re.escape(name)}\]\].*?)((?:enabled|interface_enabled)\s*=\s*)(yes|no|true|false)'
        
        new_value = "yes" if enable else "no"
        self.config_content = re.sub(
            pattern,
            rf'\g<1>\g<2>{new_value}',
            self.config_content,
            flags=re.DOTALL | re.IGNORECASE
        )
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
    
    def edit_general_settings(self):
        """Edit general Reticulum settings"""
        while True:
            self.clear_screen()
            
            # Get current values
            loglevel = self.get_setting("logging", "loglevel", "4")
            transport = self.get_setting("reticulum", "enable_transport", "False")
            panic = self.get_setting("reticulum", "panic_on_interface_error", "No")
            
            transport_str = self.t("enabled") if transport.lower() in ["true", "yes"] else self.t("disabled")
            panic_str = self.t("enabled") if panic.lower() in ["true", "yes"] else self.t("disabled")
            
            print(self.t("general_settings").format(
                loglevel=loglevel,
                transport=transport_str,
                panic=panic_str
            ))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                print(self.t("loglevel_help"))
                new_level = input(self.t("enter_loglevel")).strip()
                if new_level.isdigit() and 0 <= int(new_level) <= 7:
                    self.set_setting("logging", "loglevel", new_level)
                    print(f"\n{self.t('setting_updated')}")
                    time.sleep(1)
            
            elif choice == "2":
                print(self.t("transport_help"))
                response = input(self.t("enable_transport")).strip().lower()
                new_value = "True" if response == self.t("yes") else "False"
                self.set_setting("reticulum", "enable_transport", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "3":
                current = panic.lower() in ["true", "yes"]
                new_value = "No" if current else "Yes"
                self.set_setting("reticulum", "panic_on_interface_error", new_value)
                print(f"\n{self.t('setting_updated')}")
                time.sleep(1)
            
            elif choice == "4":
                break
    
    def manage_interfaces(self):
        """Interface management menu"""
        while True:
            self.clear_screen()
            print(self.t("interface_menu"))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                self.list_interfaces()
            elif choice == "2":
                self.toggle_interface_menu()
            elif choice == "3":
                self.remove_interface_menu()
            elif choice == "4":
                self.add_custom_interface()
            elif choice == "5":
                break
    
    def list_interfaces(self):
        """List all interfaces"""
        self.clear_screen()
        interfaces = self.parse_interfaces()
        
        if not interfaces:
            print(f"\n{self.t('no_interfaces')}")
        else:
            print(f"\n{self.t('interface_list')}\n")
            for i, iface in enumerate(interfaces, 1):
                enabled = iface["properties"].get("enabled", 
                          iface["properties"].get("interface_enabled", "no"))
                status = "✅" if enabled.lower() in ["yes", "true"] else "🔴"
                iface_type = iface["properties"].get("type", "Unknown")
                
                print(f"  {i}. {status} [{iface['name']}]")
                print(f"      Type: {iface_type}")
                
                if iface_type == "TCPClientInterface":
                    host = iface["properties"].get("target_host", "")
                    port = iface["properties"].get("target_port", "")
                    print(f"      Host: {host}:{port}")
                print()
        
        input(f"\n{self.t('press_enter')}")
    
    def toggle_interface_menu(self):
        """Toggle interface enabled/disabled"""
        self.clear_screen()
        interfaces = self.parse_interfaces()
        
        if not interfaces:
            print(f"\n{self.t('no_interfaces')}")
            input(f"\n{self.t('press_enter')}")
            return
        
        print(f"\n{self.t('interface_list')}\n")
        for i, iface in enumerate(interfaces, 1):
            enabled = iface["properties"].get("enabled",
                      iface["properties"].get("interface_enabled", "no"))
            status = "✅" if enabled.lower() in ["yes", "true"] else "🔴"
            print(f"  {i}. {status} {iface['name']}")
        
        try:
            choice = input(f"\n{self.t('select_interface')}").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                iface = interfaces[idx]
                enabled = iface["properties"].get("enabled",
                          iface["properties"].get("interface_enabled", "no"))
                is_enabled = enabled.lower() in ["yes", "true"]
                
                self.toggle_interface(iface["name"], not is_enabled)
                
                if is_enabled:
                    print(f"\n{self.t('interface_disabled')} {iface['name']}")
                else:
                    print(f"\n{self.t('interface_enabled')} {iface['name']}")
                time.sleep(1)
        except (ValueError, IndexError):
            print(f"\n{self.t('invalid_choice')}")
            time.sleep(1)
    
    def remove_interface_menu(self):
        """Remove an interface"""
        self.clear_screen()
        interfaces = self.parse_interfaces()
        
        if not interfaces:
            print(f"\n{self.t('no_interfaces')}")
            input(f"\n{self.t('press_enter')}")
            return
        
        print(f"\n{self.t('interface_list')}\n")
        for i, iface in enumerate(interfaces, 1):
            print(f"  {i}. {iface['name']}")
        
        try:
            choice = input(f"\n{self.t('select_interface')}").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                iface = interfaces[idx]
                confirm = input(f"\n{self.t('confirm_remove')}").strip().lower()
                if confirm == self.t("yes"):
                    self.remove_interface(iface["name"])
                    print(f"\n{self.t('interface_removed')} {iface['name']}")
                    time.sleep(1)
        except (ValueError, IndexError):
            print(f"\n{self.t('invalid_choice')}")
            time.sleep(1)
    
    def add_custom_interface(self):
        """Add a custom TCP interface"""
        self.clear_screen()
        print("\n➕ Add Custom TCP Interface\n")
        
        name = input(self.t("interface_name")).strip()
        if not name:
            return
        
        host = input(self.t("target_host")).strip()
        if not host:
            return
        
        port = input(self.t("target_port")).strip()
        if not port:
            port = "4242"
        
        if self.add_tcp_interface(name, host, port):
            print(f"\n{self.t('interface_added')} {name}")
        else:
            print(f"\n{self.t('already_exists')}")
        
        time.sleep(1)
    
    def add_tcp_interface_menu(self):
        """Add TCP Client interfaces menu"""
        while True:
            self.clear_screen()
            print(self.t("tcp_menu"))
            
            choice = input(self.t("enter_choice")).strip()
            
            if choice == "1":
                iface = TCP_INTERFACES["rmap"]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"\n{self.t('interface_added')} {iface['name']}")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "2":
                iface = TCP_INTERFACES["dublin"]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"\n{self.t('interface_added')} {iface['name']}")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "3":
                iface = TCP_INTERFACES["btb"]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"\n{self.t('interface_added')} {iface['name']}")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "4":
                iface = TCP_INTERFACES["sydney"]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"\n{self.t('interface_added')} {iface['name']}")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "5":
                iface = TCP_INTERFACES["germany"]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"\n{self.t('interface_added')} {iface['name']}")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "6":
                self.add_custom_interface()
            
            elif choice == "7":
                # Add all recommended interfaces
                added = 0
                for key in ["rmap", "dublin", "btb"]:
                    iface = TCP_INTERFACES[key]
                    if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                        added += 1
                
                if added > 0:
                    print(f"\n{self.t('nodes_added')} ({added} nodes)")
                else:
                    print(f"\n{self.t('already_exists')}")
                time.sleep(1)
            
            elif choice == "8":
                break
    
    def quick_connect(self):
        """Quick connect - add recommended nodes"""
        self.clear_screen()
        print(self.t("quick_connect"))
        
        confirm = input(self.t("add_all_confirm")).strip().lower()
        if confirm == self.t("yes"):
            added = 0
            for key in ["rmap", "dublin", "btb"]:
                iface = TCP_INTERFACES[key]
                if self.add_tcp_interface(iface["name"], iface["host"], iface["port"]):
                    print(f"  ✅ Added: {iface['name']}")
                    added += 1
                else:
                    print(f"  ℹ️  Skipped (exists): {iface['name']}")
            
            if added > 0:
                print(f"\n{self.t('nodes_added')}")
            time.sleep(2)
    
    def check_and_fix_config(self):
        """Check configuration for issues and optionally fix them"""
        self.clear_screen()
        print(self.t("check_fix_title"))
        print(f"{self.t('checking_config')}\n")
        
        issues = []
        fixes = []
        
        # FIRST: Test with rnsd if available (most reliable check)
        rnsd_ok, rnsd_error = self.test_with_rnsd_silent()
        
        if rnsd_ok:
            print(f"  {self.t('rnsd_test_passed')}")
            print(f"\n{self.t('config_valid')}")
            input(f"\n{self.t('press_enter')}")
            return
        elif rnsd_error:
            print(f"  {self.t('rnsd_test_failed')}")
            print(f"    {rnsd_error}\n")
        
        # Check 1: Required sections exist
        required_sections = ["reticulum", "logging", "interfaces"]
        for section in required_sections:
            # Use regex to avoid false matches like [[interfaces]]
            if not re.search(rf'^\[{section}\]\s*$', self.config_content, re.MULTILINE):
                issues.append(self.t("issue_section_missing").format(section=section))
                if section == "reticulum":
                    fixes.append(("add_section", section, "enable_transport = No\nshare_instance = Yes"))
                elif section == "logging":
                    fixes.append(("add_section", section, "loglevel = 4"))
                elif section == "interfaces":
                    fixes.append(("add_section", section, "\n  [[Default Interface]]\n    type = AutoInterface\n    enabled = yes"))
        
        # Check 2: Interface indentation (2 spaces for [[]], 4 for properties)
        interfaces_section = re.search(r'\[interfaces\]\s*\n(.*?)(?=\n\[[a-z]|\Z)', self.config_content, re.DOTALL | re.IGNORECASE)
        
        if interfaces_section:
            section_content = interfaces_section.group(1)
            lines = section_content.split('\n')
            
            current_interface = None
            bad_interfaces = set()
            
            for i, line in enumerate(lines):
                # Skip empty lines and comments
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                
                # Check for interface header
                iface_match = re.match(r'^(\s*)\[\[([^\]]+)\]\]', line)
                if iface_match:
                    indent = len(iface_match.group(1))
                    current_interface = iface_match.group(2)
                    if indent != 2:
                        bad_interfaces.add(current_interface)
                    continue
                
                # Check for property indentation (only if we're inside an interface)
                prop_match = re.match(r'^(\s*)(\w+)\s*=', line)
                if prop_match and current_interface:
                    indent = len(prop_match.group(1))
                    if indent != 4:
                        bad_interfaces.add(current_interface)
            
            for iface in bad_interfaces:
                issues.append(self.t("issue_bad_indentation").format(name=iface))
                fixes.append(("fix_indentation", iface))
        
        # Check 3: Empty interfaces section
        if interfaces_section:
            section_content = interfaces_section.group(1).strip()
            # Remove comments
            non_comment_lines = [l for l in section_content.split('\n') if l.strip() and not l.strip().startswith('#')]
            if not non_comment_lines or "[[" not in section_content:
                issues.append(self.t("issue_empty_section"))
                fixes.append(("add_default_interface", ))
        
        # Check 4: Duplicate interfaces
        if interfaces_section:
            interface_names = re.findall(r'\[\[([^\]]+)\]\]', interfaces_section.group(1))
            seen = set()
            for name in interface_names:
                if name in seen:
                    issues.append(self.t("issue_duplicate_interface").format(name=name))
                    fixes.append(("remove_duplicate", name))
                seen.add(name)
        
        # Display results
        if not issues:
            if rnsd_error:
                # rnsd failed but we couldn't detect the issue
                print(f"\n  ⚠️  Could not automatically detect the issue.")
                print(f"  Please check the config file manually for syntax errors.")
                print(f"\n  Common issues:")
                print(f"    • Incorrect indentation (use 2 spaces for [[Interface]], 4 for properties)")
                print(f"    • Missing or extra brackets")
                print(f"    • Invalid parameter names or values")
                print(f"    • Tabs instead of spaces")
                
                # Offer to rebuild config
                print(f"\n  Would you like to rebuild the config from scratch?")
                response = input(f"  This will reset to defaults but preserve interfaces (y/n): ").strip().lower()
                if response == self.t("yes"):
                    self.rebuild_config()
            else:
                print(f"\n{self.t('config_valid')}")
        else:
            print(f"\n{self.t('config_issues').format(count=len(issues))}\n")
            for i, issue in enumerate(issues, 1):
                print(f"  {i}. {issue}")
            
            # Ask if user wants to fix
            print()
            response = input(self.t("fix_issues")).strip().lower()
            
            if response == self.t("yes"):
                print(f"\n{self.t('fixing_issues')}\n")
                self.apply_fixes(fixes)
                print(f"\n{self.t('issues_fixed')}")
                
                # Test again
                rnsd_ok, rnsd_error = self.test_with_rnsd_silent()
                if rnsd_ok:
                    print(f"\n  {self.t('rnsd_test_passed')}")
                elif rnsd_error:
                    print(f"\n  {self.t('rnsd_test_failed')}")
                    print(f"    {rnsd_error}")
        
        input(f"\n{self.t('press_enter')}")
    
    def rebuild_config(self):
        """Rebuild config from scratch, preserving interface definitions"""
        print(f"\n  🔧 Rebuilding configuration...")
        
        # Extract existing interfaces
        interfaces_section = re.search(r'\[interfaces\]\s*\n(.*?)(?=\n\[[a-z]|\Z)', 
                                       self.config_content, re.DOTALL | re.IGNORECASE)
        
        interfaces_content = ""
        if interfaces_section:
            # Parse and rebuild interfaces with correct indentation
            section = interfaces_section.group(1)
            current_iface = None
            current_props = []
            interfaces = []
            
            for line in section.split('\n'):
                stripped = line.strip()
                
                # Skip empty lines and comments
                if not stripped or stripped.startswith('#'):
                    continue
                
                # Interface header
                iface_match = re.match(r'\[\[([^\]]+)\]\]', stripped)
                if iface_match:
                    # Save previous interface
                    if current_iface:
                        interfaces.append((current_iface, current_props))
                    current_iface = iface_match.group(1)
                    current_props = []
                    continue
                
                # Property
                prop_match = re.match(r'(\w+)\s*=\s*(.+)', stripped)
                if prop_match and current_iface:
                    current_props.append((prop_match.group(1), prop_match.group(2)))
            
            # Don't forget last interface
            if current_iface:
                interfaces.append((current_iface, current_props))
            
            # Rebuild with correct indentation
            for iface_name, props in interfaces:
                interfaces_content += f"\n  [[{iface_name}]]\n"
                for key, value in props:
                    interfaces_content += f"    {key} = {value}\n"
        
        # If no interfaces found, add default
        if not interfaces_content.strip():
            interfaces_content = """
  [[Default Interface]]
    type = AutoInterface
    enabled = yes
"""
        
        # Build new config
        self.config_content = f"""[reticulum]
enable_transport = No
share_instance = Yes

[logging]
loglevel = 4

[interfaces]
{interfaces_content}"""
        
        self.has_changes = True
        print(f"  ✅ Configuration rebuilt successfully!")
        print(f"  Please save and test with rnsd.")
    
    def test_with_rnsd_silent(self):
        """Test the config with rnsd silently, return (success, error_message)"""
        # Check if rnsd is available
        try:
            result = subprocess.run(
                ["which", "rnsd"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return None, None  # rnsd not available
        except Exception:
            return None, None
        
        # Save current config temporarily if there are unsaved changes
        config_saved = False
        original_on_disk = None
        
        if self.config_content != self.original_content:
            try:
                # Read current on-disk content
                if self.config_path.exists():
                    with open(self.config_path, 'r') as f:
                        original_on_disk = f.read()
                
                # Save current content
                with open(self.config_path, 'w') as f:
                    f.write(self.config_content)
                config_saved = True
            except Exception as e:
                return None, f"Could not save for testing: {e}"
        
        # Test by running rnsd briefly
        try:
            result = subprocess.run(
                ["rnsd", "--config", str(self.config_path.parent)],
                capture_output=True,
                text=True,
                timeout=3
            )
            
            # Check for config errors in stderr
            combined = result.stdout + result.stderr
            if "Could not parse" in combined or "Error" in combined:
                error_lines = [l for l in combined.split('\n') if 'Error' in l or 'Could not parse' in l]
                error_msg = error_lines[0] if error_lines else "Unknown parsing error"
                
                # Restore original if we modified it
                if config_saved and original_on_disk is not None:
                    with open(self.config_path, 'w') as f:
                        f.write(original_on_disk)
                
                return False, error_msg
            
            return True, None
                
        except subprocess.TimeoutExpired:
            # If it runs for 3 seconds without error, config is probably fine
            return True, None
        except Exception as e:
            return None, f"Test error: {e}"
        finally:
            # Restore original if we modified it
            if config_saved and original_on_disk is not None:
                try:
                    with open(self.config_path, 'w') as f:
                        f.write(original_on_disk)
                except:
                    pass
    
    def apply_fixes(self, fixes):
        """Apply the list of fixes to the config"""
        for fix in fixes:
            fix_type = fix[0]
            
            if fix_type == "add_section":
                section = fix[1]
                content = fix[2]
                self.config_content = self.config_content.rstrip() + f"\n\n[{section}]\n{content}\n"
                print(f"  ✅ Added [{section}] section")
                self.has_changes = True
            
            elif fix_type == "add_key":
                section = fix[1]
                key = fix[2]
                value = fix[3]
                self.set_setting(section, key, value)
                print(f"  ✅ Added {key} = {value} to [{section}]")
            
            elif fix_type == "fix_indentation":
                iface_name = fix[1]
                self.fix_interface_indentation(iface_name)
                print(f"  ✅ Fixed indentation for [[{iface_name}]]")
            
            elif fix_type == "add_default_interface":
                interface_block = "\n  [[Default Interface]]\n"
                interface_block += "    type = AutoInterface\n"
                interface_block += "    enabled = yes\n"
                
                # Add after [interfaces]
                self.config_content = re.sub(
                    r'(\[interfaces\])\s*\n',
                    r'\1' + interface_block,
                    self.config_content
                )
                print(f"  ✅ Added default AutoInterface")
                self.has_changes = True
            
            elif fix_type == "remove_duplicate":
                # Remove second occurrence of interface
                iface_name = fix[1]
                pattern = rf'(\[\[{re.escape(iface_name)}\]\].*?)(\[\[{re.escape(iface_name)}\]\].*?)(?=\[\[|\[(?!\[)|$)'
                self.config_content = re.sub(pattern, r'\1', self.config_content, flags=re.DOTALL)
                print(f"  ✅ Removed duplicate [[{iface_name}]]")
                self.has_changes = True
    
    def fix_interface_indentation(self, iface_name):
        """Fix indentation for a specific interface"""
        # Find the interface block
        pattern = rf'(\s*)\[\[{re.escape(iface_name)}\]\](.*?)(?=\[\[|\[(?!\[)|$)'
        match = re.search(pattern, self.config_content, re.DOTALL)
        
        if match:
            block = match.group(0)
            lines = block.split('\n')
            fixed_lines = []
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('[[') and stripped.endswith(']]'):
                    # Interface header - 2 spaces
                    fixed_lines.append('  ' + stripped)
                elif '=' in stripped and stripped:
                    # Property - 4 spaces
                    fixed_lines.append('    ' + stripped)
                elif stripped:
                    # Other content - 4 spaces
                    fixed_lines.append('    ' + stripped)
                else:
                    # Empty line
                    fixed_lines.append('')
            
            fixed_block = '\n'.join(fixed_lines)
            self.config_content = self.config_content.replace(block, fixed_block)
            self.has_changes = True
    
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
                self.edit_general_settings()
            elif choice == "3":
                self.manage_interfaces()
            elif choice == "4":
                self.add_tcp_interface_menu()
            elif choice == "5":
                self.quick_connect()
            elif choice == "6":
                self.check_and_fix_config()
            elif choice == "7":
                self.save_config()
                print(f"\n{self.t('goodbye')}")
                break
            elif choice == "8":
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
    
    configurator = ReticulumConfigurator()
    configurator.run()


if __name__ == "__main__":
    main()
