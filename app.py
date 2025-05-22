import streamlit as st
from docling.document_converter import DocumentConverter
import tempfile
import os
from pathlib import Path

st.title("Markdown Converter")

st.write("Upload a document and convert it to Markdown.")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "pptx"])


def convert():
    # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        # Convert the document
        converter = DocumentConverter()
        result = converter.convert(temp_path)
        
        # Generate unique filename
        output_path = f"{uploaded_file.name}.md"
        
        # Save result
        result.document.save_as_markdown(output_path)
        
        # Read the markdown file to create a download link
        with open(output_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Create download button
        st.download_button(
            label="Download Markdown",
            data=markdown_content,
            file_name=f"converted_{uploaded_file.name}.md",
            mime="text/markdown"
        )
        
        # Clean up temporary files
        os.remove(temp_path)
        os.remove(output_path)
        
        st.success("Conversion completed successfully!")

if uploaded_file is not None:
    try:
        if st.button("Convert"):
            convert()
    except Exception as e:
        st.error(f"An error occurred during conversion: {str(e)}")
