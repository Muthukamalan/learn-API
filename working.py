from fastapi import FastAPI,Path,Query
from typing import Optional
from pydantic import BaseModel,validator
from datetime import datetime


app = FastAPI()

inventory={
    1:{
        "model":"linear",
        "accuracy":"50.0",
        "version":"1.0.0",
        "date": "2020-02-12",
    },
    2:{
        "model":"logistic",
        "accuracy":"49.0",
        "version":"1.0.0",
        "date":  "2020-03-02",
    },
    3:{
        "model":"ensemble",
        "accuracy":"89.0",
        "version":"1.0.0",
        "date":  "2021-06-22",
    },
    4:{
        "model":"deeplearning",
        "accuracy":"98.0",
        "version":"1.0.0",
        "date":  "2022-04-16",
    },
    5:{
        "model":"linear",
        "accuracy":"67.0",
        "version":"1.0.1",
        "date": "2020-04-12",
    },
}


# http://127.0.0.1:8000/
@app.get("/")
def home():
    return {"Hello":"User"}


# http://127.0.0.1:8000/about
@app.get("/about")
def about():
    return {"build by ":"muthu"}


# http://127.0.0.1:8000/all-model
@app.get("/all-model")
async def all_models():
    return {"models":inventory}



# http://127.0.0.1:8000/get-model/{model_id:int}           PATH variable without validation 
@app.get('/get-model/{model_id}')
def get_model(model_id:int):
    return {"item":inventory[model_id]}



# http://127.0.0.1:8000/get-model-by-id/{int}
@app.get('/get-model-by-id/{model_id}')
def get_items(model_id:int = Path(None,description="ID expects Integer",gt=0,le=len(inventory))):   # Path(default_value, description="")
    return {"item":inventory[model_id]}



# http://127.0.0.1:8000/get-model-by-name?model_name="model_name"
@app.get("/get-model-by-name")                                                                      # by-default query parameter required so None or add Optional
def get_by_name(*, model_name:Optional[str]=Query("",description="Expects string")):
    model_name = model_name.strip().lower()
    bucket_list = []
    for item_id in inventory:
        if (inventory[item_id]["model"]==model_name):
            bucket_list.append(inventory[item_id])
    if(len(bucket_list)!=0):
        return({"models":bucket_list})
    return {"data":"model not yet build"}



'''  ## POST request ##  '''

class Model(BaseModel):
    model:str
    accuracy:float
    version: Optional[str]=None
    date : Optional[datetime]=datetime.now() 



# http://127.0.0.1:8000/create-model  <JSON - BODY >
@app.post("/create-model/{model_id}")                                                                       #combine query and path parameter
async def create_item(item:Model,model_id:int):
    # print(type(item))
    if( model_id in inventory): return {"custom err":"model already present"}
    inventory[model_id]={
        "model":str(item.model).strip().lower(),
        "accuracy": item.accuracy,
        "version": item.version,
        "date": item.date
    }
    return {
        "response": "item added",
        "all items":inventory
    }



'''  ## PUT request ##  '''

class UpdateModel(BaseModel):
    model:Optional[str]=None
    accuracy:Optional[float]=None
    version: Optional[str]=None
    date : Optional[datetime]=datetime.now() 


@app.put("/update-model/")
def update_item(item_id:int,item:UpdateModel):
    if( item_id not in inventory): return {"error":"Item id does not present in inventory"}
    else:
        if item.model != None: inventory[item_id]["model"] = item.model
        elif item.accuracy != None: inventory[item_id]["accuracy"] = item.accuracy
        elif item.brand!=None: inventory[item_id]["version"] = item.version
        inventory[item_id]["date"]=item.date
        return {
            "status":"updated!!",
            "income change":item,
            "updated item":inventory[item_id],
            "all  stocks": inventory
        }



'''  ## DELETE request ##  '''

@app.delete("/delete-model")
def delete_item(model_id:int= Query(None,description="ID expects Integer",gt=0,le=len(inventory))):        #Path(default_value, description=""  ))
    if model_id not in inventory:
        return {"error": "ID not exists"}
    else:
        del inventory[model_id]
        return {"msg": "ID deleted!!"}



# To RUN : uvicorn working:app --reload
# To Test: http://127.0.0.1:8000/docs