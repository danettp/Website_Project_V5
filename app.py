from website import create_app

if __name__ == "__main__":
    app = create_app()  # Create a Flask application instance using the create_app function
    app.run(debug=True) # Run the Flask application in debug mode

# Adding avatar image/account page 4 24:48