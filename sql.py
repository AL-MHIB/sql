#!/usr/bin/env python3
"""
SQLMap GUI Tool - Professional SQL Injection Testing Interface
Advanced graphical interface for SQLMap commands with modern dark theme
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, simpledialog
import subprocess
import threading
import json
import os
import sys
from datetime import datetime

class SQLMapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 SQLMap Professional - Advanced SQL Injection Scanner")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        self.root.minsize(1200, 800)
        
        # Variables
        self.current_command = ""
        self.is_running = False
        self.output_buffer = ""
        
        # Professional color scheme
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3a3a3a',
            'accent_blue': '#00d4ff',
            'accent_green': '#00ff88',
            'accent_red': '#ff4757',
            'accent_orange': '#ffa502',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'border': '#404040',
            'success': '#2ed573',
            'warning': '#ffa502',
            'error': '#ff4757'
        }
        
        # Style configuration
        self.setup_styles()
        
        # Create main interface
        self.create_interface()
        
        # Load presets
        self.load_presets()
    
    def setup_styles(self):
        """Configure professional GUI styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Professional dark theme configuration
        style.configure('TNotebook', 
                       background=self.colors['bg_primary'], 
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('TNotebook.Tab', 
                       background=self.colors['bg_secondary'], 
                       foreground=self.colors['text_primary'],
                       padding=[25, 12],
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('TNotebook.Tab', 
                 background=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['bg_tertiary'])])
        
        style.configure('TFrame', 
                       background=self.colors['bg_primary'])
        
        style.configure('TLabel', 
                       background=self.colors['bg_primary'], 
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9))
        
        style.configure('TButton', 
                       background=self.colors['accent_blue'], 
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9, 'bold'),
                       padding=[15, 8])
        
        style.map('TButton', 
                 background=[('active', self.colors['accent_green']),
                           ('pressed', self.colors['accent_orange'])])
        
        # Special button styles
        style.configure('Scan.TButton',
                       background=self.colors['accent_green'],
                       font=('Segoe UI', 10, 'bold'),
                       padding=[20, 10])
        
        style.map('Scan.TButton',
                 background=[('active', self.colors['success']),
                           ('pressed', self.colors['accent_orange'])])
        
        style.configure('Stop.TButton',
                       background=self.colors['accent_red'],
                       font=('Segoe UI', 9, 'bold'))
        
        style.map('Stop.TButton',
                 background=[('active', self.colors['error']),
                           ('pressed', self.colors['accent_orange'])])
        
        # Entry styles
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       bordercolor=self.colors['border'],
                       font=('Consolas', 9))
        
        # Combobox styles
        style.configure('TCombobox',
                       fieldbackground=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_secondary'])
    
    def create_interface(self):
        """Create the main GUI interface"""
        # Header frame with title and main scan button
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        # Title and description
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = tk.Label(title_frame, 
                              text="🔒 SQLMap Professional Scanner", 
                              font=('Segoe UI', 16, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent_blue'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Advanced SQL Injection Testing & Database Security Assessment",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(anchor=tk.W)
        
        # Main scan button in header
        self.main_scan_button = ttk.Button(header_frame, 
                                          text="🚀 START SCAN", 
                                          style='Scan.TButton',
                                          command=self.quick_scan)
        self.main_scan_button.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_basic_tab()
        self.create_advanced_tab()
        self.create_enumeration_tab()
        self.create_bruteforce_tab()
        self.create_techniques_tab()
        self.create_output_tab()
        self.create_presets_tab()
        
        # Status bar
        self.create_status_bar()
    
    def create_basic_tab(self):
        """Create basic SQLMap options tab"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="🎯 Basic Options")
        
        # Create scrollable frame
        canvas = tk.Canvas(basic_frame, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Target URL
        ttk.Label(scrollable_frame, text="🎯 Target URL:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=10, pady=(15, 5))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(scrollable_frame, textvariable=self.url_var, width=70, font=('Consolas', 9))
        url_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(15, 5))
        
        # Request data
        ttk.Label(scrollable_frame, text="📤 POST Data:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.data_var = tk.StringVar()
        data_entry = ttk.Entry(scrollable_frame, textvariable=self.data_var, width=70, font=('Consolas', 9))
        data_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # Cookie
        ttk.Label(scrollable_frame, text="🍪 Cookie:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.cookie_var = tk.StringVar()
        cookie_entry = ttk.Entry(scrollable_frame, textvariable=self.cookie_var, width=70, font=('Consolas', 9))
        cookie_entry.grid(row=2, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # User-Agent
        ttk.Label(scrollable_frame, text="🌐 User-Agent:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.user_agent_var = tk.StringVar()
        user_agent_entry = ttk.Entry(scrollable_frame, textvariable=self.user_agent_var, width=70, font=('Consolas', 9))
        user_agent_entry.grid(row=3, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # Referer
        ttk.Label(scrollable_frame, text="🔗 Referer:", font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.referer_var = tk.StringVar()
        referer_entry = ttk.Entry(scrollable_frame, textvariable=self.referer_var, width=70, font=('Consolas', 9))
        referer_entry.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # Headers
        ttk.Label(scrollable_frame, text="📋 Custom Headers:", font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.headers_var = tk.StringVar()
        headers_entry = ttk.Entry(scrollable_frame, textvariable=self.headers_var, width=70, font=('Consolas', 9))
        headers_entry.grid(row=5, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # Proxy
        ttk.Label(scrollable_frame, text="🔒 Proxy:", font=('Segoe UI', 10, 'bold')).grid(row=6, column=0, sticky=tk.W, padx=10, pady=(10, 5))
        self.proxy_var = tk.StringVar()
        proxy_entry = ttk.Entry(scrollable_frame, textvariable=self.proxy_var, width=70, font=('Consolas', 9))
        proxy_entry.grid(row=6, column=1, columnspan=2, sticky=tk.EW, padx=10, pady=(10, 5))
        
        # Options frame
        options_frame = ttk.LabelFrame(scrollable_frame, text="⚙️ Advanced Options", padding=15)
        options_frame.grid(row=7, column=0, columnspan=3, sticky=tk.EW, padx=10, pady=(20, 10))
        
        # Tor
        self.tor_var = tk.BooleanVar()
        tor_check = ttk.Checkbutton(options_frame, text="🌐 Use Tor Network", variable=self.tor_var)
        tor_check.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        # Random Agent
        self.random_agent_var = tk.BooleanVar()
        random_agent_check = ttk.Checkbutton(options_frame, text="🎲 Random User-Agent", variable=self.random_agent_var)
        random_agent_check.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configure grid weights
        scrollable_frame.columnconfigure(1, weight=1)
        basic_frame.columnconfigure(0, weight=1)
    
    def create_advanced_tab(self):
        """Create advanced SQLMap options tab"""
        advanced_frame = ttk.Frame(self.notebook)
        self.notebook.add(advanced_frame, text="⚡ Advanced Options")
        
        # Risk level
        ttk.Label(advanced_frame, text="Risk Level:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.risk_var = tk.StringVar(value="1")
        risk_combo = ttk.Combobox(advanced_frame, textvariable=self.risk_var, values=["1", "2", "3"], width=10)
        risk_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Level
        ttk.Label(advanced_frame, text="Level:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.level_var = tk.StringVar(value="1")
        level_combo = ttk.Combobox(advanced_frame, textvariable=self.level_var, values=["1", "2", "3", "4", "5"], width=10)
        level_combo.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Threads
        ttk.Label(advanced_frame, text="Threads:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.threads_var = tk.StringVar(value="1")
        threads_entry = ttk.Entry(advanced_frame, textvariable=self.threads_var, width=10)
        threads_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Timeout
        ttk.Label(advanced_frame, text="Timeout:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.timeout_var = tk.StringVar(value="30")
        timeout_entry = ttk.Entry(advanced_frame, textvariable=self.timeout_var, width=10)
        timeout_entry.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Retries
        ttk.Label(advanced_frame, text="Retries:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.retries_var = tk.StringVar(value="3")
        retries_entry = ttk.Entry(advanced_frame, textvariable=self.retries_var, width=10)
        retries_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Delay
        ttk.Label(advanced_frame, text="Delay:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
        self.delay_var = tk.StringVar(value="0")
        delay_entry = ttk.Entry(advanced_frame, textvariable=self.delay_var, width=10)
        delay_entry.grid(row=2, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Batch mode
        self.batch_var = tk.BooleanVar()
        ttk.Checkbutton(advanced_frame, text="Batch Mode (No questions)", variable=self.batch_var).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Verbose
        self.verbose_var = tk.BooleanVar()
        ttk.Checkbutton(advanced_frame, text="Verbose Output", variable=self.verbose_var).grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=5, pady=5)
        
        # Output directory
        ttk.Label(advanced_frame, text="Output Directory:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.output_dir_var = tk.StringVar()
        output_entry = ttk.Entry(advanced_frame, textvariable=self.output_dir_var, width=40)
        output_entry.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(advanced_frame, text="Browse", command=self.browse_output_dir).grid(row=4, column=3, padx=5, pady=5)
        
        # Configure grid weights
        advanced_frame.columnconfigure(1, weight=1)
    
    def create_enumeration_tab(self):
        """Create enumeration options tab"""
        enum_frame = ttk.Frame(self.notebook)
        self.notebook.add(enum_frame, text="🔍 Enumeration")
        
        # Database enumeration
        ttk.Label(enum_frame, text="Database Enumeration:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.enum_dbs_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Enumerate Databases", variable=self.enum_dbs_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.enum_tables_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Enumerate Tables", variable=self.enum_tables_var).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.enum_columns_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Enumerate Columns", variable=self.enum_columns_var).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.enum_schema_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Enumerate Schema", variable=self.enum_schema_var).grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Specific database/table
        ttk.Label(enum_frame, text="Specific Database:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.database_var = tk.StringVar()
        database_entry = ttk.Entry(enum_frame, textvariable=self.database_var, width=30)
        database_entry.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Label(enum_frame, text="Specific Table:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.table_var = tk.StringVar()
        table_entry = ttk.Entry(enum_frame, textvariable=self.table_var, width=30)
        table_entry.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Dump options
        ttk.Label(enum_frame, text="Dump Options:").grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.dump_all_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Dump All", variable=self.dump_all_var).grid(row=8, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.dump_table_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Dump Table", variable=self.dump_table_var).grid(row=9, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.dump_columns_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Dump Columns", variable=self.dump_columns_var).grid(row=10, column=0, sticky=tk.W, padx=5, pady=2)
        
        # Count
        self.count_var = tk.BooleanVar()
        ttk.Checkbutton(enum_frame, text="Count Entries", variable=self.count_var).grid(row=11, column=0, sticky=tk.W, padx=5, pady=2)
    
    def create_bruteforce_tab(self):
        """Create bruteforce options tab"""
        brute_frame = ttk.Frame(self.notebook)
        self.notebook.add(brute_frame, text="💥 Bruteforce")
        
        # Common table names
        self.common_tables_var = tk.BooleanVar()
        ttk.Checkbutton(brute_frame, text="Common Table Names", variable=self.common_tables_var).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Common column names
        self.common_columns_var = tk.BooleanVar()
        ttk.Checkbutton(brute_frame, text="Common Column Names", variable=self.common_columns_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Custom wordlist
        ttk.Label(brute_frame, text="Custom Wordlist:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.wordlist_var = tk.StringVar()
        wordlist_entry = ttk.Entry(brute_frame, textvariable=self.wordlist_var, width=50)
        wordlist_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        ttk.Button(brute_frame, text="Browse", command=self.browse_wordlist).grid(row=2, column=2, padx=5, pady=5)
        
        # Configure grid weights
        brute_frame.columnconfigure(1, weight=1)
    
    def create_techniques_tab(self):
        """Create SQL injection techniques tab"""
        tech_frame = ttk.Frame(self.notebook)
        self.notebook.add(tech_frame, text="🎯 Techniques")
        
        # Injection techniques
        ttk.Label(tech_frame, text="Injection Techniques:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.tech_boolean_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="Boolean-based blind", variable=self.tech_boolean_var).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.tech_error_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="Error-based", variable=self.tech_error_var).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.tech_union_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="UNION query-based", variable=self.tech_union_var).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.tech_stacked_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="Stacked queries", variable=self.tech_stacked_var).grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.tech_time_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="Time-based blind", variable=self.tech_time_var).grid(row=5, column=0, sticky=tk.W, padx=5, pady=2)
        
        self.tech_inline_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="Inline queries", variable=self.tech_inline_var).grid(row=6, column=0, sticky=tk.W, padx=5, pady=2)
        
        # OS detection
        self.os_detect_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="OS Detection", variable=self.os_detect_var).grid(row=7, column=0, sticky=tk.W, padx=5, pady=5)
        
        # DBMS detection
        self.dbms_detect_var = tk.BooleanVar()
        ttk.Checkbutton(tech_frame, text="DBMS Detection", variable=self.dbms_detect_var).grid(row=8, column=0, sticky=tk.W, padx=5, pady=2)
    
    def create_output_tab(self):
        """Create output display tab"""
        output_frame = ttk.Frame(self.notebook)
        self.notebook.add(output_frame, text="📊 Output & Results")
        
        # Command display
        ttk.Label(output_frame, text="Generated Command:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.command_text = scrolledtext.ScrolledText(output_frame, height=8, width=80, 
                                                     bg=self.colors['bg_secondary'], 
                                                     fg=self.colors['text_primary'], 
                                                     insertbackground=self.colors['accent_blue'],
                                                     font=('Consolas', 9))
        self.command_text.grid(row=1, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        # Output display
        ttk.Label(output_frame, text="📊 SQLMap Output:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, width=80, 
                                                    bg=self.colors['bg_secondary'], 
                                                    fg=self.colors['text_primary'], 
                                                    insertbackground=self.colors['accent_blue'],
                                                    font=('Consolas', 9))
        self.output_text.grid(row=3, column=0, columnspan=3, sticky=tk.EW, padx=5, pady=5)
        
        # Control buttons
        button_frame = ttk.Frame(output_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="🔧 Generate Command", command=self.generate_command).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🚀 Execute SQLMap", command=self.execute_sqlmap, style='Scan.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="⏹️ Stop", command=self.stop_execution, style='Stop.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Clear Output", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save Output", command=self.save_output).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        output_frame.columnconfigure(0, weight=1)
    
    def create_presets_tab(self):
        """Create presets tab"""
        preset_frame = ttk.Frame(self.notebook)
        self.notebook.add(preset_frame, text="⚙️ Presets")
        
        # Preset list
        ttk.Label(preset_frame, text="⚙️ Available Presets:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.preset_listbox = tk.Listbox(preset_frame, height=15, 
                                        bg=self.colors['bg_secondary'], 
                                        fg=self.colors['text_primary'], 
                                        selectbackground=self.colors['accent_blue'],
                                        font=('Segoe UI', 9),
                                        relief=tk.FLAT,
                                        borderwidth=0)
        self.preset_listbox.grid(row=1, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        # Preset buttons
        preset_button_frame = ttk.Frame(preset_frame)
        preset_button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(preset_button_frame, text="📥 Load Preset", command=self.load_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_button_frame, text="💾 Save Current as Preset", command=self.save_preset).pack(side=tk.LEFT, padx=5)
        ttk.Button(preset_button_frame, text="🗑️ Delete Preset", command=self.delete_preset).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        preset_frame.columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create professional status bar"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="🟢 Ready - Enter target URL to begin scanning")
        status_label = tk.Label(status_frame, 
                               textvariable=self.status_var, 
                               bg=self.colors['bg_secondary'],
                               fg=self.colors['text_primary'],
                               font=('Segoe UI', 9),
                               relief=tk.FLAT,
                               anchor=tk.W,
                               padx=10,
                               pady=5)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Progress indicator
        self.progress_var = tk.StringVar(value="")
        progress_label = tk.Label(status_frame,
                                 textvariable=self.progress_var,
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['accent_blue'],
                                 font=('Segoe UI', 9, 'bold'),
                                 padx=10,
                                 pady=5)
        progress_label.pack(side=tk.RIGHT)
    
    def quick_scan(self):
        """Quick scan with basic settings"""
        if not self.url_var.get():
            messagebox.showerror("Error", "Please enter a target URL first")
            return
        
        # Set basic scan parameters
        self.risk_var.set("2")
        self.level_var.set("3")
        self.batch_var.set(True)
        self.verbose_var.set(True)
        self.random_agent_var.set(True)
        
        # Generate and execute command
        self.generate_command()
        self.execute_sqlmap()
        
        # Update status
        self.status_var.set("🟡 Quick scan initiated...")
        self.progress_var.set("⏳ Scanning...")
    
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def browse_wordlist(self):
        """Browse for wordlist file"""
        filename = filedialog.askopenfilename(
            title="Select Wordlist File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.wordlist_var.set(filename)
    
    def generate_command(self):
        """Generate SQLMap command based on current settings"""
        command_parts = ["sqlmap"]
        
        # Basic options
        if self.url_var.get():
            command_parts.append(f"-u \"{self.url_var.get()}\"")
        
        if self.data_var.get():
            command_parts.append(f"--data=\"{self.data_var.get()}\"")
        
        if self.cookie_var.get():
            command_parts.append(f"--cookie=\"{self.cookie_var.get()}\"")
        
        if self.user_agent_var.get():
            command_parts.append(f"--user-agent=\"{self.user_agent_var.get()}\"")
        
        if self.referer_var.get():
            command_parts.append(f"--referer=\"{self.referer_var.get()}\"")
        
        if self.headers_var.get():
            command_parts.append(f"--headers=\"{self.headers_var.get()}\"")
        
        if self.proxy_var.get():
            command_parts.append(f"--proxy=\"{self.proxy_var.get()}\"")
        
        # Advanced options
        if self.risk_var.get() != "1":
            command_parts.append(f"--risk={self.risk_var.get()}")
        
        if self.level_var.get() != "1":
            command_parts.append(f"--level={self.level_var.get()}")
        
        if self.threads_var.get() != "1":
            command_parts.append(f"--threads={self.threads_var.get()}")
        
        if self.timeout_var.get() != "30":
            command_parts.append(f"--timeout={self.timeout_var.get()}")
        
        if self.retries_var.get() != "3":
            command_parts.append(f"--retries={self.retries_var.get()}")
        
        if self.delay_var.get() != "0":
            command_parts.append(f"--delay={self.delay_var.get()}")
        
        # Boolean options
        if self.tor_var.get():
            command_parts.append("--tor")
        
        if self.random_agent_var.get():
            command_parts.append("--random-agent")
        
        if self.batch_var.get():
            command_parts.append("--batch")
        
        if self.verbose_var.get():
            command_parts.append("-v")
        
        # Enumeration options
        if self.enum_dbs_var.get():
            command_parts.append("--dbs")
        
        if self.enum_tables_var.get():
            command_parts.append("--tables")
        
        if self.enum_columns_var.get():
            command_parts.append("--columns")
        
        if self.enum_schema_var.get():
            command_parts.append("--schema")
        
        if self.database_var.get():
            command_parts.append(f"-D \"{self.database_var.get()}\"")
        
        if self.table_var.get():
            command_parts.append(f"-T \"{self.table_var.get()}\"")
        
        if self.dump_all_var.get():
            command_parts.append("--dump-all")
        
        if self.dump_table_var.get():
            command_parts.append("--dump")
        
        if self.dump_columns_var.get():
            command_parts.append("--dump-columns")
        
        if self.count_var.get():
            command_parts.append("--count")
        
        # Bruteforce options
        if self.common_tables_var.get():
            command_parts.append("--common-tables")
        
        if self.common_columns_var.get():
            command_parts.append("--common-columns")
        
        if self.wordlist_var.get():
            command_parts.append(f"--wordlist=\"{self.wordlist_var.get()}\"")
        
        # Technique options
        techniques = []
        if self.tech_boolean_var.get():
            techniques.append("B")
        if self.tech_error_var.get():
            techniques.append("E")
        if self.tech_union_var.get():
            techniques.append("U")
        if self.tech_stacked_var.get():
            techniques.append("S")
        if self.tech_time_var.get():
            techniques.append("T")
        if self.tech_inline_var.get():
            techniques.append("Q")
        
        if techniques:
            command_parts.append(f"--technique={''.join(techniques)}")
        
        if self.os_detect_var.get():
            command_parts.append("--os-detect")
        
        if self.dbms_detect_var.get():
            command_parts.append("--dbms-detect")
        
        # Output directory
        if self.output_dir_var.get():
            command_parts.append(f"--output-dir=\"{self.output_dir_var.get()}\"")
        
        self.current_command = " ".join(command_parts)
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, self.current_command)
        self.status_var.set("✅ Command generated successfully")
        self.progress_var.set("🔧 Ready to execute")
    
    def execute_sqlmap(self):
        """Execute SQLMap command with professional feedback"""
        if not self.current_command:
            messagebox.showerror("Error", "Please generate a command first")
            return
        
        if self.is_running:
            messagebox.showwarning("Warning", "SQLMap is already running")
            return
        
        self.is_running = True
        self.status_var.set("🟡 Executing SQLMap...")
        self.progress_var.set("⏳ Initializing...")
        
        # Clear previous output
        self.output_text.delete(1.0, tk.END)
        
        # Add header to output
        self.output_text.insert(tk.END, "="*80 + "\n")
        self.output_text.insert(tk.END, "🔒 SQLMap Professional Scanner - Execution Started\n")
        self.output_text.insert(tk.END, f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, f"🎯 Command: {self.current_command}\n")
        self.output_text.insert(tk.END, "="*80 + "\n\n")
        
        # Execute in separate thread
        thread = threading.Thread(target=self._run_sqlmap)
        thread.daemon = True
        thread.start()
    
    def _run_sqlmap(self):
        """Run SQLMap command in separate thread"""
        try:
            # Execute the command
            process = subprocess.Popen(
                self.current_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output in real-time
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.root.after(0, self._update_output, line)
            
            process.wait()
            
            self.root.after(0, self._execution_finished)
            
        except Exception as e:
            self.root.after(0, self._execution_error, str(e))
    
    def _update_output(self, line):
        """Update output display"""
        self.output_text.insert(tk.END, line)
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def _execution_finished(self):
        """Handle execution completion"""
        self.is_running = False
        self.status_var.set("🟢 SQLMap execution completed successfully")
        self.progress_var.set("✅ Done")
        
        # Add completion footer
        self.output_text.insert(tk.END, "\n" + "="*80 + "\n")
        self.output_text.insert(tk.END, "✅ SQLMap execution completed successfully\n")
        self.output_text.insert(tk.END, f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, "="*80 + "\n")
        
        messagebox.showinfo("Success", "🎉 SQLMap execution completed successfully!")
    
    def _execution_error(self, error):
        """Handle execution error"""
        self.is_running = False
        self.status_var.set("🔴 SQLMap execution failed")
        self.progress_var.set("❌ Error")
        
        # Add error footer
        self.output_text.insert(tk.END, "\n" + "="*80 + "\n")
        self.output_text.insert(tk.END, "❌ SQLMap execution failed\n")
        self.output_text.insert(tk.END, f"🚨 Error: {error}\n")
        self.output_text.insert(tk.END, f"⏰ Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.output_text.insert(tk.END, "="*80 + "\n")
        
        messagebox.showerror("Error", f"❌ SQLMap execution failed:\n{error}")
    
    def stop_execution(self):
        """Stop SQLMap execution"""
        if self.is_running:
            self.is_running = False
            self.status_var.set("Stopping SQLMap...")
            # Note: In a real implementation, you would need to kill the process
            messagebox.showinfo("Info", "Stop functionality would terminate the SQLMap process")
    
    def clear_output(self):
        """Clear output display"""
        self.output_text.delete(1.0, tk.END)
        self.command_text.delete(1.0, tk.END)
        self.status_var.set("🗑️ Output cleared")
        self.progress_var.set("")
    
    def save_output(self):
        """Save output to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("SQLMap Command:\n")
                    f.write(self.current_command + "\n\n")
                    f.write("SQLMap Output:\n")
                    f.write(self.output_text.get(1.0, tk.END))
                messagebox.showinfo("Success", f"Output saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save output: {e}")
    
    def load_presets(self):
        """Load professional presets"""
        self.presets = {
            "🚀 Quick Scan": {
                "risk": "2",
                "level": "3",
                "batch": True,
                "verbose": True,
                "random_agent": True
            },
            "🔍 Comprehensive Scan": {
                "risk": "3",
                "level": "5",
                "threads": "10",
                "batch": True,
                "verbose": True,
                "enum_dbs": True,
                "enum_tables": True,
                "enum_columns": True,
                "random_agent": True
            },
            "📊 Database Enumeration": {
                "risk": "2",
                "level": "3",
                "batch": True,
                "enum_dbs": True,
                "enum_tables": True,
                "enum_columns": True,
                "verbose": True
            },
            "💾 Data Extraction": {
                "risk": "3",
                "level": "4",
                "batch": True,
                "dump_all": True,
                "verbose": True,
                "random_agent": True
            },
            "🎯 Stealth Mode": {
                "risk": "1",
                "level": "2",
                "delay": "2",
                "batch": True,
                "tor": True,
                "random_agent": True
            },
            "⚡ Aggressive Scan": {
                "risk": "3",
                "level": "5",
                "threads": "15",
                "batch": True,
                "verbose": True,
                "enum_dbs": True,
                "enum_tables": True,
                "enum_columns": True,
                "dump_all": True
            }
        }
        
        # Update preset listbox
        self.preset_listbox.delete(0, tk.END)
        for preset_name in self.presets.keys():
            self.preset_listbox.insert(tk.END, preset_name)
    
    def load_preset(self):
        """Load selected preset"""
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a preset to load")
            return
        
        preset_name = self.preset_listbox.get(selection[0])
        preset = self.presets[preset_name]
        
        # Apply preset values
        for key, value in preset.items():
            if hasattr(self, f"{key}_var"):
                getattr(self, f"{key}_var").set(value)
        
        self.status_var.set(f"✅ Loaded preset: {preset_name}")
        self.progress_var.set("⚙️ Preset applied")
        messagebox.showinfo("Success", f"✅ Preset '{preset_name}' loaded successfully!")
    
    def save_preset(self):
        """Save current settings as preset"""
        preset_name = simpledialog.askstring("💾 Save Preset", "Enter preset name:")
        if not preset_name:
            return
        
        # Add emoji if not present
        if not any(ord(char) > 127 for char in preset_name):
            preset_name = f"⚙️ {preset_name}"
        
        # Collect current settings
        preset = {}
        for attr_name in dir(self):
            if attr_name.endswith('_var') and hasattr(getattr(self, attr_name), 'get'):
                var = getattr(self, attr_name)
                value = var.get()
                if value:  # Only save non-empty values
                    key = attr_name[:-4]  # Remove '_var' suffix
                    preset[key] = value
        
        self.presets[preset_name] = preset
        self.load_presets()  # Refresh the list
        self.status_var.set(f"✅ Preset '{preset_name}' saved")
        self.progress_var.set("💾 Saved")
        messagebox.showinfo("Success", f"✅ Preset '{preset_name}' saved successfully!")
    
    def delete_preset(self):
        """Delete selected preset"""
        selection = self.preset_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a preset to delete")
            return
        
        preset_name = self.preset_listbox.get(selection[0])
        
        if messagebox.askyesno("🗑️ Confirm Deletion", f"Are you sure you want to delete preset '{preset_name}'?"):
            del self.presets[preset_name]
            self.load_presets()  # Refresh the list
            self.status_var.set(f"🗑️ Preset '{preset_name}' deleted")
            self.progress_var.set("")
            messagebox.showinfo("Success", f"✅ Preset '{preset_name}' deleted successfully!")

def main():
    """Main function - Professional SQLMap GUI Launcher"""
    try:
        root = tk.Tk()
        
        # Set window icon (if available)
        try:
            root.iconbitmap('sqlmap_icon.ico')
        except:
            pass
        
        # Create application
        app = SQLMapGUI(root)
        
        # Center the window professionally
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 1400
        window_height = 900
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Set window properties
        root.resizable(True, True)
        root.minsize(1200, 800)
        
        # Start the application
        print("🔒 SQLMap Professional GUI Started Successfully")
        print("🎯 Ready for SQL Injection Testing")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting SQLMap GUI: {e}")
        messagebox.showerror("Startup Error", f"Failed to start SQLMap GUI:\n{e}")

if __name__ == "__main__":
    main()
