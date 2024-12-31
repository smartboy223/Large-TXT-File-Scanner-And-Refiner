
# Scan and Refine Large TXT Files

## 📋 Project Overview
**Scan and Refine Large TXT Files** is a Python-based graphical user interface (GUI) tool for processing and refining large text files. With this tool, you can:

- Dynamically filter lines using include and exclude keywords.
- Process multiple text files in a batch.
- Display refined results in a visually intuitive table.
- Save the results to a file for future use.

This tool is especially useful for users who need to sift through massive text files and extract specific lines based on customizable criteria.

---

## 🛠️ Features

- **Dynamic Filtering**: Refine lines based on include or exclude keywords.
- **Batch Processing**: Handle multiple text files simultaneously.
- **Interactive GUI**: A user-friendly interface built with Tkinter.
- **Result Management**: Save refined results to a file or clear them with one click.
- **Customizable Settings**: Set the maximum number of results, select files, and adjust filters dynamically.

---

## 📝 Prerequisites

Ensure you have Python 3.x installed on your system. Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/smartboy223/Scan-and-refine-large-txt-file.git
   cd Scan-and-refine-large-txt-file
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python3 refine.py
   ```

---

## 📂 Input File Information

- Replace the default `input.txt` file with your own large text file.
- The code is capable of processing extremely large files. It has been tested successfully with a **5GB file containing 80 million lines**.
- By default, the tool stops after refining **100 results**, but it can handle up to **3000 refined results** with ease. Depending on the file size and filters applied, this may take a few seconds or minutes.

---

## 📂 File Structure

- **`refine.py`**: The main Python script for running the GUI tool.
- **`requirements.txt`**: File listing all Python dependencies for the project.
- **`README.md`**: Documentation for the project.
- **Sample Input Files**: Example text files (`input.txt`, `input-1.txt`, etc.) to test the functionality.

---

## 💡 Example Usage

### Input
- **Include Keywords**: `keyword1, keyword2`
- **Exclude Keywords**: `exclude1, exclude2`
- **Text Files**: Replace `input.txt` with your own large text file.

### Output
- A refined results file (`refined_results.txt`) containing lines that match the include/exclude criteria.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## 📧 Contact

Created by **smartboy223**. For any questions or feedback, reach out via GitHub.

---

## 🏆 Acknowledgments

Thanks to the open-source community for tools and inspiration that make this project possible.

---
