from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Init app & api
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# Create a small dictionary
names = {
         "mike": {"age": 21, "gender": "male"},
         "steve": {"age": 58, "gender": "male"}
        }

# Parser for request arguments
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video is reequired", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video is required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes on the video")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}

# First resource
class HelloWorld(Resource):
    def get(self, name):
        # Ensure information is serializable. Here, a python dictionary
        # Matches JSON serializable objects from API 
        return names[name]

    def post(self, name):
        return {'data': 'Posted ' + name}

# Second resource
class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find Video ID....")
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
                abort(409, message="Video ID is taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID doesn't exist to update....")

        if args['name']:
            result.name = args['name']

        if args['views']:
            result.views = args['views']

        if args['likes']:
            result.views = args['likes']

        db.session.commit()
        return result

        
    def delete(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID doesn't exist to delete....")
        db.session.delete(result)
        db.session.commit()
        return '', 204

# First resource URL is added to API, with specific params
api.add_resource(HelloWorld, "/helloworld/<string:name>")

# Second resource URL is added to API
api.add_resource(Video, "/video/<int:video_id>")

# App run procedure
if __name__ == "__main__":
    app.run(debug=True)
