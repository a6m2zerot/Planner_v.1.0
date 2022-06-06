from app import app
import os
app.run(debug=True)

if __name__ == "__main__":
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run("https://localhost")
