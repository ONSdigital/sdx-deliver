from app import app, load_config

if __name__ == '__main__':
    print('Starting SDX Deliver')
    load_config()
    app.run(debug=False, host='0.0.0.0', port=5000)
