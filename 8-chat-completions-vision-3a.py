import os
from llama_stack_client import LlamaStackClient
from dotenv import load_dotenv
import logging
import base64
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError


load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


# Model: meta-llama/Llama-3.2-vision-11B
# ollama run llama3.2-vision:11b --keepalive 60m
# OR
# Model: ibm/Granite-3.2-vision-2B
# ollama run granite3.2-vision:2b-fp16 --keepalive 60m


LLAMA_STACK_SERVER=os.getenv("LLAMA_STACK_SERVER")
LLAMA_STACK_VISION_MODEL=os.getenv("LLAMA_STACK_VISION_MODEL")

PDF_TO_ANALYZE="images/invoice_2.pdf"

logger.info(LLAMA_STACK_SERVER)
logger.info(LLAMA_STACK_VISION_MODEL)

def convert_pdf_to_png(pdf_path):
    logger.info(f"Converting PDF to PNG: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    try:
        print(f"Converting {pdf_path} to PNG images...")
        # Convert PDF to a list of PIL images
        images = convert_from_path(pdf_path)

        # Get the base name of the PDF file without extension
        base_filename = os.path.splitext(os.path.basename(pdf_path))[0]

        # Extract the directory from pdf_path
        output_dir = os.path.dirname(pdf_path)
        if output_dir == '':
            output_dir = '.'  # Use current directory if no directory in path


        # Save each image as a PNG file
        for i, image in enumerate(images):
            output_filename = os.path.join(output_dir, f"{base_filename}_page_{i + 1}.png")
            image.save(output_filename, 'PNG')
            print(f"Saved page {i + 1} to {output_filename}")
            return output_filename

        print("Conversion complete.")

    except PDFInfoNotInstalledError:
        print("Error: pdf2image requires poppler to be installed and in PATH.")
        print("Please install poppler:")
        print("  macOS (brew): brew install poppler")
        print("  Debian/Ubuntu: sudo apt-get install poppler-utils")
        print("  Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases/")
    except PDFPageCountError:
        print(f"Error: Could not get page count for {pdf_path}. Is it a valid PDF?")
    except PDFSyntaxError:
        print(f"Error: PDF file {pdf_path} seems to be corrupted or invalid.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")        
        return base64_string

client = LlamaStackClient(base_url=LLAMA_STACK_SERVER)

converted_image = convert_pdf_to_png(PDF_TO_ANALYZE)
encoded_image = encode_image(converted_image)


response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encoded_image
                    }
                },
                {
                    "type": "text",
                    "text": "what is the invoice number and only the invoice number",
                }
            ]
        }
    ],    
    # temperature=0.0, 
)

print(response.completion_message.content)

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encoded_image
                    }
                },
                {
                    "type": "text",
                    "text": "what is seller's name",
                }
            ]
        }
    ],     
)

print(response.completion_message.content)

response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encoded_image
                    }
                },
                {
                    "type": "text",
                    "text": "what is seller's street address",
                }
            ]
        }
    ],     
)

print(response.completion_message.content)


response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encoded_image
                    }
                },
                {
                    "type": "text",
                    "text": "what is seller tax id",
                }
            ]
        }
    ],     
)

print(response.completion_message.content)


response = client.inference.chat_completion(
    model_id=LLAMA_STACK_VISION_MODEL,
    messages=[
        # {"role": "system", "content": "You are an expert image analyzer"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": {
                        "data": encoded_image
                    }
                },
                {
                    "type": "text",
                    "text": "what is the total gross worth, only the total",
                }
            ]
        }
    ],    
    # temperature=0.0, 
)

print(response.completion_message.content)

