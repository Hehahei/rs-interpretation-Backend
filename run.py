from app import app
from config import PORT

app.run(host='0.0.0.0', port=PORT, debug=False)