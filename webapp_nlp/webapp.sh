#!/bin/bash

## Start Installation

echo "You are going to install react and flask necessities tools"


# Install NVM(Node Version Manager)
echo "Installing NVM..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
sleep 2

# Load NVM
echo "**ADD TO BASH**"
source ~/.bashrc
#export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
#[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

sleep 2

# install latest node js

echo "Installing latest Node.js"
nvm install node

# Install npm via apt-get to ensure it's available (might not be the latest version)
echo "Installing npm via apt-get..."
apt-get update && apt-get install -y npm

sleep 2

# Update npm to the latest version
echo "Updating npm to the latest version..."
npm update -g
sleep 2


# Install React Router
echo "Installing React Router..."
yarn add react-router-dom
sleep 2

# Install React Bootstrap
echo "Installing React Bootstrap..."
npm install react-bootstrap bootstrap

# Install React Hook Form
echo "Installing React Hook Form..."
npm install react-hook-form
sleep 2

# Install Flask and Flask-CORS for the Flask server
echo "Installing Flask and Flask-CORS..."
pip install flask flask-cors
sleep 1

# Install Axios for making HTTP requests from React
echo "Installing Axios..."
yarn add axios
sleep 2

# Install React Chart.js
#echo "Installing React Chart.js..."
#npm install react-chartjs-2 chart.js

# Install pdf viewer

#echo "Install PDF viewer"
# pdf viewer:
#npm install @react-pdf/renderer pdfjs-dist

echo "React Pdf installation!"
npm i react-pdf

# react chat bot
echo "Chat BOT react"
npm i react-chatbot-kit

echo "Installation complete Successfull!!"





