# ReceiptFlow AI

ReceiptFlow AI is a privacy-first, offline-first receipt and invoice organizer for freelancers. Documents are processed by a **local FastAPI service** that calls **Ollama on your own machine**. The browser stores extracted records in IndexedDB; CSV export is generated locally.

## Privacy model
- Uploaded documents are sent only to `localhost` FastAPI, not to a hosted service.
- FastAPI extracts PDF text locally and sends text to Ollama. For image receipts, it can send the image to a local vision model configured in `.env`.
- Expense metadata is stored in the browser's IndexedDB database.
- No analytics, advertising SDK, account system, or cloud database is included.
- This is a local-first app, not a security certification. Keep your OS account encrypted, secure local backups, and verify model outputs before using them for tax filing.

## Stack
- React + Vite + TypeScript
- Tailwind CSS, Lucide React, Framer Motion
- IndexedDB via `idb`
- FastAPI, PyMuPDF, Pillow, Ollama local HTTP API

## Requirements
- Node.js 20+
- Python 3.11+
- [Ollama](https://ollama.com/download)
- A model available locally in Ollama. Example text model: `ollama pull gemma2:2b`.
- For image understanding, pull a vision model supported by Ollama, e.g. `ollama pull llava:7b` (hardware requirements vary).

## Run locally

### 1. Start Ollama
Install Ollama, then:
```bash
ollama serve
ollama pull gemma2:2b
```
Optional vision model:
```bash
ollama pull llava:7b
```

### 2. Start FastAPI
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
On macOS/Linux, use `cp .env.example .env` instead of `copy`.

### 3. Start the frontend
In a second terminal:
```bash
cd frontend
npm install
npm run dev
```
Open the local URL Vite prints (usually `http://localhost:5173`).

## Usage
1. Open the app and drop PDF, PNG, JPG, JPEG, or WEBP receipts into the upload area.
2. The browser posts each file to the local FastAPI service.
3. The backend extracts PDF text or passes image data to your configured local vision model, then asks Ollama for structured JSON.
4. Review and correct the vendor, date, category, tax, total, and line items before relying on them.
5. Search/filter the table, edit a record, delete records, or export the visible records to CSV.

## Configuration
Copy `backend/.env.example` to `backend/.env`:
- `OLLAMA_BASE_URL`: defaults to `http://127.0.0.1:11434`
- `OLLAMA_TEXT_MODEL`: defaults to `gemma2:2b`
- `OLLAMA_VISION_MODEL`: defaults to `llava:7b`
- `MAX_UPLOAD_MB`: maximum upload size
- `CORS_ORIGINS`: comma-separated allowed frontend origins

The app binds to loopback by default. Do not expose the backend or Ollama port to your LAN or the public internet unless you understand the security implications.

## Troubleshooting
- **Backend unavailable:** verify `uvicorn` is running at `127.0.0.1:8000`.
- **Ollama unavailable:** run `ollama serve` and check `http://127.0.0.1:11434/api/tags`.
- **Model missing:** run `ollama pull <model-name>` and ensure `.env` matches the pulled model.
- **Poor extraction:** use a stronger model, improve scan quality, or manually correct the record. OCR/model accuracy is not guaranteed.
- **Scanned PDF:** this starter extracts embedded PDF text. For image-only/scanned PDFs, add local OCR (such as Tesseract) or convert pages to images and use the vision path.

## Testing and feedback integration
There is no remote telemetry. To collect feedback while preserving privacy:
1. Ask testers to use synthetic or redacted receipts.
2. Gather feedback manually through an issue template or local notes; do not ask them to upload real financial documents.
3. Record model name, OS, error text, and whether the extraction was wrong—never the receipt itself.
4. Prioritize recurring extraction failures, category confusion, keyboard accessibility, and CSV compatibility.
5. Add automated tests for each regression before changing prompts or parsing logic.

## Development commands
```bash
# frontend
npm run dev
npm run build
# backend (from backend/)
pytest
```

## Important limitation
This is a local application scaffold intended to run on the user's machine. Do not deploy the backend to a cloud host if your promise is that documents never leave the device. A public static frontend can be hosted separately, but local mode should still target a user-controlled local backend and clearly show connection status.
