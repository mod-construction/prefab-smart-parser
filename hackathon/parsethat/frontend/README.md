# smart-parser-ui

# Web Application: PDF Uploader and Structured Data Viewer

This repository contains a web application built with ReactJS and .NET. It allows users to upload PDF files, processes the uploaded file by calling a Python service, and returns structured data to be displayed on the client page.

## Features
- Upload a single PDF file through the user interface.
- Backend API (built with .NET) sends the PDF file path to the Python service.
- Displays structured data (text and tables) extracted and processed by the Python service.

## Technologies Used
- **Frontend**: ReactJS
- **Backend**: .NET (C#)

## Installation

### Prerequisites
- Link to python repository: https://github.com/LupoSun/AECHachathon_MOD_ParseThat
- Node.js and npm
- .NET SDK

### Steps

1. **Clone the Repository**:
   ```bash  
   git clone <repository-url>  
   cd web-application  

2.  **Configure the API endpoint**: Configure AiApiUrls for the Python service in the backend settings file (appsettings.json).