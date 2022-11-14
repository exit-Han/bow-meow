import app

if __name__ == '__main__':
    app.create_env().run('0.0.0.0', port=5000, debug=True)