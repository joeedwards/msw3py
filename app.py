import streamlit as st
import os

# Set the directory you want to manage
BASE_DIR = './'

def list_files(startpath):
    """List files and directories in the given path."""
    files_list = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        files_list.append('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            files_list.append('{}{}'.format(subindent, f))
    return files_list

def main():
    st.title("Simple File Manager with Streamlit")

    # List files and directories
    files = list_files(BASE_DIR)
    for file in files:
        st.text(file)

    # Upload files
    uploaded_file = st.file_uploader("Choose a file to upload", type=["txt", "csv", "png", "jpg"])
    if uploaded_file:
        with open(os.path.join(BASE_DIR, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getvalue())
        st.success(f"Uploaded {uploaded_file.name} successfully!")

    # Delete files
    selected_file = st.selectbox("Choose a file to delete", [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))])
    if st.button("Delete"):
        os.remove(os.path.join(BASE_DIR, selected_file))
        st.success(f"Deleted {selected_file} successfully!")

if __name__ == "__main__":
    main()