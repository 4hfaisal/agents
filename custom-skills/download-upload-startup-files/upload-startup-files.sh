#!/bin/bash

# Upload Startup Files with Timestamped Folders
# Automates downloading from Google Drive and uploading to timestamped folders in Dropbox

set -euo pipefail

# Configuration
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TIMESTAMP_FOLDER="Startup_Documents_${TIMESTAMP}"
DROPBOX_SHARED_PATH="/Kodee_share"

# Startup companies and their file mappings
declare -A STARTUP_FILES=(
    ["Genoome"]="genoome_pitch_deck.pdf genoome_application_form.pdf"
    ["Ananas"]="anas_pitch_deck.pdf anas_application_form.pdf"
    ["CashOver"]="cashover_pitch_deck.pdf cashover_application_form.pdf"
    ["Ogold"]="ogold_pitch_deck.pdf ogold_application_form.pdf"
)

# Google Drive file IDs (replace with actual IDs)
declare -A GOOGLE_DRIVE_IDS=(
    ["genoome_pitch_deck.pdf"]="google_drive_file_id_1"
    ["genoome_application_form.pdf"]="google_drive_file_id_2"
    ["anas_pitch_deck.pdf"]="google_drive_file_id_3"
    ["anas_application_form.pdf"]="google_drive_file_id_4"
    ["cashover_pitch_deck.pdf"]="google_drive_file_id_5"
    ["cashover_application_form.pdf"]="google_drive_file_id_6"
    ["ogold_pitch_deck.pdf"]="google_drive_file_id_7"
    ["ogold_application_form.pdf"]="google_drive_file_id_8"
)

echo "🚀 Starting startup files upload process"
echo "📁 Timestamp folder: ${TIMESTAMP_FOLDER}"
echo "📂 Dropbox target: ${DROPBOX_SHARED_PATH}"
echo ""

# Create temporary directory for downloads
TEMP_DIR="/tmp/startup_files_${TIMESTAMP}"
mkdir -p "${TEMP_DIR}"
cd "${TEMP_DIR}"

echo "📥 Downloading files from Google Drive..."

# Download all files
for startup_name in "${!STARTUP_FILES[@]}"; do
    files=${STARTUP_FILES[$startup_name]}
    
    for file in $files; do
        file_id=${GOOGLE_DRIVE_IDS[$file]}
        if [ -n "$file_id" ]; then
            echo "⬇️  Downloading ${file} (${file_id})"
            
            # Download file from Google Drive
            composio execute GOOGLE_DRIVE_DOWNLOAD_FILE -d "{\"file_id\": \"${file_id}\", \"local_path\": \"${file}\"}"
            
            if [ -f "${file}" ]; then
                echo "✅ Downloaded: ${file}"
            else
                echo "❌ Failed to download: ${file}"
                exit 1
            fi
        else
            echo "⚠️  No Google Drive ID found for: ${file}"
        fi
    done
done

echo ""
echo "📤 Uploading files to Dropbox..."

# Upload all files to timestamped folders
for startup_name in "${!STARTUP_FILES[@]}"; do
    files=${STARTUP_FILES[$startup_name]}
    
    echo "📁 Uploading files for ${startup_name}..."
    
    for file in $files; do
        if [ -f "${file}" ]; then
            dropbox_path="${DROPBOX_SHARED_PATH}/${TIMESTAMP_FOLDER}/${startup_name}/${file}"
            echo "⬆️  Uploading ${file} to ${dropbox_path}"
            
            # Upload file to Dropbox
            composio execute DROPBOX_UPLOAD_FILE --file "${file}" -d "{\"path\": \"${dropbox_path}\", \"mode\": \"overwrite\", \"autorename\": true}"
            
            echo "✅ Uploaded: ${file}"
        else
            echo "❌ File not found: ${file}"
        fi
    done
done

echo ""
echo "🎉 Upload completed successfully!"
echo "📊 Summary:"
echo "   - Timestamp: ${TIMESTAMP}"
echo "   - Folder: ${TIMESTAMP_FOLDER}"
echo "   - Location: ${DROPBOX_SHARED_PATH}"
echo "   - Files uploaded: $(find . -type f | wc -l)"
echo ""

# Cleanup
rm -rf "${TEMP_DIR}"

echo "🧹 Cleaned up temporary files"
echo "✅ Process completed at $(date)"