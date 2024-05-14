from fastapi import BackgroundTasks, FastAPI, APIRouter, HTTPException
from configurations import collection
from database.schemas import all_tasks
from database.models import Todo
from datetime import datetime
from bson.objectid import ObjectId
from log.log import write_logs

app = FastAPI()
router = APIRouter()

@router.get("/")
async def get_all_todos():
    data = collection.find({"is_deleted": False})
    return all_tasks(data)

@router.post("/")
async def create_task(new_task: Todo, background_tasks: BackgroundTasks):
    try:
        # print(new_task, '-------------', type(new_task))
        background_tasks.add_task(write_logs, message = f"a todo with {dict(new_task)['title'].upper()} as title is going to be added")
        resp = collection.insert_one(dict(new_task))
        background_tasks.add_task(write_logs, message = f"a todo with {dict(new_task)['title'].upper()} as title inserted - id in db: {str(resp.inserted_id)}")
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"some error occured {e}")

@router.put("/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        exsiting_task = collection.find_one({"_id": id, "is_deleted": False})
        if not exsiting_task:
            return HTTPException(status_code= 404, detail=f"Task does not exist")
        updated_task.updated_at = int(datetime.timestamp(datetime.now()))
        response = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status_code": 200, "id": task_id, "message": "Task updated successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured: {e}")

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        exsiting_task = collection.find_one({"_id": id, "is_deleted": False})
        if not exsiting_task:
            return HTTPException(status_code= 404, detail=f"Task does not exist")
        response = collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"status_code": 200, "id": task_id, "message": "Task deleted successfully"}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Some error occured: {e}")
    

app.include_router(router)