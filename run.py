from app import app

if __name__ == '__main__':
    print('Starting SDX Deliver')
    app.run(debug=True, host='0.0.0.0', port=5000)
