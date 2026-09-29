# 🤖 Daily Orders AI Backend [![Platform](https://img.shields.io/badge/Platform-Cloud-blue.svg)](https://render.com) [![Python Version](https://img.shields.io/badge/Python-3.12.10%2B-green.svg)](https://python.org) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A **FastAPI backend** that provides AI-powered processing services for the **[Daily Orders AI Process](https://github.com/AmmarAlhashemi/Daily-Orders-AI-Process)** desktop application.

The backend securely handles Google Gemini API communication and exposes structured HTTP endpoints for order parsing and intelligent transaction splitting.

------------------------------------------------------------------------

## 🔗 Related Project

**Desktop Application:** `[https://github.com/AmmarAlhashemi/Daily-Orders-AI-Process]`

------------------------------------------------------------------------

## 🌟 Features

- **AI Order Parsing:** Converts unstructured daily order text into structured transaction data.
- **Smart Transaction Splitting:** Uses predefined business rules and Gemini AI to distribute transactions between `ENTITY_A` and `ENTITY_B`.
- **Primary & Fallback Models:** Supports a primary Gemini model with a fallback model when required.
- **Structured API Responses:** Uses Pydantic schemas for validated request and response data.
- **Secure API Key Handling:** Gemini credentials are loaded through environment variables and are never included in the source code.

------------------------------------------------------------------------

## 🏗️ Architecture

```text
Desktop Application
        │
        │ HTTP / HTTPS
        ▼
   FastAPI Backend
        │
        ▼
   Google Gemini API

------------------------------------------------------------------------

The backend is maintained as a separate repository from the Desktop application and is deployed independently on Render.

---

## 🛠️ Tech Stack

- Python 3.12.10
- FastAPI
- Uvicorn
- Pydantic
- Google GenAI SDK
- Python Dotenv

---

## 📡 API Endpoints

### `GET /`

Health check endpoint used to verify that the backend is running.

### `POST /parse-orders`

Processes unstructured daily order text and returns structured transaction data.

### `POST /smart-split`

Processes transaction data and returns the serial numbers that should be removed from each entity's ledger.

---

## 📝 License

This project is licensed under the MIT License.

See the [`LICENSE`](LICENSE) file for details.