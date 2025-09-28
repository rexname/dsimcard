from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    app.run(host=os.getenv('HOST', '0.0.0.0'), port=int(os.getenv('PORT', 8804)), debug=bool(int(os.getenv('FLASK_DEBUG', 1))))
