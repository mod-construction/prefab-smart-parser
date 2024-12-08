### Python Service  

**README.md**  

```markdown  
# Python Service: PDF Text and Table Extraction  

This repository contains a Python service that processes PDF files to extract text and tables, then converts the extracted content into structured data using OpenAI's models.  

## Features  
- Extracts text and tables from PDF files using `pdfplumber` or a similar library.  
- Utilizes OpenAI APIs for prompting and converting extracted content into structured data.  
- Receives PDF file paths from a web application and returns structured data in JSON format.  

## Technologies Used  
- Python 3.11.10  
- Libraries: `marker`, OpenAI API, `Flask`  

## Installation  

### Prerequisites  
- Python 3.11.10 or later  
- OpenAI API key  

### Steps 

1. **Clone the Repository**
   Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   cd python-service
   ```

2. **Create a Virtual Environment**
   Set up a Python virtual environment to isolate dependencies:

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Install Dependencies**
   Install the required Python packages listed in the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up API Key**
   Update the `secret.py` file in the root of the project to store your OpenAI API key:
   ```bash
   echo "OPENAI_API_KEY=your-openai-api-key" > 
   ```
   Replace `your-openai-api-key` with your actual API key from OpenAI.

5. **Run the Service**
   Start the Flask server to make the service accessible:
   ```bash
   python run.py
   ```

   The service will be available at `http://localhost:5000`.

## Usage

### API Endpoint

#### GET `/api/parseit`
**Description**: Processes a PDF file, extracts its text and tables, and returns structured data in JSON format.

- **Request Body**:
  ```json
  { "input": "path/to/pdf/file.pdf" }
  ```

## License
This project is licensed under the MIT License.