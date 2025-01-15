from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename
from models.comment import Comment
from models.user import User
from models.easypoint import EasyPoint, EasyPointsSimplify
from models.dynamicpost import DynamicPost
from models.photo import Photo
from models.file import File
from create_app import db
import os

main = Blueprint('main', __name__)

# 配置上传文件夹和文件大小限制
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'pdf'}  # 允许的文件类型
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 限制上传文件大小为 16MB

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 检查文件类型是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 上传图片
@main.route('/upload', methods=['POST'])
def upload_image():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo part"}), 400

    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 将文件信息保存到数据库
        new_file = File(filename=filename)
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": f"File {filename} uploaded successfully", "path": filepath}), 200

    return jsonify({"error": "File type not allowed"}), 400

# 提供图片访问
@main.route('/uploads/photos/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 添加新评论
@main.route('/comments', methods=['POST'])
def add_comment():
    data = request.json
    new_comment = Comment(
        user_id=data['user_id'],
        content=data['content'],
        like=data.get('like', 0),
        dislike=data.get('dislike', 0),
        date=data['date']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"message": "Comment added successfully!"}), 201

# 更新评论
@main.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.json
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    comment.content = data.get('content', comment.content)
    comment.like = data.get('like', comment.like)
    comment.dislike = data.get('dislike', comment.dislike)
    comment.date = data.get('date', comment.date)

    db.session.commit()
    return jsonify({"message": "Comment updated successfully!"})

# 删除评论
@main.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully!"})

# 根据 ID 获取 Comment
@main.route('/comments/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    return jsonify(comment.to_dict())

# 获取所有评论
@main.route('/comments', methods=['GET'])
def get_all_comments():
    comments = Comment.query.all()
    return jsonify([comment.to_dict() for comment in comments])

# 获取所有用户
@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# 添加新用户
@main.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        name=data['name'],
        avatar=data['avatar']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"}), 201

# 更新用户
@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.name = data.get('name', user.name)
    user.avatar = data.get('avatar', user.avatar)

    db.session.commit()
    return jsonify({"message": "User updated successfully!"})

# 删除用户
@main.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"})

# 根据 ID 获取 User
@main.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())

# 获取所有 EasyPointSimplify
@main.route('/easypoint/simplify', methods=['GET'])
def get_easypoints():
    points = EasyPoint.query.all()
    simplified_points = [EasyPointsSimplify(point.point_id, point.name, point.lat, point.lng).to_dict() for point in points]
    return jsonify(simplified_points)

# 获取所有 EasyPoint
@main.route('/easypoints/full', methods=['GET'])
def get_fulleasypoints():
    points = EasyPoint.query.all()
    return jsonify([point.to_dict() for point in points])

# 添加新 EasyPoint
@main.route('/easypoints', methods=['POST'])
def add_easypoint():
    data = request.json
    new_point = EasyPoint(
        user_id=data['user_id'],
        name=data['name'],
        type=data['type'],
        info=data['info'],
        location=data['location'],
        photo=data['photo'],  # 这里假设 photo 是上传图片的文件名
        refresh_time=data['refresh_time'],
        likes=data.get('likes', 0),
        dislikes=data.get('dislikes', 0),
        lat=data['lat'],
        lng=data['lng']
    )
    db.session.add(new_point)
    db.session.commit()
    return jsonify({"message": "EasyPoint added successfully!"}), 201

# 更新 EasyPoint
@main.route('/easypoints/<int:point_id>', methods=['PUT'])
def update_easypoint(point_id):
    data = request.json
    point = EasyPoint.query.get(point_id)
    if not point:
        return jsonify({"error": "EasyPoint not found"}), 404

    point.name = data.get('name', point.name)
    point.type = data.get('type', point.type)
    point.info = data.get('info', point.info)
    point.location = data.get('location', point.location)
    point.photo = data.get('photo', point.photo)
    point.refresh_time = data.get('refresh_time', point.refresh_time)
    point.likes = data.get('likes', point.likes)
    point.dislikes = data.get('dislikes', point.dislikes)
    point.lat = data.get('lat', point.lat)
    point.lng = data.get('lng', point.lng)

    db.session.commit()
    return jsonify({"message": "EasyPoint updated successfully!"})

# 删除 EasyPoint
@main.route('/easypoints/<int:point_id>', methods=['DELETE'])
def delete_easypoint(point_id):
    point = EasyPoint.query.get(point_id)
    if not point:
        return jsonify({"error": "EasyPoint not found"}), 404

    db.session.delete(point)
    db.session.commit()
    return jsonify({"message": "EasyPoint deleted successfully!"})

# 根据 ID 获取 EasyPoint
@main.route('/easypoints/<int:point_id>', methods=['GET'])
def get_easypoint(point_id):
    point = EasyPoint.query.get(point_id)
    if not point:
        return jsonify({"error": "EasyPoint not found"}), 404
    return jsonify(point.to_dict())

# 添加新 DynamicPost
@main.route('/dynamicposts', methods=['POST'])
def add_dynamicpost():
    data = request.json
    new_post = DynamicPost(
        title=data['title'],
        date=data['date'],
        like=data.get('like', 0),
        content=data['content'],
        lat=data['location']['lat'] if data['location'] else None,
        lng=data['location']['lng'] if data['location'] else None,
        position=data['position'],
        user_id=data['user_id'],
        comment_id=data.get('comment_id')  # 允许为空值
    )
    db.session.add(new_post)
    db.session.commit()

    # 处理照片列表
    if 'photos' in data:
        for photo_url in data['photos']:
            new_photo = Photo(url=photo_url, dynamicpost_id=new_post.id)
            db.session.add(new_photo)
        db.session.commit()

    return jsonify({"message": "DynamicPost added successfully!"}), 201

# 更新 DynamicPost
@main.route('/dynamicposts/<int:post_id>', methods=['PUT'])
def update_dynamicpost(post_id):
    data = request.json
    post = DynamicPost.query.get(post_id)
    if not post:
        return jsonify({"error": "DynamicPost not found"}), 404

    post.title = data.get('title', post.title)
    post.date = data.get('date', post.date)
    post.like = data.get('like', post.like)
    post.content = data.get('content', post.content)
    if data.get('location'):
        post.lat = data['location'].get('lat', post.lat)
        post.lng = data['location'].get('lng', post.lng)
    post.position = data.get('position', post.position)
    post.user_id = data.get('user_id', post.user_id)
    post.comment_id = data.get('comment_id', post.comment_id)

    db.session.commit()

    # 处理照片列表
    if 'photos' in data:
        # 删除旧照片
        Photo.query.filter_by(dynamicpost_id=post.id).delete()
        # 添加新照片
        for photo_url in data['photos']:
            new_photo = Photo(url=photo_url, dynamicpost_id=post.id)
            db.session.add(new_photo)
        db.session.commit()

    return jsonify({"message": "DynamicPost updated successfully!"})

# 删除 DynamicPost
@main.route('/dynamicposts/<int:post_id>', methods=['DELETE'])
def delete_dynamicpost(post_id):
    post = DynamicPost.query.get(post_id)
    if not post:
        return jsonify({"error": "DynamicPost not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "DynamicPost deleted successfully!"})

# 根据 ID 获取 DynamicPost
@main.route('/dynamicposts/<int:post_id>', methods=['GET'])
def get_dynamicpost(post_id):
    post = DynamicPost.query.get(post_id)
    if not post:
        return jsonify({"error": "DynamicPost not found"}), 404
    return jsonify(post.to_dict())

# 获取所有 DynamicPost
@main.route('/dynamicposts', methods=['GET'])
def get_all_dynamicposts():
    dynamicposts = DynamicPost.query.all()
    return jsonify([dynamicpost.to_dict() for dynamicpost in dynamicposts])