import streamlit as st
import subprocess
import tempfile
import os


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
        
        # Run deface CLI program
        if st.button("Run deface"):
            output_file = "defaced_video.mp4"
            command = ["deface", temp_file_path, "-o", output_file]
            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
