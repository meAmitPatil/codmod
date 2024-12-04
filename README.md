# CodMod - AI-Powered Code Modifier

[![Deploy on Render](https://img.shields.io/badge/Deployed%20on-Render-brightgreen)](https://codmod.onrender.com)

CodMod is an AI-powered web application designed to help developers modify, refine, and execute code seamlessly. With its user-friendly interface, CodMod integrates AI for real-time code modification suggestions and execution, making it a powerful tool for developers.

---

## 🚀 **Features**
- **Code Modification**: Input code and receive AI-powered modifications based on your requirements.
- **Real-Time Execution**: Run the generated code directly within the application to test results.
- **Beautiful UI**: Responsive and clean design for an enhanced user experience.
- **Mem0.ai Integration**: Memory features for context-based interactions.
- **Reflection Workflow**: Ensures generated code is optimized and refined through an iterative process of feedback and enhancement.
- **E2B Integration**: Secure and efficient real-time code execution powered by **E2B**.

---

## 🌐 **Live Application**
Access CodMod live at: [https://codmod.onrender.com](https://codmod.onrender.com)

---

## 🛠️ **Technologies Used**
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Models**: Integrated with Qwen and Mem0.ai APIs
- **Workflow**: Reflection Workflow for iterative code refinement
- **Code Execution**: Powered by **E2B** for seamless and secure execution
- **Hosting**: Render

---

## 📝 **Usage**
1. **Code Input**: Paste the code snippet you want to modify.
2. **Modification Request**: Describe the changes you'd like to see.
3. **Final Code**: View the AI-generated code in the output section.
4. **Execution**: Run the modified code in real-time, securely powered by **E2B**, and view the results.

---

## 🧑‍💻 **Getting Started**

### Prerequisites
1. Python 3.11 or later.
2. `pip` installed.
3. `gunicorn` for deployment.

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/meAmitPatil/codmod.git
    ```
2. Navigate to the project directory:
    ```bash
    cd codmod
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Create a `.env` file in the root directory:
    ```plaintext
    MEM0_API_KEY=<your_mem0_api_key>
    E2B_API_KEY=<your_e2b_api_key>
    FIREWORKS_API_KEY=<your_fireworks_api_ke>
    ```
5. Run the application:
    ```bash
    python app.py
    ```

6. Visit the app at `http://127.0.0.1:5000` in your browser.

---

## 🛠️ **Deployment**
CodMod is hosted on Render. For deployment instructions, refer to [Render Documentation](https://render.com/docs).

---

## 🤝 **Contributing**
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add your message"
    ```
4. Push the branch:
    ```bash
    git push origin feature-branch-name
    ```
5. Open a Pull Request.

---

🎉 **Thank you for using CodMod!**
