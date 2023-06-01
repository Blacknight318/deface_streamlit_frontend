import streamlit as st
import subprocess
import tempfile
import os
import re
import time
# import threading


def parse_percentage(output_line):
    # Implement your own logic to extract the percentage value from the output line
    # This depends on the format of the output from your CLI command
    # Return the extracted percentage value as an integer or None if not found
    # Example: If the percentage is in the format "100%|██████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 2137/2137 [07:48<00:00, 4.57it/s]"
    # Extract the percentage value using regular expressions
    match = re.search(r"(\d+)%", output_line)
    if match:
        percentage = int(match.group(1))
        return percentage
    else:
        return None

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def main():
    st.title("Anonymizing Video Files")
    st.write("Blur faces in video files for anonymity.")
    
    # File selection
    video_file = st.file_uploader("Upload a video file", type=["mp4"])
    
    # Display video if a file is selected
    if video_file is not None:
        st.video(video_file)
        
        # Save uploaded file to temporary location
        temp_dir = tempfile.TemporaryDirectory()
        temp_file_path = os.path.join(temp_dir.name, video_file.name)
        with open(temp_file_path, "wb") as f:
            f.write(video_file.read())
           
        # Adding options to retain audio and set threshold for more customized processing
        add_option = st.checkbox("Add --keep-audio option")

        # Adding slider from 0.01 to 0.99 for threshold adjustment
        threshold = st.slider("Adjust threshold (default 0.2)", min_value=0.01, max_value=0.99, value=0.2, step=0.01)

        # Run deface CLI program
        if st.button("Run deface"):
            
            # output_file = "defaced_video.mp4"
            output_file = os.path.join(temp_dir.name, os.path.splitext(video_file.name)[0] + "_processed.mp4")
            start_time = time.time()
            command = ["deface", temp_file_path, "-o", output_file]
            
            if add_option:
                command.append("--keep-audio")
            
            if threshold != 0.2:
                command.extend(["-t", str(threshold)])

            # Adding switch to OpenCV, primarily for those without an Nvidia GPU
            command.extend(["--backend", "opencv"])
            
            # Initialize the progress variable
            progress_bar = st.progress(0)

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            
            for line in process.stdout:
                percentage = parse_percentage(line)
                if percentage is not None:
                    progress_bar.progress(percentage)

            # Wait for the CLI command to finish
            process.wait()
    
            # Show a completion message
            # st.success("Deface completed!")

            
            if process.returncode == 0:
                st.success("Deface process completed successfully!")
                st.video(output_file)
                end_time = time.time()
                elapsed_time =  end_time - start_time
                formatted_time = format_time(elapsed_time)
                st.write(f"Processing took {formatted_time} seconds.")

                # Download code
                with open(output_file, 'rb') as f:
                    st.download_button('Download MP4', f, file_name=output_file)
                    # os.remove(output_file)
            else:
                st.error("Deface process failed. Error message:")
                st.code(process.stderr.read())
        
        # Cleanup temporary directory
        temp_dir.cleanup()


if __name__ == "__main__":
    main()
