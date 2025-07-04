
# GUI-Based Multi-threaded Port Scanner

A Python-based **TCP Port Scanner** with a graphical interface built using Tkinter. This tool allows users to scan a range of ports on any IP address or hostname, view open/closed ports in real time, and interact with a simple, user-friendly UI.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Overview

This application performs real-time port scanning using **multi-threaded socket connections**. It allows users to input a target IP or domain, define a custom port range, and view live results of which ports are open or closed.

Designed to be efficient and responsive, the scanner can be used for educational, security testing, or administrative purposes within legally permitted environments.

---

## Features

- TCP connect scanning using raw sockets  
- Multi-threaded for faster execution  
- Real-time output of open and closed ports  
- Start/Stop functionality during scans  
- Status label for user feedback  
- Summary popup after scan completion  
- Clean and minimal dark-themed GUI  

---

## Technologies Used

| Technology | Purpose                       |
|------------|-------------------------------|
| Python     | Core programming language     |
| Tkinter    | GUI interface                 |
| socket     | TCP connection testing        |
| threading  | Multi-threaded execution      |
| time       | Duration measurement, delays  |

---

## System Architecture

```
User Input → Input Validation → Threaded TCP Connections → Real-Time Result Display → Summary Popup
```

Each port in the specified range is scanned using a separate thread to check for open connections. Results are updated in a `Treeview` widget with color tags based on status.

---

## How It Works

### User Input
- Target IP/Hostname  
- Start and End port range  

### Workflow
1. Validate inputs  
2. Launch individual threads per port  
3. Attempt TCP connection on each port  
4. Update display as:
   - `OPEN` (if connection successful)  
   - `Closed` (otherwise)  
5. Show popup summary after scan (total open ports + scan duration)  

---

## Usage

### Prerequisites

- Python 3.x  

### Installation

```bash
git clone https://github.com/yourusername/gui-port-scanner.git
cd gui-port-scanner
```

### Running the Application

```bash
python port_scanner.py
```

### Notes

- Ensure that firewall/antivirus does not block Python's outbound connections  
- Only scan systems you have permission to test  

---


## Future Enhancements

| Feature           | Description                                 |
|------------------|---------------------------------------------|
| Service Detection| Show common services (e.g., HTTP on port 80)|
| Export Results   | Save results as CSV or JSON                 |
| Banner Grabbing  | Fetch and display basic service banners     |
| Thread Pooling   | Smarter concurrency management              |
| UDP Scanning     | Add support for scanning UDP ports          |
| Responsive GUI   | Make UI adjust to screen size               |

---

## License

This project is for **educational and ethical use only**. Unauthorized scanning of devices or networks without permission is strictly discouraged.

---

## Author

Created as part of a cybersecurity-focused internship project.
