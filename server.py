from flask import Flask, jsonify, request
from db import read_files_db, open_db
from cmd_arguments import args



# Run the app
def start_server():
    # function: start_server

    # purpose: Starts the REST API Server

    # inputs: 

    # returns:

    app = Flask(__name__)

    # Welcome route
    @app.route('/')
    def index():
        return "Welcome to the User API!"

    @app.route('/files', methods=['GET'])
    def get_files():
        conn = open_db()
        files = read_files_db(conn)
        if files is None:
            return jsonify({"error": "Unable to retrieve files"}), 500  # Return 500 if there's an error
        return jsonify(files)
        
    app.run(debug=args.debug, port=int(args.port))
