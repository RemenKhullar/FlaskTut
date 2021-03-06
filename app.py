from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tmp/database.db'
db=SQLAlchemy(app)

class VideoModel(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	name=db.Column(db.String(100),nullable=False)
	views=db.Column(db.Integer,nullable=False)
	likes=db.Column(db.Integer,nullable=False)

	def __repr__(self):
		return f'Video (name= {name}, views={views}, likes={likes})'

#db.create_all() #ONly run first time

video_put_args=reqparse.RequestParser()
video_put_args.add_argument('name',type=str,help='Name of the video',required=True)
video_put_args.add_argument('views',type=int,help='views of the video',required=True)
video_put_args.add_argument('likes',type=int,help='likes of the video',required=True )

video_up_args=reqparse.RequestParser()
video_up_args.add_argument('name',type=str,help='Name of the video')
video_up_args.add_argument('views',type=int,help='views of the video')
video_up_args.add_argument('likes',type=int,help='likes of the video')

resource_fields={
	'id':fields.Integer,
	'name':fields.String,
	'likes':fields.Integer,
	'views':fields.Integer
}

class Video(Resource):
	@marshal_with(resource_fields)
	def get(self,vid_id):
		result=VideoModel.query.filter_by(id=vid_id).first()
		if not result:
			abort(404,message='Vid id not exists...')
		return result, 200

	@marshal_with(resource_fields)	
	def post(self,vid_id):
		result=VideoModel.query.filter_by(id=vid_id).first()
		if result:
			abort(409,message=f'Video id {vid_id} taken')
		args=video_put_args.parse_args()
		video=VideoModel(id=vid_id,name=args['name'],likes=args['likes'],views=args['views'])
		db.session.add(video)
		db.session.commit()
		return video, 201

	@marshal_with(resource_fields)
	def patch(self,vid_id):
		result=VideoModel.query.filter_by(id=vid_id).first()
		if not result:
			abort(404,'video does not exists...')
		args=video_up_args.parse_args()
		if args['name']:
			result.name=args['name'] 
		if args['likes']:
			result.likes=args['likes'] 
		if args['views']:
			result.views=args['views'] 

		db.session.commit()
		return result, 200

	def delete(self,vid_id):
		result=VideoModel.query.filter_by(id=vid_id).first()
		if not result:
			abort(404,'video does not exists...')
		
		db.session.delete(result)
		db.session.commit()
		return {"message":f"deleted video {vid_id}"}, 201

api.add_resource(Video,'/video/<int:vid_id>')

if __name__=="__main__":
	app.run(debug=True)

