from marker.convert import convert_single_pdf
from marker.models import load_all_models
import os


class ParseThat_PDF_Agent:
    def __init__(self):
        self._images = None
        self._fulltext = None
        self._metadata = None

    def parse(self, filepath):
        """
        Parse the PDF file and extract full text, images, and metadata.

        :param filepath: Path to the PDF file.
        """
        fpath = filepath  # Corrected variable assignment
        model_lst = load_all_models()
        full_text, images, out_meta = convert_single_pdf(fpath, model_lst)

        self._fulltext = full_text
        self._images = images
        self._metadata = out_meta

    def save(self, filepath, save_fulltext=True, save_images=True, save_metadata=True):
        """
        Save the extracted text, images, and metadata.

        :param filepath: Path to the output folder or file.
        :param save_fulltext: Boolean to indicate if full text should be saved.
        :param save_images: Boolean to indicate if images should be saved.
        :param save_metadata: Boolean to indicate if metadata should be saved.
        """
        # Define the output folder based on the PDF file name
        base_name = os.path.splitext(os.path.basename(filepath))[0]
        output_folder = os.path.join(os.path.dirname(filepath), base_name)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        # Save full text as a Markdown file
        if save_fulltext and self._fulltext:
            output_md_path = os.path.join(output_folder, f"{base_name}.md")
            with open(output_md_path, "w", encoding="utf-8") as md_file:
                md_file.write(self._fulltext)
            print(f"Markdown file saved at {output_md_path}")

        # Save images in a subfolder
        if save_images and self._images:
            output_images_folder = os.path.join(output_folder, "images")
            os.makedirs(output_images_folder, exist_ok=True)

            for filename, image in self._images.items():
                image_path = os.path.join(output_images_folder, filename)
                image.save(image_path)
            print(f"Images saved in folder: {output_images_folder}")

        # Save metadata as a JSON file
        if save_metadata and self._metadata:
            output_meta_path = os.path.join(output_folder, f"{base_name}_metadata.json")
            with open(output_meta_path, "w", encoding="utf-8") as meta_file:
                json.dump(self._metadata, meta_file, indent=2)
            print(f"Metadata saved at {output_meta_path}")
