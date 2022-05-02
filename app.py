from drinkify import app

if __name__ == '__main__':
    # to run from mobile add host = 'IPv4 address' to the arguments 
    app.run(debug=False, port='0.0.0.0')