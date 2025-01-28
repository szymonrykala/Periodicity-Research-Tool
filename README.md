
# String Pattern Research Tool

**SPRT** is a Python-based project designed for efficient data processing and visualization. This project includes a structured development environment for streamlined workflows and easy automation.

---

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
  - [Testing](#testing)
  - [Code Formatting](#code-formatting)
  - [Building](#building)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/szymonrykala/Periodicity-Research-Tool
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry run bash
   ```

---

## Usage

To run the application in development mode:
```bash
poetry run python sprt
```

To run the application after building:
```bash
poe run-build
```

---

## Development

The project uses `poethepoet` for task automation. Available commands are:

### Testing
Run tests:
```bash
poe test
```

### Code Formatting
Format the code:
```bash
poe format
```

### Building
Build the project into a standalone executable:
```bash
poe build
```

--- 

Feel free to contact the author, **Szymon Rykała**, at `<szymonrykala@gmail.com>` for any questions or feedback.
