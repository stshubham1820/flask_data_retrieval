from . import app, db
from .models import Cat
from flask import jsonify,request
from .tasks import fetch_and_store_data


'''

get_processed_data will bring the data available in Cat Table with pagination per page will have 10 data

'''
@app.route('/api/v1/get-processed-data', methods=['GET'])
def get_processed_data():
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated_cats = Cat.query.paginate(page=page, per_page=per_page, error_out=False)

    
    result = [
        {
            'id': cat.id,
            'weight': cat.weight,
            'name': cat.name,
            'description': cat.description,
            'origin': cat.origin,
            'life_span': cat.life_span,
            'intelligence': cat.intelligence
        } for cat in paginated_cats.items
    ]

    response = {
        'data': result,
        'total': paginated_cats.total,
        'pages': paginated_cats.pages,
        'current_page': paginated_cats.page,
        'per_page': paginated_cats.per_page,
        'has_next': paginated_cats.has_next,
        'has_prev': paginated_cats.has_prev
    }

    return jsonify(response), 200

'''

Home Page Route

'''

@app.route('/', methods=['GET'])
def home_page():
    url_available_are = ['get : /api/v1/get-processed-data','post : /api/v1/store_data']
    data = {'Available Routes : ':url_available_are}
    return jsonify(data), 200

@app.route('/create_db', methods=['GET'])
def create_db():
    db.create_all()
    return jsonify('DB Created'), 200

'''

store_data will call fetch_and_store_data function that will asynchronously store the data 

for more details follow tasks.py

'''

@app.route('/api/v1/store_data',methods=['GET'])
def store_data():
    fetch_and_store_data.delay()
    return jsonify('Data Creation is Asynchronously Started'), 200
