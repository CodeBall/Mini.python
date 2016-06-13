from flask import render_template
from .model import *
from application import app, session
from flask import flash


@app.route('/')
def index():
    rnt = {}
    nodes = session.query(Node).filter_by(nod_pid=21).all()
    rnt[21] = nodes
    lists = [21]

    for x in lists:
        for i in rnt[x]:
            two = session.query(Node).filter_by(nod_pid=i.node_id).all()
            if (two):
                rnt[i.node_id] = two
                lists.append(i.node_id)

    return render_template('index.html', start=21, rnt=rnt)


@app.route('/node/children/<int:id>')
def node_children(id):
    try:
        self_node = Node.get_node(id)
    except AttributeError:
        return render_template('error.html',status = "出错了哦")

    try:
        children = self_node.get_node_child()
    except AttributeError:
        return render_template('error.html',status = "出错了哦~")

    parent_line = self_node.parent_line.split(',')
    parents = Node.get_node_parent(parent_line)
    parents.append(self_node)

    topic = Topic.get_topic(id)

    self_node = self_node.nod_title

    return render_template('listing.html', itself=self_node, childs=children, parents=parents, topic=topic)


@app.route('/area/children/<area_id>')
def area_child(area_id):

    self_area = Area.get_area(area_id)
    children = self_area.get_area_child()

    parent_line = self_area.parent_line.split(',')
    parents = Area.get_area_parents(parent_line)
    parents.append(self_area)

    topic = Topic.get_topic_area(area_id)

    self_title = self_area.area_title

    return render_template('area.html', itself=self_title, childs=children, parents=parents, topic=topic)


@app.route('/topic/<tpc_id>/<tpc_uid>/<tpc_pid>/<tpc_area>')
def topic(tpc_id, tpc_uid, tpc_pid, tpc_area):

    itself = Topic.get_topic_selt(tpc_id)

    user = User.get_topic_user(tpc_uid)

    node = Node.get_node_topic(tpc_pid)
    if node:
        parent_line = node.parent_line.split(',')
        nodes = Node.get_node_parent(parent_line)
        nodes.append(node)

    areas = []
    area = Area.get_area_topic(tpc_area)
    if area:
        area_line = area.parent_line.split(',')
        areas = Area.get_area_parents(area_line)
        areas.append(area)

    reply = Reply.get_reply_topic(tpc_id)

    return render_template('topic.html', itself=itself, user=user, parents=nodes,
                           areas=areas, reply=reply)


@app.route('/user/<int:user_id>')
def user(user_id):

    itself = User.get_user(user_id)
    status = 0
    topic = []
    if (itself):
        topic = Topic.get_topic_user(user_id)
        status = 1

    return render_template('user.html', status=status, itself=itself, topic=topic)
