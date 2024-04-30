# ✨ Geminal ✨

A Chatbot on Terminal powered by Google Generative AI.

## 🎥 Demo

[demo.mp4](https://github.com/nhattdm/Geminal/assets/86051561/33de07f3-5eb3-4855-933e-3fe90904bd05)

## 🎯 Why Geminal?

Windows has integrated Copilot into its own system, but Linux does not. Therefore, I developed Geminal, a chatbot for
the terminal powered by Google's Generative AI, specifically designed for Linux programmers.

Here's why you might choose Geminal:

* **Focus on your code:** Geminal integrates seamlessly into your terminal, allowing you to ask questions about your
  code without leaving your workflow.
* **Open source and free to use:** Geminal is open source and completely free to use, making it an accessible option for
  all programmers.
* **Fast and efficient:** Geminal utilizes Gemini Pro, a powerful AI assistant, to provide you with accurate and timely
  answers.
* **Tailored to Linux users:** Geminal is designed specifically for Linux users, ensuring compatibility with your
  operating system.
* **Supports multiple languages:** Geminal supports a wide range of programming languages, making it a versatile tool
  for programmers of all backgrounds.
* **Easy to use:** Geminal's intuitive interface and simple commands make it easy to get started and use effectively.
* **Enhances productivity:** Geminal helps you save time and effort by providing instant assistance, allowing you to
  focus on the task at hand.

## 📌 Minimum Requirements

- Linux, macOS, or [WSL on Windows](https://learn.microsoft.com/en-us/windows/wsl/install)
- [Python](https://www.python.org/downloads/) >= 3.10

## ⚡ Quick Installation

```bash
pip install "https://github.com/nhattdm/Geminal/releases/download/v0.1.0/geminal-0.1.0.tar.gz"
```

## 🦾 Supported Model Versions

| Model name                   | Note                                        |
|------------------------------|---------------------------------------------|
| gemini-pro                   | gemini-pro is an alias for gemini-1.0-pro   |
| models/gemini-pro            | model code of Gemini 1.0 Pro                |
| gemini-1.0-pro-latest        | latest version of Gemini 1.0 Pro            |
| gemini-1.0-pro               | latest stable version of Gemini 1.0 Pro     |
| gemini-1.0-pro-001           | stable version of Gemini 1.0 Pro            |
| models/gemini-1.5-pro-latest | model code of Gemini 1.5 Pro (preview only) |

For more information, please refer to this [document](https://ai.google.dev/gemini-api/docs/models/gemini).

## ❓ Usage

Please, make sure that you have set GOOGLE_API_KEY and MODEL_NAME as environment variables.

```
Usage: geminal [-v] [-h] [PROMPT]

Geminal is a chatbot on Terminal powered by Google Generative AI.

options:
    -h, --help      Show this help message and exit.
    -v, --version   Show version and exit.

prompt:
    Your prompt can be added after `geminal`. Example: geminal who are you?
```

## 🛠 How to install Geminal from `tar.gz` package in source code

```bash
git clone https://github.com/nhattdm/Geminal.git

cd geminal

make install
```

## 🛠 How to build Geminal from source code

```bash
git clone https://github.com/nhattdm/Geminal.git

cd geminal

make build
```

## 🐳 How to dockerize Geminal as an image to run with Docker _(lowly recommended)_

- **Step 1:** Please make sure that you have installed Docker on your computer before moving on to the next step.


- **Step 2:** Dockerize Geminal as an image.

```bash
git clone https://github.com/nhattdm/Geminal.git

cd Geminal

make dockerize
```

- **Step 3:** Run just the created image with Docker.

```bash
docker run -it --rm --name geminal geminal
```

If you're wondering why this is not highly recommended, please refer to the [Notes](#-notes) section for more
information.

## 📝 Notes

- If you don't have your own GOOGLE API KEY, visit [Makersuite by Google](https://makersuite.google.com/) and create a
  new one for free.
- Use `Tab` or `Alt+Enter` for a newline (multiline input).
- The list of actions that interact with the last response from Gemini Pro will not be available if you run the
  application
  in a container.
- In case you're unable to copy the last message or code block from Gemini Pro to your clipboard, install
  the [`xclip`](https://linuxconfig.org/how-to-use-xclip-on-linux) package if you're using a Linux distribution. For
  macOS users, seek a similar solution.

## ⚙️ Developed & Tested on

- Ubuntu 22.04
- Python 3.10
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) 1.8.2
- [Anaconda3](https://docs.anaconda.com/free/anaconda/install/linux/#installation)
  or [Miniconda3](https://docs.anaconda.com/free/miniconda/miniconda-install/) (Optional)

## 🤝 Contributing

I don't have plans to continue maintaining this project anymore. Feel free to contribute to this project if you have any
further ideas.

## 📃 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
