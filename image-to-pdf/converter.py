from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import sys

def convert_images_to_pdf(image_paths, output_pdf):
    """
    Convert one or multiple images to a PDF file.
    
    Args:
        image_paths (list): List of image file paths
        output_pdf (str): Output PDF file path
    """
    try:
        # Create a new PDF with the specified name
        c = canvas.Canvas(output_pdf, pagesize=A4)
        
        # Process each image
        for image_path in image_paths:
            if not os.path.exists(image_path):
                print(f"Warning: Image {image_path} not found. Skipping...")
                continue
                
            # Open and convert the image
            img = Image.open(image_path)
            
            # Get image size
            img_width, img_height = img.size
            
            # Calculate aspect ratio
            aspect = img_height / float(img_width)
            
            # Set maximum width and height for the PDF page
            max_width = 500  # points
            max_height = 700  # points
            
            # Calculate dimensions to fit the page while maintaining aspect ratio
            if aspect > float(max_height)/max_width:
                width = max_height / aspect
                height = max_height
            else:
                width = max_width
                height = max_width * aspect
            
            # Calculate centering
            x = (A4[0] - width) / 2
            y = (A4[1] - height) / 2
            
            # Draw the image
            c.drawImage(image_path, x, y, width, height)
            
            # Add a new page
            c.showPage()
        
        # Save the PDF
        c.save()
        print(f"PDF created successfully: {output_pdf}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Check if arguments are provided
    if len(sys.argv) < 3:
        print("Usage: python converter.py output.pdf image1.jpg [image2.jpg ...]")
        print("Example: python converter.py output.pdf img1.jpg img2.jpg img3.png")
        return
    
    # Get output PDF name and image paths from command line arguments
    output_pdf = sys.argv[1]
    image_paths = sys.argv[2:]
    
    # Convert images to PDF
    convert_images_to_pdf(image_paths, output_pdf)

if __name__ == "__main__":
    main()
