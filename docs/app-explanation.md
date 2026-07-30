# AfyaFlow Pwani App Explanation

## 1. The Challenge AfyaFlow Pwani Solves

Primary and community health centres often report medicine and diagnostic-test stock levels through paper stock cards, short WhatsApp messages, phone calls, photographs, or voice notes. These reports are usually unstructured, sometimes multilingual, and often delayed before they reach supply-chain administrators.

The result is a dangerous operational gap:

- A facility may be almost out of ORS, malaria rapid diagnostic tests, or antibiotics.
- The shortage may not be visible to administrators until patients are already affected.
- Nearby facilities may have enough stock to support a transfer, but there is no fast way to identify safe redistribution options.
- Manual follow-up is slow, inconsistent, and hard to audit.

AfyaFlow Pwani solves this by turning unstructured facility reports into verified stock records, early stock-out warnings, transfer recommendations, bilingual handoff messages, and an audit trail.

The app focuses on one reliable competition workflow: from facility report to confirmed inventory alert.

## 2. What the App Does

AfyaFlow Pwani is a Streamlit demo application for health supply-chain triage. It lets a user submit a stock report, validates the extracted information, calculates risk, recommends transfer options, and prepares an administrator handoff message.

The app demonstrates these capabilities:

1. Multisource facility input
   - Text reports typed or pasted directly into the app.
   - Image uploads from the user's device, such as photographed stock cards.
   - Audio uploads from the user's device, such as short voice stock reports.

2. Structured extraction
   - The app converts unstructured input into a normalized stock report.
   - In local/offline mode, it uses deterministic fallback extraction.
   - In Kaggle GPU mode, the same boundary can be connected to a real Gemma runtime.

3. Human confirmation
   - Extracted fields are shown in editable form fields.
   - A human can inspect and correct the report before operational action.

4. Deterministic risk calculation
   - The app calculates days of stock using stock balance and average daily use.
   - It adjusts risk when patient footfall indicates higher demand.
   - It classifies stock status as green, amber, or red.

5. Transfer recommendation
   - The app checks synthetic nearby facility inventory.
   - It recommends transfer options only when the donor facility can retain a safety buffer.

6. Bilingual handoff message
   - The app drafts an administrator handoff in English or Swahili.
   - This supports realistic communication in coastal Kenya health workflows.

7. Audit event preview
   - The app shows the event that would be written to the audit log.
   - This supports transparency and accountability before inventory action.

## 3. Main User Roles

### Health Worker

The health worker is the person reporting the stock situation from a PHC or CHC. They may submit:

- a typed stock report;
- a photographed stock card;
- a short voice report;
- a mixed English/Swahili message.

### Supply-Chain Administrator

The administrator reviews the extracted report, confirms the fields, checks the risk level, reviews transfer options, and sends or acts on the handoff message.

### Judge or Demo Viewer

The judge watches the app prove the full workflow:

1. unstructured report goes in;
2. structured stock report comes out;
3. deterministic code calculates risk;
4. the system recommends a safe next action;
5. the app keeps human confirmation and auditability in the loop.

## 4. User Interaction Flow

### Step 1: Open the App

The user runs the Streamlit app. The page opens with the title AfyaFlow Pwani and a short caption describing the goal: turning stock reports into early warnings and redistribution actions.

### Step 2: Choose Demo Controls

In the sidebar, the user selects:

- a synthetic scenario;
- the handoff language, either English or Swahili.

The synthetic scenario preloads a safe public example. This keeps the demo reproducible and avoids real patient or facility data.

### Step 3: Choose Source Type

The user chooses one source type:

1. text;
2. image;
3. audio.

Each source type changes the input controls shown by the app.

### Step 4A: Text Input Flow

If the user selects text:

1. The app shows a text area.
2. The user pastes or edits a stock report.
3. The text is passed into the extraction workflow.

Example report:

```text
Old Town Health Centre reports ORS sachets balance is 18 units. Average daily use is 9 units. Patient footfall is high today.
```

### Step 4B: Image Input Flow

If the user selects image:

1. The app shows an image uploader.
2. The user uploads a photographed stock card or facility report from their device.
3. The app previews the uploaded image.
4. The user types what is visible on the image or pastes OCR/Gemma vision text.
5. The app sends image metadata plus readable stock-report text into the workflow.

This design supports the current public demo while keeping the system ready for a real multimodal Gemma runtime. In local fallback mode, the extractor still needs readable text. In the real model path, image understanding can replace the typed visible-text hint.

### Step 4C: Audio Input Flow

If the user selects audio:

1. The app shows an audio uploader.
2. The user uploads a voice stock report from their device.
3. The app previews the audio so the user can play it.
4. The user types the transcript or pastes speech-to-text output.
5. The app sends audio metadata plus spoken stock-report transcript into the workflow.

This keeps the current demo reliable while making the user interaction realistic. A real audio-capable runtime can later replace the typed transcript with direct audio transcription or multimodal extraction.

### Step 5: Generate Verified Stock Alert

The user clicks Generate verified stock alert.

The app then runs the full workflow:

1. extract a stock report;
2. load synthetic facility inventory;
3. calculate stock-out risk;
4. rank safe transfer options;
5. draft a handoff message;
6. prepare an audit event.

### Step 6: Review Human-Confirmed Fields

The app displays editable fields:

- facility;
- item;
- balance units;
- average daily use;
- source language;
- extraction confidence.

This is the human-in-the-loop safety step. The app does not present model output as automatically final; a user must be able to inspect and correct it.

### Step 7: Review Risk and Transfer Action

The app shows:

- risk level;
- days of stock;
- adjusted daily use;
- reason for the classification;
- recommended transfer options if safe options exist.

Risk levels mean:

- green: stock is currently safe;
- amber: stock needs attention soon;
- red: stock-out risk is urgent.

### Step 8: Review Administrator Handoff

The app drafts a message in the selected language. This message is meant for an administrator or supply-chain coordinator who needs to act quickly.

The handoff summarizes:

- facility;
- item;
- risk level;
- recommended next step.

### Step 9: Review Audit Event

The audit preview shows the structured record of what happened. This helps prove that AfyaFlow is designed for accountable workflows, not hidden model decisions.

## 5. Data Flow From Start to Finish

The full data flow is:

```text
User input
  -> source type selection
  -> text / image / audio collection
  -> raw workflow input
  -> GemmaClient extraction boundary
  -> StockReport schema validation
  -> synthetic facility inventory lookup
  -> deterministic risk calculation
  -> safe transfer ranking
  -> bilingual handoff message
  -> audit event preview / audit log
  -> user-facing result
```

### 5.1 Input Collection

The Streamlit app collects the user input depending on source type.

- Text input is collected directly from a text area.
- Image input is collected through a file uploader, previewed, and paired with visible stock-card text.
- Audio input is collected through a file uploader, previewed, and paired with a transcript.

### 5.2 Extraction Boundary

The collected input is passed into the workflow as raw input plus source type.

The extraction boundary is important because it separates model understanding from operational decision-making.

- Gemma or fallback extraction reads the unstructured report.
- It returns a structured stock-report payload.
- The payload must match the expected report schema.

### 5.3 Schema Validation

The structured report is validated into a stock report object. Required fields include:

- facility;
- item;
- balance units;
- average daily use;
- report date;
- source type;
- source language;
- confidence;
- optional patient footfall;
- notes.

If required fields are missing or invalid, extraction fails safely instead of producing a misleading alert.

### 5.4 Inventory Loading

The app loads synthetic inventory records. These represent nearby PHC/CHC facilities and available stock levels.

The public project uses synthetic data only. This protects privacy and makes the demo reproducible for judges.

### 5.5 Risk Calculation

The risk engine calculates how many days the current stock will last:

```text
days of stock = balance units / adjusted daily use
```

The engine can adjust daily use when patient footfall suggests a demand spike.

Then it assigns a risk band:

- red for urgent stock-out risk;
- amber for near-term concern;
- green for stable stock.

### 5.6 Transfer Ranking

If a facility is at risk, the app checks whether another synthetic facility can safely transfer stock.

A transfer option is only recommended if the donor facility can keep enough stock after the transfer. This avoids solving one stock-out by creating another.

### 5.7 Handoff Generation

The tool registry drafts a handoff message in English or Swahili. This message is designed to be understandable and actionable for a supply-chain administrator.

### 5.8 Audit Trail

The app prepares an audit event that includes:

- model name;
- source type;
- extracted report;
- risk result;
- handoff message.

This supports traceability and makes the workflow easier to review.

## 6. Feature-by-Feature Summary

| Feature | What it does | Why it matters |
|---|---|---|
| Synthetic scenario selector | Loads safe example stock reports | Keeps the demo reproducible |
| Handoff language selector | Chooses English or Swahili | Supports local communication |
| Source type selector | Allows text, image, or audio input | Matches real facility reporting channels |
| Text input | Accepts typed/pasted reports | Fastest report path |
| Image upload | Accepts stock-card/report photos | Demonstrates device-based image reporting |
| Audio upload | Accepts short voice reports | Demonstrates voice-note reporting |
| Extraction workflow | Converts unstructured input to structured fields | Makes messy reports usable |
| Human-confirmed fields | Lets a user inspect/edit extracted values | Prevents blind automation |
| Risk metrics | Shows risk level, days of stock, adjusted use | Explains urgency clearly |
| Transfer table | Ranks safe donor facilities | Supports practical redistribution |
| Handoff message | Drafts administrator communication | Speeds up action |
| Audit preview | Shows the structured workflow record | Supports accountability |

## 7. Safety and Responsible AI Design

AfyaFlow Pwani is intentionally designed so the model does not control the whole workflow.

Gemma or fallback extraction handles the messy input-understanding step. Deterministic application code handles stock arithmetic, risk thresholds, transfer rules, approved tool execution, and audit logging.

This matters because health supply-chain decisions must be explainable, reviewable, and safe.

Key safety principles:

- No real patient data is used in the public demo.
- Human confirmation is required before operational action.
- Risk calculation is deterministic and testable.
- Tool execution is constrained to approved actions.
- Audit records make decisions traceable.
- Prototype thresholds are assumptions, not official policy.

## 8. What Judges Should Notice

Judges should see that AfyaFlow Pwani is not just a chatbot. It is a controlled workflow where Gemma helps with unstructured extraction, while the application enforces validation, deterministic calculations, safety boundaries, and clear next actions.

The strongest competition story is:

1. the problem is real and operationally important;
2. the workflow is narrow but complete;
3. Gemma is used where it adds value;
4. deterministic code controls high-stakes decisions;
5. the demo is reproducible with synthetic data;
6. the app is practical for frontline reporting contexts.

## 9. Current Limitations

The current public demo supports user-device image and audio upload, but the local fallback extractor still needs readable text or transcript hints. This keeps the demo reliable without requiring local model weights.

In the Kaggle GPU version, a real Gemma runtime can be connected behind the same extraction boundary to process richer multimodal input. The downstream safety workflow remains the same.

The current prototype is also limited to a small synthetic inventory and a focused medicine/test-kit stock workflow. It does not diagnose patients, prescribe treatment, manage clinician attendance, or use real facility credentials.

## 10. End-to-End Example

A typical user interaction looks like this:

1. A facility worker reports that ORS sachets are nearly out.
2. The user opens AfyaFlow Pwani.
3. The user selects a synthetic scenario or enters a new report.
4. The user chooses text, image, or audio.
5. The user uploads or types the report.
6. The app extracts structured stock fields.
7. The user reviews and confirms the extracted fields.
8. The risk engine classifies the report as red, amber, or green.
9. The app recommends a safe transfer option if available.
10. The app drafts a bilingual handoff message.
11. The audit preview records what happened.
12. The administrator has a clear, explainable action path.

This is the core value of AfyaFlow Pwani: turning scattered stock reports into timely, explainable supply-chain action.