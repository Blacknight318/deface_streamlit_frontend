# Streamlit wrapper for the python deface module for facial blurr

## Running the code natively

### Running the program
```bash
git clone https://github.com/Blacknight318/deface_streamlit_frontend.git
cd deface_streamlit_frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### libgl error
If you get a libgl and are on ubuntu not using a fiscrete graphics card run the following
```bash
sudo apt install libgl1-mesa-glx
```

### NVIDIA GPU
If you're using an NVIDIA GPU then you can comment out line 60 to revert back to the default onnxruntime.


## Running as a docker
```bash
docker run -d --name deface-streamlit-frontend -p 8080:8501 merlin615/deface-webui:nonvidia-latest
```
