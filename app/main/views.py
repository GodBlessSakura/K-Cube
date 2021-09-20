from datetime import datetime
import os
import json
from flask import render_template, session, redirect, url_for, request, abort, current_app, flash,make_response, jsonify
from flask_login import current_user
from . import main
from .forms import PostForm, EditProfileForm,EditProfileAdminForm, CommentForm
from .. import db, photos
from ..models import User,Role,Post,Comment
from ..email import send_email
from ..decorators import admin_required, permission_required
from ..models import Permission
from flask_login import login_required
from ..neo_db.query_graph import query, all_graph, query_add_link, query_delete_link, query_two, query_delete_head_node, query_delete_tail_node, query_add_head_node, query_add_tail_node
# from ..neo_db.query_graph import query, all_graph

# @main.route('/', methods=['GET', 'POST'])
# @main.route('/index', methods=['GET', 'POST'])
# def index():
#     return render_template('tree.html')

@main.route("/", methods=["GET","POST"])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    show_followed = False
    show_yours = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_yours = bool(request.cookies.get('show_yours', ''))
    if show_followed:
        query = current_user.followed_posts
    elif show_yours:
        query = Post.query.filter_by(author=current_user)
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('main_page.html', form=form, posts=posts,show_followed=show_followed, pagination=pagination,show_yours=show_yours)

@main.route("/logout", methods=["GET","POST"])
@login_required
def logout():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    show_followed = False
    show_yours = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
        show_yours = bool(request.cookies.get('show_yours', ''))
    if show_followed:
        query = current_user.followed_posts
    elif show_yours:
        query = Post.query.filter_by(author=current_user)
    else:
        query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,show_followed=show_followed, pagination=pagination,show_yours=show_yours)


@main.route('/admin', methods=["GET","POST"])
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

@main.route("/user/<username>",methods=["GET","POST"])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    page = request.args.get("page",1,type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    return render_template("user.html", user=user, posts=posts,pagination=pagination)  



@main.route("/editProfile",methods=["GET","POST"])
@login_required
def edit_user():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if form.photo.data:
            current_user.image_filename = photos.save(form.photo.data,name="user/" + current_user.username + ".")
            current_user.image_url = photos.url(current_user.image_filename)
        db.session.add(current_user)
        return redirect(url_for("main.user",username=current_user.username))
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me    
    return render_template("editProfile.html", form=form, image_url=current_user.image_url)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.location = form.location.data
        user.about_me = form.about_me.data
        if form.photo.data:
            user.image_filename = photos.save(form.photo.data, name="user/" + user.username+".")
            user.image_url = photos.url(user.image_filename)
        db.session.add(user)
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('editProfile.html', form=form, user=user,image_url=user.image_url)

@main.route("/post/<int:id>",methods=['GET', 'POST'])
def post(id):
    show_more = False
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if current_user.can(Permission.COMMENT) and form.validate_on_submit():
        comment = Comment(body=form.body.data,author=current_user._get_current_object(),post=post)
        db.session.add(comment)
        return redirect(url_for('main.post',id=id))
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.filter_by(post_id=id,disable=False).order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template("post.html", form=form,posts=[post],comments=comments,pagination=pagination,show_more=show_more)

@main.route("/createPost", methods=["GET","POST"])
@login_required
def create_post():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data,body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post',id=post.id))
    return render_template("construction.html",form=form,createPostFlag=True)


@main.route("/kgs", methods=["GET","POST"])
@login_required
def kgs():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data,body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post',id=post.id))
    return render_template("main_page.html",form=form,createPostFlag=True)



@main.route("/editPost/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        post.title = form.title.data
        db.session.add(post)
        return redirect(url_for("main.post",id=post.id))
    form.body.data = post.body
    form.title.data = post.title
    return render_template("editPost.html",form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)

@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    resp.set_cookie('show_yours', '', max_age=30*24*60*60)

    return resp

@main.route('/yours')
@login_required
def show_yours():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_yours', '1', max_age=30*24*60*60)
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    resp.set_cookie('show_yours', '', max_age=30*24*60*60)
    return resp

@main.route("/moderate-comments", methods=["GET","POST"])
@permission_required(Permission.MODERATE_COMMENTS)
@login_required
def moderate_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    comments = pagination.items
    return render_template('comments.html', pagination=pagination,comments=comments)

@main.route("/disable-comment/<int:id>", methods=["GET","POST"])
@permission_required(Permission.MODERATE_COMMENTS)
@login_required
def disable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disable = True
    db.session.add(comment)
    return redirect(url_for("main.moderate_comments", page=request.args.get('page', 1, type=int)))

@main.route("/enable-comment/<int:id>", methods=["GET","POST"])
@permission_required(Permission.MODERATE_COMMENTS)
@login_required
def enable_comment(id):
    comment = Comment.query.get_or_404(id)
    comment.disable = False
    db.session.add(comment)
    return redirect(url_for("main.moderate_comments", page=request.args.get('page', 1, type=int)))


@main.route('/search', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@main.route('/teach_plan', methods=['GET', 'POST'])
def teach_plan():
    return render_template('plan.html')


@main.route('/sendjson', methods=['POST'])
def sendjson():
# 接受前端发来的数据
    data = json.loads(request.get_data())
    file_name = data["name"]
    path = os.path.dirname(__file__)
    print("path:", path)
    with open(path + "/" + file_name + ".json", "w") as f:
        json.dump(data, f)
        print("Successfully saved!")


    # score = data["score"]
    # 自己在本地组装成Json格式,用到了flask的jsonify方法
    info = dict()
    info['name'] = "Successfully saved!"
    # info['lesson'] = lesson
    # info['score'] = score

    return jsonify(info)

@main.route('/myspace', methods=['GET', 'POST'])
def myspace():
    user_id = current_user.username
    print(user_id)
    return render_template('mykg.html', user_name=str(user_id))

@main.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query_two(str(name))
    # json_data = query()
    return jsonify(json_data)


@main.route('/subgraph', methods=['GET', 'POST'])
def subgraph():
    name = request.args.get('name')
    json_data = query_two(str(name))
    return jsonify(json_data)


@main.route('/add_head_node', methods=['GET', 'POST'])
def add_head_node():
    source = request.args.get('source')
    target = request.args.get('target')
    query_add_head_node(str(source), str(target))
    return source


@main.route('/add_tail_node', methods=['GET', 'POST'])
def add_tail_node():
    source = request.args.get('source')
    target = request.args.get('target')
    query_add_tail_node(str(source), str(target))
    return source


@main.route('/delete_head_node', methods=['GET', 'POST'])
def delete_head_node():
    name = request.args.get('name')
    json_data = query_delete_head_node(str(name))
    return jsonify(json_data)


@main.route('/delete_tail_node', methods=['GET', 'POST'])
def delete_tail_node():
    name = request.args.get('name')
    json_data = query_delete_tail_node(str(name))
    return jsonify(json_data)


@main.route('/add_link', methods=['GET', 'POST'])
def add_link():
    source = request.args.get('source')
    target = request.args.get('target')
    query_add_link(str(source), str(target))
    return source


@main.route('/delete_link', methods=['GET', 'POST'])
def delete_link():
    source = request.args.get('source')
    target = request.args.get('target')
    query_delete_link(str(source), str(target))
    return source


@main.route('/fold', methods=['GET', 'POST'])
def fold():
    return render_template('fold.html')


@main.route('/tree',methods=['GET', 'POST'])
def tree():
    return render_template('tree.html')

@main.route('/construction',methods=['GET', 'POST'])
@login_required
def construction():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.post', id=post.id))

    user_id = current_user.username;
    return render_template('construction.html', user_name=user_id)

@main.route('/graph_json', methods=['GET', 'POST'])
def graph_json():
    json_data = {"name": "Original",
                 "children": [{"name": "analytics",
                               "children": [{"name": "cluster",
                                             "children": [{"name": "AgglomerativeCluster", "size": 3938},
                                                          {"name": "CommunityStructure", "size": 3812},
                                                          {"name": "HierarchicalCluster", "size": 6714},
                                                          {"name": "MergeEdge", "size": 743}
                                                          ]
                                             },
                                            {
                                                "name": "graph",
                                                "children": [
                                                    {"name": "BetweennessCentrality", "size": 3534},
                                                    {"name": "LinkDistance", "size": 5731},
                                                    {"name": "MaxFlowMinCut", "size": 7840},
                                                    {"name": "ShortestPaths", "size": 5914},
                                                    {"name": "SpanningTree", "size": 3416}
                                                ]
                                            },
                                            {
                                                "name": "optimization",
                                                "children": [
                                                    {"name": "AspectRatioBanker", "size": 7074}
                                                ]
                                            }
                                            ]
                               }
                              ]
                 }
    # json_data1 = {"name": "AI",
    #              "children": [{"name": "analytics",
    #                            "children": [{"name": "cluster",
    #                                          "children": [{"name": "AgglomerativeCluster", "size": 3938},
    #                                                       {"name": "CommunityStructure", "size": 3812},
    #                                                       {"name": "HierarchicalCluster", "size": 6714},
    #                                                       {"name": "MergeEdge", "size": 743}
    #                                                       ]
    #                                          },
    #                                         {
    #                                             "name": "graph",
    #                                             "children": [
    #                                                 {"name": "BetweennessCentrality", "size": 3534},
    #                                                 {"name": "LinkDistance", "size": 5731},
    #                                                 {"name": "MaxFlowMinCut", "size": 7840},
    #                                                 {"name": "ShortestPaths", "size": 5914},
    #                                                 {"name": "SpanningTree", "size": 3416}
    #                                             ]
    #                                         },
    #                                         {
    #                                             "name": "optimization",
    #                                             "children": [
    #                                                 {"name": "AspectRatioBanker", "size": 7074}
    #                                             ]
    #                                         }
    #                                         ]
    #                            }
    #
    #                           ]
    #              }
    return jsonify(json_data)

@main.route('/get_profile',methods=['GET','POST'])


# @main.route('/KGQA_answer', methods=['GET', 'POST'])
# def KGQA_answer():
#     question = request.args.get('name')
#     json_data = get_KGQA_answer(get_target_array(str(question)))
#     return jsonify(json_data)
# @main.route('/search_name', methods=['GET', 'POST'])
# def search_name():
#     name = request.args.get('name')
#     json_data=query(str(name))
#     return jsonify(json_data)

@main.route('/mydict', methods=['GET', 'POST'])
def mydict():
    json_data = {"name": "Original",
                 "children": [{"name": "analytics",
                               "children": [{"name": "cluster",
                                             "children": [{"name": "AgglomerativeCluster", "size": 3938},
                                                          {"name": "CommunityStructure", "size": 3812},
                                                          {"name": "HierarchicalCluster", "size": 6714},
                                                          {"name": "MergeEdge", "size": 743}
                                                          ]
                                             },
                                            {
                                                "name": "graph",
                                                "children": [
                                                    {"name": "BetweennessCentrality", "size": 3534},
                                                    {"name": "LinkDistance", "size": 5731},
                                                    {"name": "MaxFlowMinCut", "size": 7840},
                                                    {"name": "ShortestPaths", "size": 5914},
                                                    {"name": "SpanningTree", "size": 3416}
                                                ]
                                            },
                                            {
                                                "name": "optimization",
                                                "children": [
                                                    {"name": "AspectRatioBanker", "size": 7074}
                                                ]
                                            }
                                            ]
                               }
                              ]
                 }
    return jsonify(json_data)

@main.route('/all_kg', methods=['GET', 'POST'])
def all_kg():
    # json_data = {"name": "Original",
    #              "children": [{"name": "analytics",
    #                            "children": [{"name": "cluster",
    #                                          "children": [{"name": "AgglomerativeCluster", "size": 3938},
    #                                                       {"name": "CommunityStructure", "size": 3812},
    #                                                       {"name": "HierarchicalCluster", "size": 6714},
    #                                                       {"name": "MergeEdge", "size": 743}
    #                                                       ]
    #                                          },
    #                                         {
    #                                             "name": "graph",
    #                                             "children": [
    #                                                 {"name": "BetweennessCentrality", "size": 3534},
    #                                                 {"name": "LinkDistance", "size": 5731},
    #                                                 {"name": "MaxFlowMinCut", "size": 7840},
    #                                                 {"name": "ShortestPaths", "size": 5914},
    #                                                 {"name": "SpanningTree", "size": 3416}
    #                                             ]
    #                                         },
    #                                         {
    #                                             "name": "optimization",
    #                                             "children": [
    #                                                 {"name": "AspectRatioBanker", "size": 7074}
    #                                             ]
    #                                         }
    #                                         ]
    #                            }
    #                           ]
    #              }
    json_data = all_graph()
    return jsonify(json_data)

@main.route('/all_kg_build', methods=['GET', 'POST'])
def all_kg_build():
    json_data = {"name": "Original",
                 "children": [{"name": "analytics",
                               "children": [{"name": "cluster",
                                             "children": [{"name": "AgglomerativeCluster", "size": 3938},
                                                          {"name": "CommunityStructure", "size": 3812},
                                                          {"name": "HierarchicalCluster", "size": 6714},
                                                          {"name": "MergeEdge", "size": 743}
                                                          ]
                                             },
                                            {
                                                "name": "graph",
                                                "children": [
                                                    {"name": "BetweennessCentrality", "size": 3534},
                                                    {"name": "LinkDistance", "size": 5731},
                                                    {"name": "MaxFlowMinCut", "size": 7840},
                                                    {"name": "ShortestPaths", "size": 5914},
                                                    {"name": "SpanningTree", "size": 3416}
                                                ]
                                            },
                                            {
                                                "name": "optimization",
                                                "children": [
                                                    {"name": "AspectRatioBanker", "size": 7074}
                                                ]
                                            }
                                            ]
                               }
                              ]
                 }
    return jsonify(json_data)

@main.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


@main.route('/all_url', methods=['GET', 'POST'])
def all_url():
    json_data = {
      "Artificial_Intelligence": {
         "url1": "www",
         "wiki_url": "www.baidu.com"
      },
      "Data_Mining": {
        "url1": "",
        "url2": ""
      },
      "Machine_Learning": {
        "url1": "",
        "ur21": ""
      }
}
