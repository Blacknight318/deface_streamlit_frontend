import streamlit as st
import subprocess
import tempfile
import os
import re


def parse_percentage(output_line):
    match = re.search(r"(\d+)%", output_line)
    if match:
        percentage = int(match.group(1))
        return percentage
    else:
        return None

def main():
    st.title("Anonymizing Video Files")
    st.write("Blur faces in video files for anonymity.")

    # File selection
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov"])

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
        threshold = st.slider("Adjust threshold(default 0.2)", min_value=0.01, max_value=0.99, value=0.2, step=0.01)

        # Run deface CLI program
        if st.button("Run deface"):
            output_file = "defaced_video.mp4"
            command = ["deface", temp_file_path, "-o", output_file]
            if add_option:
                command.append("--keep-audio")

            if threshold != 0.2:
                command.extend(["-t", str(threshold)])

            progress_bar = st.progress(0)

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

            for line in process.stdout:
                percentage = parse_percentage(line)
                if percentage is not None:
                    progress_bar.progress(percentage)

            # Wait for the CLI command to finish
            process.wait()

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                st.success("Deface process completed successfully!")
                st.video(output_file)

                # Download code
                with open('defaced_video.mp4', 'rb') as f:
                    st.download_button('Download MP4', f, file_name='defaced_video.mp4')
                    os.remove(output_file)
            else:
                st.error("Deface process failed. Error message:")
                st.code(stderr.decode("utf-8"))

        # Cleanup temporary directory
        temp_dir.cleanup()


if __name__ == "__main__":
    main()
