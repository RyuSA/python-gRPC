from route_pb2 import *
from route_pb2_grpc import TodoGatewayStub
import grpc

from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")


def create_todo(stub, todo_name):
    response = stub.TodoCreate(TodoCreateRequest(
        todo_name=todo_name,
        timestamp=get_timestamp()
    ))

    if response.response.is_success:
        print("create success")
    else:
        print("Error : " + response.response.message)


def show_todos(stub):
    response = stub.TodoShow(
        TodoShowRequest(
            timestamp=get_timestamp()
        )
    )

    print("---- Todo Name : is done? ----")

    for todo in response.todos:
        print("%s : %s" % (todo.todo_name, todo.is_done))

    print("")


def update_todo(stub, todo_name, is_done):
    response = stub.TodoUpdate(
        TodoUpdateRequest(
            todo=TodoComponent(
                todo_name=todo_name,
                is_done=is_done
            ),
            timestamp=get_timestamp()
        )
    )

    if response.response.is_success:
        print("update success")
        if response.response.message:
            print("message : %s" % response.response.message)
    else:
        print("Error : " + response.response.message)


if __name__ == '__main__':

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = TodoGatewayStub(channel)

        while True:
            command = input().split()
            if len(command) == 0:
                break
            if command[0] == "c" or command[0] == "create":
                # create todo
                try:
                    todo_name = command[1]
                except:
                    print("input todo name: ", end="")
                    todo_name = input()
                create_todo(stub, todo_name)
            elif command[0] == "s" or command[0] == "show":
                # show todos
                show_todos(stub)
            elif command[0] == "u" or command[0] == "update":
                # update todo
                try:
                    todo_name = command[1]
                except:
                    print("input todo name: ", end="")
                    todo_name = input()
                try:
                    is_done = command[2] == "y" or command[2] == "yes"
                except:
                    print("is done ? y/n: ", end="")
                    _is_done = input()
                    is_done = _is_done == "y" or _is_done == "yes"
                update_todo(stub, todo_name, is_done)
            else:
                print("input an illigal command, try again.")
