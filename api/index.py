from http.server import BaseHTTPRequestHandler
import os
import sys
import telebot
import logging

# Add the parent directory to path so we can import bot.py from the root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot import bot  # Imports the bot instance from bot.py

# --- CONFIGURATION ---
DEBUG_MODE = os.environ.get("DEBUG_LOGS", "False").lower() == "true"

# Set logging level: DEBUG if enabled, else INFO (Clean logs)
telebot.logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

# CRITICAL: Enforce synchronous execution for Vercel
bot.threaded = False

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write("Bot is running!".encode('utf-8'))

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            json_string = post_data.decode('utf-8')

            # Conditional Debug Logging
            if DEBUG_MODE:
                print(f"HEADERS: {self.headers}", file=sys.stderr)
                print(f"CONTENT_LENGTH: {content_length}", file=sys.stderr)
                print(f"RAW BODY: {json_string}", file=sys.stderr)

            update = telebot.types.Update.de_json(json_string)

            if DEBUG_MODE:
                print(f"PARSED UPDATE: {update}", file=sys.stderr)
                print("STARTING process_new_updates...", file=sys.stderr)

            # Synchronous processing
            bot.process_new_updates([update])

            if DEBUG_MODE:
                print("FINISHED process_new_updates", file=sys.stderr)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("OK".encode('utf-8'))

        except Exception as e:
            # Always log actual crashes to stderr
            print(f"Error processing update: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write("Error handled".encode('utf-8'))
