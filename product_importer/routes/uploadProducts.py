import os
from flask import Blueprint, request, make_response
from werkzeug.utils import secure_filename
from uploadFileTask import handle_file

from ..models import db,Products
import pandas as pd
#from uploadFileTask import handle_file
from multiprocessing.pool import ThreadPool as Pool
upload_products = Blueprint('upload',  __name__,
                        template_folder='templates')

t = Pool(processes=20)


@upload_products.route('/upload', methods=['POST'])
def upload():
    # Remember the paramName was set to 'file', we can use that here to grab it
    file = request.files['file']
    filename = secure_filename(file.filename)
    print(filename)
    # secure_filename makes sure the filename isn't unsafe to save
    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), secure_filename(file.filename))
    current_chunk = int(request.form['dzchunkindex'])
    print("chunck ",current_chunk)
    print("chunk total count",)
    if os.path.exists(save_path) and current_chunk == 0:
            os.remove(save_path)
    with open(save_path, 'ab') as f:
        # Goto the offset, aka after the chunks we already wrote
        f.seek(int(request.form['dzchunkbyteoffset']))
        data=file.stream.read()
        f.write(data)
    if current_chunk ==(int(request.form['dztotalchunkcount'])-1):
         #t1 = threading.Thread(target=store_data_in_db, args=(save_path,db))
         #t1.start()
         # t1.join()
         #store_data_in_db(save_path)
         # t.join()
         # t.close()
         #handle_file.send(save_path)
         handle_file(save_path)
    return make_response(('Chunk', 200))

def handle_file(save_path):
    f = get_next_record(save_path)
    for i in f:
        t.map(store_in_db, (i,))

def get_next_record(file):
    df = pd.read_csv(file, sep=',')
    print(df.head(5))
    df=df.drop_duplicates(subset='sku', keep='first')
    inc=j=int(df.shape[0]/100)
    i=0
    for _ in range(100):
        yield df[i:j]
        i+=inc
        j+=inc

def store_in_db(dataset):
    products=[]
    #dataset.drop_duplicates(subset='sku', keep="last")
    for index, data in dataset.iterrows():
        products.append(Products(name=data[0], sku=data[1], description=data[2]))
        #db.session.merge(record)
    try:
        db.session.bulk_save_objects(products)
        db.session.commit()
    except Exception as e:
        print(e)




def store_data_in_db(file,db):
    Products.query.delete()
    db.session.commit()
    import pandas as pd
    df = pd.read_csv(file, sep=',', header=None)
    try:
          for index, row in df.iterrows():
                 record = Products(name=row[0], sku=row[1], description=row[2])
                 db.session.merge(record)
    except Exception as e :
                 print(e)
    db.session.commit()







