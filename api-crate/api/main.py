import jwt
from functools import wraps
from flask_cors import CORS
from models.device import Device
import database.mongo as dbase_mongo
import database.crate as dbase_crate
from datetime import datetime, timedelta
from flask import Flask, jsonify, request, make_response


db_crate = dbase_crate.dbConnection()
cursor = db_crate.cursor()

app = Flask(__name__)
app.config['SECRET_KEY']= 'thisisthesecretkey'
app.config.from_object(__name__)
# apply CORS headers to all responses
CORS(app)


def token_required(f):
    """
    Decorator to require JWT token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == 'OPTIONS':
            return jsonify({}), 204
        
        if 'Authorization' not in request.headers or not request.headers['Authorization'].startswith('Bearer '):
            return jsonify({'error': 'Missing authorization header'}), 401
    
        token = request.headers['Authorization'].split(' ')[1]
        try:
            payload = jwt.decode(token,
                             app.config['SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Invalid token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as ex:
            print(ex)
            return jsonify({'error': 'Invalid token'}), 401
        return f(*args, **kwargs)

    return decorated

@app.route('/identity/v0.1/auth/tokens')
def login():
    host = request.host
    
    if host:
        token = jwt.encode({'host' : host, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return make_response(jsonify({'token' : token.decode("utf-8")}), 201)
    
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

@app.route('/', methods=['GET'])
def goToSwagger():
    return 'Please, use swagger to test the API', 201

@app.route('/lastState/v0.2/<string:org>/<string:dev>', methods=['GET'])
@token_required
def getLastState(org, dev):
    query = f"SELECT * FROM mt{org}.et{dev} ORDER BY time_index DESC LIMIT 1"
    cursor.execute(query)
    data = cursor.fetchone()
    if data:
        # Get the column names from the cursor description
        column_names = [column[0] for column in cursor.description]
        # Create a dictionary to store the fetched data with column names as keys
        data_dict = {column_names[i]: data[i] for i in range(len(column_names))}

    if data_dict:
        return jsonify(data_dict), 200
    else:
        return 'Content-Type not supported!'
    
@app.route('/allStates/v0.2/<string:org>/<string:dev>', methods=['GET'])
@token_required
def getAllStates(org, dev):
    query = f"SELECT * FROM mt{org}.et{dev}"
    cursor.execute(query)
    data = cursor.fetchall()
    if data:
        # Get the column names from the cursor description
        column_names = [column[0] for column in cursor.description]
        
        # Create a list of dictionaries to store the fetched data with column names as keys
        data_list = []
        for row in data:
            data_dict = {column_names[i]: row[i] for i in range(len(column_names))}
            data_list.append(data_dict)
    
    if data_list:
        return jsonify(data_list), 200
    else:
        return 'Content-Type not supported!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
