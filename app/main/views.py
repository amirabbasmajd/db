import uuid
from datetime import datetime
from time import time
from bson.objectid import ObjectId

from flask import (
    render_template,
    url_for,
    redirect,
    request,
    flash
)
from flask_login import login_required

from app import mongo
from app.main import main
from app.main.forms import AddPostForm
from app.main.forms import addMyComment


@main.route('/', methods=['GET', 'POST'] )
@login_required
def home():

    print('zzzzzzzzz')
    if request.method == 'POST':

        request.form[''];
        flash('comment add successfully', category='success')
    print("hello")
    post = mongo.db.posts.find()
    return render_template('index.html', post=post , form=addMyComment())



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
    if form.validate_on_submit():
        file_path = "/static/img/" + str(uuid.uuid1())
        mongo.db.posts.insert({'title': form.title.data,
                               'post_body': form.post.data,
                               'published_on': published_on,
                               'image': file_path,
                               'image_file_name': request.files['image'].filename,
                               'link': form.link.data,
                               'tags': form.tags.data.split(',')
                               })
        request.files['image'].save("../mongodb_project/app" + file_path)
        flash('Post added successfully!', category='success')
        return redirect(url_for('main.new_post'))
    return render_template('add_post.html', form=form)


@main.route('/profile')
def profile():
    return render_template('profile.html')

# @main.route('/showpostandcomment/<string:post_id>', methods=['GET', 'POST'])
@main.route('/showpostandcomment', methods=['GET', 'POST'])
def showpostandcomment():
    # if request.form['postId']:
    #     exit(0);

    # print( request.form['id'])
    # print('helll')
    # pprint (" helllllllo")
    s = request.args.get('myid')
    post = mongo.db.posts.find({"_id":ObjectId(s)})

    return render_template('showpostcomment.html' ,post=post)