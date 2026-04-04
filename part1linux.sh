#!/bin/bash
set -euo pipefail


print_message() {
    printf "\n========================================\n"
    printf "%s\n" "$1"
    printf "========================================\n\n"
}

# Feature 2: Detecting OS using OSTYPE
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        PKG_MANAGER="brew"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="Linux"
        PKG_MANAGER="apt-get"
    else
        OS="Unknown"
        PKG_MANAGER="unknown"
    fi
    print_message "Detected OS: $OS"
}

# Feature 3: Check and install Python
check_python() {
    print_message "Checking for Python3..."

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_message "Python3 is already installed: $PYTHON_VERSION"
    else
        print_message "Python3 not found. Installing..."
        if [[ "$OS" == "macOS" ]]; then
            brew install python3
        elif [[ "$OS" == "Linux" ]]; then
            sudo apt-get update
            sudo apt-get install -y python3
        fi
        print_message "Python3 installation complete"
    fi
}

# Feature 4: Verify pip is available, install if missing
check_pip() {
    print_message "Checking for pip..."

    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        print_message "pip is available: $PIP_VERSION"
    else
        print_message "pip not found. Installing..."
        if [[ "$OS" == "macOS" ]]; then
            python3 -m ensurepip --upgrade
        elif [[ "$OS" == "Linux" ]]; then
            sudo apt-get install -y python3-pip
        fi
        print_message "pip installation complete"
    fi
}

# Feature 5: Install Jupyter Notebook
install_jupyter() {
    print_message "Checking for Jupyter Notebook..."

    if command -v jupyter &> /dev/null; then
        print_message "Jupyter is already installed"
        return
    fi

    print_message "Installing Jupyter Notebook..."
    pip3 install jupyter
    print_message "Jupyter Notebook installation complete"
}

# Feature 6: macOS-specific Homebrew health check
check_brew_health() {
    if [[ "$OS" == "macOS" ]]; then
        print_message "Running Homebrew diagnostics..."
        brew doctor
    fi
}

# Main
print_message "Starting Development Environment Setup"
detect_os
check_python
check_pip
install_jupyter
check_brew_health
print_message "Setup Complete! Your development environment is ready."