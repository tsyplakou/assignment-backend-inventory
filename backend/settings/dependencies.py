from fastapi import APIRouter, Depends, Request, Response

def get_db(request: Request):
    return request.state.db
