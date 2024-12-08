import requests
import base64

def encode_pdf_to_base64(pdf_file_path):
    """
    Encode a PDF file into a base64 string for testing.
    """
    try:
        with open(pdf_file_path, "rb") as pdf_file:
            encoded_content = base64.b64encode(pdf_file.read()).decode("utf-8")
        return encoded_content
    except Exception as e:
        print(f"Error encoding PDF: {e}")
        return None

def test_process_pdf_endpoint():
    """
    Test the /process_pdf endpoint with a base64-encoded PDF.
    """
    
    url = "http://127.0.0.1:8080/process_pdf"  
    pdf_file_path = "Data/PDFs/Text PDF to Validate.pdf"   

    pdf_content = encode_pdf_to_base64(pdf_file_path)
    if not pdf_content:
        print("Failed to encode PDF file.")
        return
    
    payload = {
        "fileContent": pdf_content
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("Success! Response JSON:")
            print(response.json())
        else:
            print(f"Failed with status code {response.status_code}. Response:")
            print(response.json())
    except Exception as e:
        print(f"Error testing the endpoint: {e}")

if __name__ == "__main__":
    test_process_pdf_endpoint()
