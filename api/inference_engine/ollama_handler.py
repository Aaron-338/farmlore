import logging
import time
import json
import os
import string # Added for string.printable
import threading
import requests
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, wait_fixed

# ... existing code ...

        try:
            # Ensure the modelfiles directory exists
            modelfile_dir = os.path.dirname(modelfile_path)
            if not os.path.exists(modelfile_dir):
                logger.error(f"OllamaHandler: Modelfile directory does not exist: {modelfile_dir}")
                return False, f"Modelfile directory not found: {modelfile_dir}"

            if not os.path.exists(modelfile_path):
                logger.error(f"OllamaHandler: Modelfile does not exist: {modelfile_path}")
                return False, f"Modelfile not found: {modelfile_path}"

            with open(modelfile_path, 'r', encoding='utf-8') as f:
                modelfile_content_raw = f.read()
            logger.info(f"OllamaHandler: Modelfile {model_name} raw length: {len(modelfile_content_raw)}")

            # --- Start Refactored Cleaning Logic ---
            # 1. Normalize line endings consistently to \n
            current_content = modelfile_content_raw.replace('\r\n', '\n').replace('\r', '\n')
            logger.debug(f"OllamaHandler [{model_name}]: Content after newline normalization (first 300 chars): {current_content[:300]}")
            logger.debug(f"OllamaHandler [{model_name}]: Contains '\\n': {'\n' in current_content}")

            # 2. Remove UTF-8 BOM if present (from the beginning of the content)
            if current_content.startswith('\ufeff'):
                current_content = current_content.lstrip('\ufeff')
                logger.info(f"OllamaHandler: Modelfile {model_name} had UTF-8 BOM removed.")
            
            lines = current_content.split('\n')
            logger.debug(f"OllamaHandler [{model_name}]: Lines after split (first 5 lines): {lines[:5]}")
            logger.debug(f"OllamaHandler [{model_name}]: Number of lines after split: {len(lines)}")
            processed_lines = []
            
            for idx, line in enumerate(lines):
                original_line_for_debug = line
                clean_line_chars = []
                for char_val in [ord(c) for c in line]:
                    if char_val == 9:  # Tab
                        clean_line_chars.append('\t')
                    elif 32 <= char_val <= 126:  # Printable ASCII
                        clean_line_chars.append(chr(char_val))
                    # Other characters (including control chars other than Tab, LF, CR) are dropped from the line
                cleaned_line_for_debug = "".join(clean_line_chars)
                if original_line_for_debug != cleaned_line_for_debug:
                    logger.debug(f"OllamaHandler [{model_name}]: Line {idx} changed by cleaning. From: '{original_line_for_debug}' To: '{cleaned_line_for_debug}'")
                processed_lines.append(cleaned_line_for_debug)
            
            logger.debug(f"OllamaHandler [{model_name}]: Processed lines before join (first 5 lines): {processed_lines[:5]}")
            payload_modelfile_content = "\n".join(processed_lines)
            logger.debug(f"OllamaHandler [{model_name}]: Content after join (first 300 chars): {payload_modelfile_content[:300]}")
            
            # --- Defensive newline insertion before major keywords ---
            keywords = ["PARAMETER", "TEMPLATE", "SYSTEM", "LICENSE", "MESSAGE", "ADAPTER"]
            temp_lines = payload_modelfile_content.split('\n')
            processed_temp_lines = []
            for line in temp_lines:
                # Check if the line starts with "FROM" and also contains another keyword without a preceding newline
                # This specifically targets the "FROM ...KEYWORD" case
                if line.startswith("FROM "):
                    processed_line = line
                    for kw in keywords:
                        # Find "KEYWORD" not preceded by a newline, but possibly after "FROM "
                        # Only add newline if it's not "FROM KEYWORD" but "FROM ... KEYWORD"
                        # And make sure we're not splitting "FROM" itself if a model name contains a keyword.
                        # A simple heuristic: if a keyword is found after "FROM model_name"
                        from_part_length = len(line.split(' ')[0]) + 1 + len(line.split(' ')[1]) # "FROM model_name "
                        if kw in processed_line[from_part_length:] and f"\n{kw}" not in processed_line:
                             # Replace only the first occurrence after the model name to avoid issues with keyword in content
                            kw_index = processed_line[from_part_length:].find(kw)
                            if kw_index != -1:
                                actual_kw_index = from_part_length + kw_index
                                processed_line = processed_line[:actual_kw_index] + '\n' + processed_line[actual_kw_index:]
                    processed_temp_lines.append(processed_line)
                else:
                    processed_temp_lines.append(line)
            payload_modelfile_content = "\n".join(processed_temp_lines)

            # Ensure other keywords also start on a new line if they got merged.
            # This is a broader attempt to fix merged lines.
            for kw in keywords:
                payload_modelfile_content = payload_modelfile_content.replace(f" {kw}", f"\n{kw}") # common case like "...latest SYSTEM"
                payload_modelfile_content = payload_modelfile_content.replace(f"\t{kw}", f"\n{kw}") # In case it was tab-merged

            logger.info(f"OllamaHandler [{model_name}]: Content after defensive newline insertion (first 300 chars): {payload_modelfile_content[:300]}")
            # --- End defensive newline insertion ---

            final_cleaned_length = len(payload_modelfile_content)

            if len(modelfile_content_raw) != final_cleaned_length:
                 logger.info(
                    f"OllamaHandler: Modelfile {model_name} content transformed. "
                    f"Raw length: {len(modelfile_content_raw)}, Final cleaned length for payload: {final_cleaned_length}"
                )
            else:
                logger.info(f"OllamaHandler: Modelfile {model_name} content length unchanged after cleaning: {final_cleaned_length}")
            
            logger.info(f"OllamaHandler: Modelfile {model_name} length after normalization/strip: {len(payload_modelfile_content)}")

            payload = {
                "name": model_name,
                "modelfile": payload_modelfile_content,
                "stream": True 
            }
            logger.info(f"OllamaHandler: Full create_payload for {model_name}:\n{json.dumps(payload, indent=2)}")

            timeout = httpx.Timeout(self.MODEL_CREATION_STREAM_TIMEOUT_SECONDS, connect=self.DEFAULT_REQUEST_TIMEOUT_SECONDS)
# ... existing code ...