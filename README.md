# 🗪 Private AI Chatbot App for Ollama
Your private AI chatbot app for Android, Linux, Windows and iOS. The application is made with [Kivy](https://kivy.org/) and [KivyMD](https://kivymd.readthedocs.io/en/latest/) which can interact with the `LLM` models hosted on [Ollama](https://ollama.com/). This app needs a URL of the `Ollama API` endpoint.

> Overview: The app uses KivyMD and Kivy mainly for the AI Chatbot UI and uses python requests module to perform the chat functions using the Ollama API endpoint. The Ollama can be hosted anywhere as long as the application has a network connectivity to the Ollama URL. The app can pull out the list of installed LLM models and we can choose a model from the drop-down menu at the top. Please find the installation and build steps as descried below.

## 📽️ Demo
You can click on the below Image or this [Youtube Link](https://www.youtube.com/watch?v=a-azvqDL78k) to see the demo. Please let me know in the comments, how do you feel about this App. <br>
[![AI-Kivy-Chatbot](./docs/images/thumb.jpg)](https://www.youtube.com/watch?v=a-azvqDL78k)

## 🖧 Our Scematic Architecture
This is the scematic flow [diagram](./docs/images/kivyOllamaFlow.gif) <br>
![Flow-Diagram](./docs/images/kivyOllamaFlow.gif)

## 🧑‍💻 Quickstart Guide

### 📱 Download & Run the Android App
You can check the [Releases](https://github.com/daslearning-org/Ollama-AI-Chat-App/releases) and downlaod the latest version of the android app on your phone.

### 🐍 Run with Python
```bash
git clone https://github.com/daslearning-org/Ollama-AI-Chat-App.git
cd Ollama-AI-Chat-App/kivy/
pip install -r requirements.txt # virtual environment is recommended
python main.py
```

## 🦾 Build your own App
The Kivy project has a great tool named [Buildozer](https://buildozer.readthedocs.io/en/latest/) which can make mobile apps for `Android` & `iOS`

### 📱 Build Android App
A Linux environment is recommended for the app development. If you are on Windows, you may use `WSL` or any `Virtual Machine`. As of now the `buildozer` tool works on Python version `3.10` at maximum. I am going to use Python `3.9`

```bash
# add the python repository
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# install all dependencies.
sudo apt install -y ant autoconf automake ccache cmake g++ gcc lbzip2 libffi-dev libltdl-dev libtool libssl-dev make openjdk-17-jdk patch pkg-config python3-dev python3-pip unzip wget zip git python3.9 python3.9-venv

# optionally you may check the java installation with below commands
java -version
javac -version

# install python modules
git clone https://github.com/daslearning-org/Ollama-AI-Chat-App.git
cd Ollama-AI-Chat-App/kivy/
python3.9 -m venv .env # create python virtual environment
source .env/bin/activate
pip install -r requirements.txt

# build the android apk
buildozer android debug # this may take a good amount of time for the first time & will generate the apk in the bin directory
```

### Build Computer Application (Windows / Linux / MacOs)
Again a `Linux` environment is recommended and please follow the same steps from above till the pip module installations (do not require buildozer for desktop apps). Build cross platform apps from [docker image](https://hub.docker.com/r/cdrx/pyinstaller-windows)

```bash
# install pyinstaller
pip install pyinstaller

# generate the spec file
pyinstaller --name "dasLearningChat" --windowed --onefile main.py

# then update the spec file as needed
# then build your app which will be native to the OS i.e. Linux or Windows or MAC
pyinstaller dasLearningChat.spec

```
