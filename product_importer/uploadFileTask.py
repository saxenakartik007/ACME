import dramatiq
from multiprocessing.pool import ThreadPool as Pool
import pandas as pd
from .models import Products,db
from dramatiq.brokers.redis import RedisBroker
broker = RedisBroker()
dramatiq.set_broker(broker)

t = Pool(processes=20)

@dramatiq.actor
def handle_file(save_path):
    print("called ",save_path)
    f = get_next_record(save_path)
    for i in f:
        t.map(store_in_db, (i,))
    return None



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
    from product_importer.models import Products, db
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
    db.session.query(Products).delete()
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