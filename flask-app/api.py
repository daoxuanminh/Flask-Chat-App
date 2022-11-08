from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:daominh@localhost/newdb"
db.init_app(app)

parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('user_name')
parser.add_argument('user_password')
parser.add_argument('message')
parser.add_argument('room_id')

# TODOS = {
#     'todo1': {'task': 'build an API'},
#     'todo2': {'task': '?????'},
#     'todo3': {'task': 'profit!'},
# }
secsion = {"user_id": None}


class Rooms(db.Model):
    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.Integer)

    # def __repr__(self):
    #     return {"room_id": self.room_id, "room_name": self.room_name}


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    user_password = db.Column(db.String(100))
    # ham __init__ la ham hoi tao constructed

    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password


class RoomUsers(db.Model):
    __tablename__ = 'room_users'
    room_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)


class Message (db.Model):
    __tablename__ = 'messages'
    user_id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer)
    message = db.Column(db.Text)
    sending_time = db.Column(db.DateTime)

    def __init__(self, room_id, message, sending_time):
        self.user_id = secsion['user_id']
        self.room_id = room_id
        self.message = message
        self.sending_time = sending_time
        pass


class Friends(db.Model):
    __tablename__ = 'friends'
    user1_id = db.Column(db.Integer, primary_key=True)
    user2_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id


with app.app_context():
    # print(secsion['user_id'])
    # list_friend = Friends.query.filter_by(
    #     user1_id == secsion['user_id'])
    # args = parser.parse_args()
    # print(Message.query.filter_by(Message.room_id == args['room_id']))
    # a = Friends.query.filter_by(user1_id=secsion['user_id']).all()
    # print(a)
    # # print(Friends.query.filter_by(user1_id=secsion['user_id']))
    # for i in a:
    #     print(i.user2_id)
    # print(type(db.session))
    # args = parser.parse_args()
    # if (User.query.filter_by(user_name=args['user_name']) and User.query.filter_by(user_password=args['user_password'])):
    #     print("Login successful")
    # else:
    #     print("Login failed")

    # me = User('admin2', 'admin2')
    # delete = User.query.get('admin')
    # print(type(delete))
    # print(User.query.filter_by(user_name='missing').first())
    # db.session.add(me)
    # db.session.commit()
    # peter = User.query.filter_by(user_name='admin').first()
    # add user
    # if (User.query.filter_by(user_name='daominh').first() is None):
    #     me = User('daominh', 'daominh')
    #     # delete = User.query.get('daominh')
    #     # print(type(delete))
    #     # print(User.query.filter_by(user_name='missing').first())
    #     db.session.add(me)
    #     db.session.commit()
    # if (User.query.filter_by(user_name='admin').first()):
    #     # me = User('admin', 'admin')
    #     # delete = User.query.get('admin')
    #     delete = User.query.filter_by(user_name='admin').first()
    #     # print(type(delete))
    #     # print(User.query.filter_by(user_name='missing').first())
    #     db.session.delete(delete)
    #     db.session.commit()
    # print(User.query.filter_by(user_name='daominh').count())
    # print(peter)
    # all_user = User.query.all()
    # print(all_user)
    pass


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


# Todo
# shows a single todo item and lets you delete a todo item
# class Todo(Resource):
#     def get(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         a = db.session.query(User).all()
#         return TODOS[todo_id]

#     def delete(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         del TODOS[todo_id]
#         return '', 204

#     def put(self, todo_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         TODOS[todo_id] = task
#         return task, 201

# TodoList
# shows a list of all todos, and lets you POST to add new tasks


# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         TODOS[todo_id] = {'task': args['task']}
#         return TODOS[todo_id], 201


class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        if (secsion['user_id'] == None):
            user = User.query.filter_by(user_name=args['user_name']).first()
            if (user.user_name == args['user_name'] and user.user_password == args['user_password']):
                # session['login'] = True
                secsion['user_id'] = user.user_id
                print(secsion['user_id'])
                return {"status": "Login successful"}, secsion['user_id']
            else:
                return {"status": "Login failed"}, secsion['user_id']
        else:
            return {"status": "Logined"}, secsion['user_id']


class UserLogout(Resource):
    def get(self):
        # print(secsion['user_id'])
        secsion['user_id'] = None
        if (secsion['user_id'] == None):
            return {"status": "Logout successful"}
        else:
            return {"status": "Logout failed"}


class FriendLists(Resource):
    def get(self):
        if (secsion['user_id'] == None):
            return {"status": "chua dang nhap"}
        else:
            result = []
            list_friend = Friends.query.filter_by(
                user1_id=secsion['user_id']).all()
            # print(type(list_friend))
            for i in list_friend:
                print(i.user1_id, i.user2_id)
                result.append(int(i.user2_id))
            # print(len(result))
            s = {}
            for i in range(len(result)):
                s[i] = {User.query.filter_by(
                    user_id=result[i]).first().user_id: User.query.filter_by(
                    user_id=result[i]).first().user_name}
            return s


api.add_resource(FriendLists, '/friends')


class AddUser(Resource):
    def post(self):
        args = parser.parse_args()
        if (User.query.filter_by(user_name=args['user_name']).first() is None):
            me = User(args['user_name'], args['user_password'])
            db.session.add(me)
            db.session.commit()
            return {"status": "add successful"}
        else:
            return {"status": "add failed"}


api.add_resource(AddUser, '/adduser')


class SendMessage(Resource):
    def post(self):
        args = parser.parse_args()
        if (secsion['user_id'] != None):
            newmss = Message(
                args['room_id'], args['message'], datetime.datetime.now())
            db.session.add(newmss)
            db.session.commit()
            return {"status": "sending successful"}
        else:
            return {"status": "Chua dang nhap"}
    pass


api.add_resource(SendMessage, '/sendingmessager')


class GetListRooms(Resource):
    def get(self):
        # args = parser.parse_args()
        if (secsion['user_id'] != None):
            query = RoomUsers.query.filter_by(user_id=secsion['user_id']).all()
            # print(Rooms.query.filter_by(room_id = ).first().room_name)
            reusult = {}
            for i in range(len(query)):
                reusult['name_room_'+str(query[i].room_id)] = Rooms.query.filter_by(
                    room_id=query[i].room_id).first().room_name
            return reusult
        else:
            return {"status": "Chua dang nhap"}
    pass


api.add_resource(GetListRooms, '/listroom')


class SeenMessage(Resource):
    def get(self):
        args = parser.parse_args()
        if (secsion['user_id'] != None):
            query = RoomUsers.query.filter_by(
                room_id=args['room_id']).all()
            list_user_in_room = []
            for i in range(len(query)):
                list_user_in_room.append(query[i].user_id)
            if (secsion['user_id'] in list_user_in_room):
                mss = Message.query.filter_by(room_id=args['room_id']).order_by(
                    Message.sending_time).all()
                print(mss[0].sending_time)
                result = {}
                for i in range(len(mss)):
                    result["mss_"+str(i)] = {
                        "room_id": mss[i].room_id,
                        "user_id": mss[i].user_id,
                        "user_name": User.query.filter_by(user_id=int(mss[i].user_id)).first().user_name,
                        "sending_time": str(mss[i].sending_time)
                    }
                return result
            else:
                return {"status": "You are not at room"}
        else:
            return {"status": "Chua dang nhap"}
    pass


api.add_resource(SeenMessage, '/seenmessager')
##
# Actually setup the Api resource routing here
##
# api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    app.run(debug=True)
