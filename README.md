# Image Gallery Streamlit App

This is a simple Streamlit application that displays a gallery of 50 images. When an image is clicked, the app shows related images by appending specific suffixes to the base image filename. The related images are organized into three categories:
- **Graphs:** Images located in `results/graphs`
- **Hedonic GIF:** Images located in `results/hedonic_gif`
- **Segmented Images:** Images located in `results/segmented_images`

## Requirements

Install the Python requirements using the following command:
```console
pip install -r requirements.txt
```

## Run application
For start the application activate env:
```console
venv\Scripts\activate
```

To run each main run the command below in root directory:
```console
streamlit run app.py
```