import uuid
from datetime import datetime
from queue import Empty
from time import time
from bson.objectid import ObjectId
from flask_login import current_user

from flask import (
    render_template,
    url_for,
    redirect,
    request,
    flash
)
from flask_login import login_required, current_user

from app import mongo
from app.main import main
from app.main.forms import AddPostForm
from app.main.forms import addComment
from app.main.forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        request.form[''];
        flash('comment add successfully', category='success')
    post = mongo.db.posts.find()
    userbookmarks = mongo.db.users.find_one({"_id": current_user.username}, {"_id": 0, "bookmarks": 1})
    if 'bookmarks' in userbookmarks:
        userbookmarks = userbookmarks['bookmarks']
    return render_template('index.html', post=post, userbookmarks=userbookmarks)

    # if userbookmarks:
    #     ['bookmarks']
    # else:
    #     return render_template('index.html', post=post, userbookmarks=[])


# @main.add_comment('/addcommenct' ,methods=['GET', 'POST'] )
# def add_comment():
#     return render_template('index.html')

@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'GET':
        return render_template('add_post.html', title='Add', form=AddPostForm())

    form = AddPostForm()
    published_on = datetime.fromtimestamp(time()).strftime('%d-%m-%Y in %H:%M')
    file_type = request.files['image'].filename.split('.')[-1]
    if form.validate_on_submit():
        file_path = "/static/img/" + str(uuid.uuid1()) + '.' + file_type
        mongo.db.posts.insert({'title': form.title.data,
                               'post_body': form.post.data,
                               'published_on': published_on,
                               'image': file_path,
                               'image_file_name': request.files['image'].filename,
                               'link': form.link.data,
                               'tags': form.tags.data.split(','),
                               'username': current_user.username
                               })
        request.files['image'].save("../mongodb_project/app" + file_path)
        flash('Post added successfully!', category='success')
        return redirect(url_for('main.new_post'))
    return render_template('add_post.html', form=form)


@main.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    postid = request.args.get('postid')

    if request.method == 'GET':
        add_post_form = AddPostForm()
        try:
            post_default_values = mongo.db.posts.find_one({"_id": ObjectId(postid)})
        except Exception as e:
            return 'wrong id'
        if post_default_values == None:
            return 'wrong id'

        if current_user.username != post_default_values['username']:
            return 'you do not have access to edit this post'

        add_post_form.title.data = post_default_values['title']
        add_post_form.post.data = post_default_values['post_body']
        add_post_form.link.data = post_default_values['link']
        tags = ''
        for t in post_default_values['tags']:
            tags += t + ','
        tags = tags[:-1]
        add_post_form.tags.data = tags

        return render_template('add_post.html', title='Add', form=add_post_form)

    form = AddPostForm()
    published_on = datetime.fromtimestamp(time()).strftime('%d-%m-%Y in %H:%M')
    file_type = request.files['image'].filename.split('.')[-1]
    if form.validate_on_submit():
        file_path = "/static/img/" + str(uuid.uuid1()) + '.' + file_type
        mongo.db.posts.save(
            {'_id': ObjectId(postid),
             'title': form.title.data,
             'post_body': form.post.data,
             'published_on': published_on,
             'image': file_path,
             'image_file_name': request.files['image'].filename,
             'link': form.link.data,
             'tags': form.tags.data.split(','),
             'username': current_user.username})

        request.files['image'].save("../mongodb_project/app" + file_path)
        flash('Post edited successfully!', category='success')
        return redirect(url_for('main.profile'))
    return render_template('add_post.html', form=form)


@main.route('/deletepost')
@login_required
def delete_post():
    postid = request.args.get('postid')
    if current_user.username == mongo.db.posts.find_one({'_id': ObjectId(postid)})['username']:
        mongo.db.posts.delete_one({'_id': ObjectId(postid)})
    return redirect(url_for('main.profile'))


@main.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html', title='Search', form=SearchForm())

    form = SearchForm()
    searched_text = form.search_text.data
    if form.validate_on_submit():
        posts = mongo.db.posts.find(
            {"$or": [{"title": {"$regex": searched_text}}, {"post_body": {"$regex": searched_text}}]})

        users = mongo.db.users.find(
            {"$or": [{"_id": {"$regex": searched_text}}, {"full_name": {"$regex": searched_text}}]} ,
            {"_id" : 1, "full_name" : 1 }
        )

        if posts.count() == 0:
            flash('no post found', category='warning')
        if users.count() == 0:
            flash('no user found', category='warning')

        return render_template('search.html', title='Search', form=form, post=posts , users = users)

    return render_template('search.html', form=form)


@main.route('/mybookmarks')
@login_required
def mybookmarks():
    bookmark_ids = mongo.db.users.find_one({"_id": current_user.username})['bookmarks']
    bookmark_posts = mongo.db.posts.find({"_id": {"$in": bookmark_ids}})

    return render_template('index.html', post=bookmark_posts)


@main.route('/profile')
def profile():
    username = request.args.get('username')
    if username == None and current_user.is_authenticated:
        username = current_user.username

    can_edit = (current_user.is_authenticated and username == current_user.username)

    user_detail = mongo.db.users.find_one({"_id": username})
    if user_detail == None:
        return 'wrong username'

    post = mongo.db.posts.find({"username": username})
    return render_template('profile.html', post=post, user_detail=user_detail, can_edit=can_edit)


@main.route('/showpostandcomment', methods=['GET', 'POST'])
def showpostandcomment():
    s = request.args.get('myid')
    post = mongo.db.posts.find({"_id": ObjectId(s)})

    if request.method == 'GET':
        return render_template('showpostcomment.html', post=post, form=addComment())

    form = addComment()
    if form.addYourComment.data != "":
        comment = {'userId': current_user.username, 'text': form.addYourComment.data}
        mongo.db.posts.update({"_id": ObjectId(s)}, {"$push": {"comments": comment}})

    return render_template('showpostcomment.html', post=post, form=addComment())


@main.route('/likepost', methods=['GET', 'POST'])
def likepost():
    s = request.args.get('myid')
    countLike = mongo.db.posts.find({"like": current_user.username, "_id": ObjectId(s)}).count()
    if countLike == 0:
        mongo.db.posts.update({"_id": ObjectId(s)}, {"$push": {"like": current_user.username}})
        flash('Post liked successfully!', category='success')
    else:
        mongo.db.posts.update({"_id": ObjectId(s)}, {"$pull": {"like": current_user.username}})
        flash('Like removed successfully!', category='warning')
    return redirect(url_for('main.home'))


@main.route('/bookmark', methods=['GET', 'POST'])
@login_required
def bookmark():
    s = request.args.get('myid')
    isBookmarked = mongo.db.users.find({"_id": current_user.username, "bookmarks": s}).count()
    if isBookmarked == 0:
        mongo.db.users.update({"_id": current_user.username}, {"$push": {"bookmarks": s}})
        flash('Post bookmarked successfully!', category='success')
    else:
        mongo.db.users.update({"_id": current_user.username}, {"$pull": {"bookmarks": s}})
        flash('Bookmark removed  successfully!', category='warning')
    return redirect(url_for('main.home'))
