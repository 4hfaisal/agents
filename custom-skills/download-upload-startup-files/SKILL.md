---
skill-kind: custom
owner: Faisal Al Homodi
created: 2026-04-26
last-updated: 2026-04-27
category: [productivity, automation, file-management]
---

# Download Startup Files from Google Drive & Upload to Dropbox

## Description
This skill automates the process of downloading startup documents from Google Drive and uploading them directly to a timestamped folder in a shared Dropbox folder. It handles the complete workflow from Google Drive access to Dropbox upload with automatic timestamp-based organization.

## Prerequisites
- Google Drive access with read permissions
- Dropbox account with write permissions
- Composio CLI installed and configured

## Usage

### Manual Execution
```bash
# Run the complete workflow with timestamped folders
composio execute GOOGLE_DRIVE_DOWNLOAD_FILE -d '{"file_id": "<google_drive_file_id>", "local_path": "<local_filename>"}'
composio execute DROPBOX_UPLOAD_FILE --file "<local_filename>" -d '{"path": "/Kodee_share/Startup_Documents_$(date +%Y%m%d_%H%M%S)/<folder_name>/<filename>", "mode": "overwrite", "autorename": true}'
```

### Automated Script
```bash
# Use the provided automation script
./upload-startup-files.sh
```

The script automatically:
- Creates timestamped folders (format: Startup_Documents_YYYYMMDD_HHMMSS)
- Downloads all files from Google Drive
- Uploads directly to the shared Dropbox folder
- Organizes files by startup company
- Handles errors and provides detailed logging

## Steps

### 1. Download Files from Google Drive
Use Google Drive tools to download startup documents:
- Pitch decks
- Application forms
- Supporting documents

### 2. Upload Directly to Dropbox Shared Folder
Upload files directly to timestamped folders in the shared Dropbox:
```
/Kodee_share/
└── Startup_Documents_20260427_103000/  # Timestamped folder
    ├── Genoome/
    │   ├── genoome_pitch_deck.pdf
    │   └── genoome_application_form.pdf
    ├── Ananas/
    │   ├── anas_pitch_deck.pdf
    │   └── anas_application_form.pdf
    ├── CashOver/
    │   ├── cashover_pitch_deck.pdf
    │   └── cashover_application_form.pdf
    └── Ogold/
        ├── ogold_pitch_deck.pdf
        ├── ogold_application_form.pdf
```

### 3. Timestamp Folder Generation
Each upload creates a new timestamped folder using the format:
```bash
TIMESTAMP_FOLDER="Startup_Documents_$(date +%Y%m%d_%H%M%S)"
```

This ensures each batch of uploads gets its own unique folder, preventing conflicts and maintaining clear version history.

## Required Tools
- `GOOGLE_DRIVE_DOWNLOAD_FILE`
- `DROPBOX_UPLOAD_FILE`
- `DROPBOX_CREATE_FOLDER`
- `DROPBOX_LIST_FOLDERS`

## Configuration
Ensure these environment variables are set:
- `GOOGLE_DRIVE_FOLDER_ID`: Root folder containing startup documents
- `DROPBOX_SHARED_FOLDER_PATH`: Target shared folder path (e.g., "/Kodee_share")
- `TIMESTAMP_FORMAT`: Optional custom timestamp format (default: %Y%m%d_%H%M%S)

## Error Handling
- Checks file existence before operations
- Validates folder permissions in shared Dropbox
- Handles upload conflicts with overwrite mode
- Auto-creates timestamped folders as needed
- Provides detailed error reporting
- Validates shared folder access permissions

## Complete Workflow Example

```bash
#!/bin/bash

# Set timestamp for this batch
export TIMESTAMP=$(date +%Y%m%d_%H%M%S)
export TIMESTAMP_FOLDER="Startup_Documents_${TIMESTAMP}"

# Download files from Google Drive
composio execute GOOGLE_DRIVE_DOWNLOAD_FILE -d '{
  "file_id": "google_drive_file_id_1",
  "local_path": "genoome_pitch_deck.pdf"
}'

composio execute GOOGLE_DRIVE_DOWNLOAD_FILE -d '{
  "file_id": "google_drive_file_id_2", 
  "local_path": "genoome_application_form.pdf"
}'

# Upload directly to timestamped shared folder
composio execute DROPBOX_UPLOAD_FILE --file "genoome_pitch_deck.pdf" -d '{
  "path": "/Kodee_share/${TIMESTAMP_FOLDER}/Genoome/genoome_pitch_deck.pdf",
  "mode": "overwrite",
  "autorename": true
}'

composio execute DROPBOX_UPLOAD_FILE --file "genoome_application_form.pdf" -d '{
  "path": "/Kodee_share/${TIMESTAMP_FOLDER}/Genoome/genoome_application_form.pdf",
  "mode": "overwrite",
  "autorename": true
}'
```

## Logging
All operations are logged with timestamps and success/failure status for audit purposes. Each batch gets its own timestamped folder for clear version tracking.