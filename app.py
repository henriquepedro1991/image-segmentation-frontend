import streamlit as st
import os
import base64
from glob import glob
from streamlit_clickable_images import clickable_images

# Directories for main images and related images
IMAGES_DIR = "images"
GRAPHS_DIR = os.path.join("results", "graphs")
HEDONIC_GIF_DIR = os.path.join("results", "hedonic_gif")
SEGMENTED_DIR = os.path.join("results", "segmented_images")

# Related image suffixes
GRAPH_SUFFIXES = [
    "_graph_hedonic",
    "_graph_infomap",
    "_graph_label_propagation",
    "graph_leiden",
    "_graph_louvain",
    "_graph",
]
HEDONIC_GIF_SUFFIXES = ["_hedonic_animation_boomerang"]
SEGMENTED_SUFFIXES = [
    "_segmented_hedonic",
    "_segmented_infomap",
    "_segmented_label_propagation",
    "_segmented_leiden",
    "_segmented_louvain",
]

# Mapping dictionaries for captions
GRAPH_CAPTIONS = {
    "_graph_hedonic": "Hedonic Method",
    "_graph_infomap": "Infomap Method",
    "_graph_label_propagation": "Label Propagation Method",
    "graph_leiden": "Leiden Method",
    "_graph_louvain": "Louvain Method",
    "_graph": "Graph",
}

HEDONIC_GIF_CAPTIONS = {"_animation_boomerang_gif": "Boomerang Animation"}

SEGMENTED_CAPTIONS = {
    "_segmented_hedonic": "Hedonic Method",
    "_segmented_infomap": "Infomap Method",
    "_segmented_label_propagation": "Label Propagation Method",
    "_segmented_leiden": "Leiden Method",
    "_segmented_louvain": "Louvain Method",
}


def to_data_url(filepath: str) -> str:
    """Convert a local image file to a Base64 data URI."""
    with open(filepath, "rb") as f:
        data = f.read()
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".png":
        mime_type = "image/png"
    elif ext == ".gif":
        mime_type = "image/gif"
    else:
        mime_type = "image/jpeg"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def get_main_images():
    """Retrieve all main images from the 'images' folder (JPG/PNG/GIF)."""
    jpg_files = glob(os.path.join(IMAGES_DIR, "*.jpg"))
    png_files = glob(os.path.join(IMAGES_DIR, "*.png"))
    gif_files = glob(os.path.join(IMAGES_DIR, "*.gif"))
    return jpg_files + png_files + gif_files


def get_image_id_from_filename(filepath):
    """Extract the image ID (base name without extension)."""
    basename = os.path.basename(filepath)
    image_id, _ = os.path.splitext(basename)
    return image_id


def find_related_files(image_id: str, directory: str, suffixes: list):
    """
    For each suffix, look for any file extension matching: {image_id}{suffix}.*
    Returns a list of file paths (or None if not found).
    """
    paths = []
    for suffix in suffixes:
        pattern = os.path.join(directory, f"{image_id}{suffix}.*")
        matches = glob(pattern)
        if matches:
            paths.append(matches[0])
        else:
            paths.append(None)
    return paths


def get_all_related_images(image_id: str) -> dict:
    """Group all related images into categories."""
    return {
        "Graphs": find_related_files(image_id, GRAPHS_DIR, GRAPH_SUFFIXES),
        "Hedonic GIF for alpha variation": find_related_files(
            image_id, HEDONIC_GIF_DIR, HEDONIC_GIF_SUFFIXES
        ),
        "Segmented Images": find_related_files(
            image_id, SEGMENTED_DIR, SEGMENTED_SUFFIXES
        ),
    }


def get_caption_for_file(filepath: str, image_id: str, caption_dict: dict) -> str:
    """
    Given a file path and the base image_id, extract the suffix and return
    the corresponding caption from caption_dict. If no mapping exists,
    return the original file name.
    """
    filename = os.path.basename(filepath)
    root, _ = os.path.splitext(filename)
    if root.startswith(image_id):
        suffix = root[len(image_id) :]
    else:
        suffix = root
    return caption_dict.get(suffix, filename)


st.title("Image Gallery")
st.header("Click on an image below to view its related images")

# Initialize session state for the selected image
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# Main gallery: show clickable main images
if st.session_state.selected_image is None:
    main_images = sorted(get_main_images())
    main_image_data_uris = [to_data_url(path) for path in main_images]
    main_image_titles = [os.path.basename(path) for path in main_images]

    clicked_index = clickable_images(
        main_image_data_uris,
        titles=main_image_titles,
        div_style={"display": "flex", "flex-wrap": "wrap"},
        img_style={"margin": "5px", "height": "150px"},
        key="main_image_gallery",
    )

    if clicked_index > -1:
        selected_path = main_images[clicked_index]
        st.session_state.selected_image = get_image_id_from_filename(selected_path)

# Related images display for the selected image
else:
    st.header(f"Related images for {st.session_state.selected_image}")
    all_related = get_all_related_images(st.session_state.selected_image)

    for group_name, paths in all_related.items():
        st.subheader(group_name)
        valid_paths = [p for p in paths if p is not None]
        if valid_paths:
            data_uris = [to_data_url(p) for p in valid_paths]
            if group_name == "Graphs":
                cap_dict = GRAPH_CAPTIONS
            elif group_name == "Hedonic GIF":
                cap_dict = HEDONIC_GIF_CAPTIONS
            elif group_name == "Segmented Images":
                cap_dict = SEGMENTED_CAPTIONS
            else:
                cap_dict = {}
            captions = [
                get_caption_for_file(p, st.session_state.selected_image, cap_dict)
                for p in valid_paths
            ]
            clickable_images(
                data_uris,
                titles=captions,
                div_style={"display": "flex", "flex-wrap": "wrap"},
                img_style={"margin": "5px", "height": "150px"},
                key=f"related_{group_name}_{st.session_state.selected_image}",
            )
        else:
            st.write("No images found in this category.")
    if st.button("Back to Gallery"):
        st.session_state.selected_image = None
