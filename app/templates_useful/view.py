main.route("/", methods=["GET","POST"])
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

@main.route('/get_all_relation', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')

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

@main.route('/myspace', methods=['GET', 'POST'])
def myspace():
    user_id = current_user.username
    print(user_id)
    return render_template('mykg.html', user_name=str(user_id))

