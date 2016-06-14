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
            two = i.get_node_child()
            if two:
                rnt[i.node_id] = two
                lists.append(i.node_id)

    return render_template('index.html', start=21, rnt=rnt)


@app.route('/node/children/<int:id>')
def node_children(id):
    self_node = Node.get_node(id)

    if not isinstance(self_node, Node):
        flash("找不到该目录")
        return render_template('error.html')

    children = self_node.get_node_child()

    parent_line = self_node.parent_line.split(',')
    parents = []
    if len(parent_line) > 0:
        parents = Node.get_node_parent(parent_line)
    parents.append(self_node)

    topic = self_node.topics

    return render_template('listing.html', itself=self_node, childs=children, parents=parents, topic=topic)


@app.route('/area/children/<area_id>')
def area_child(area_id):
    self_area = Area.get_area(area_id)

    if not isinstance(self_area, Area):
        flash("找不到该地域")
        return render_template('error.html')

    children = self_area.get_area_child()

    parent_line = self_area.parent_line.split(',')
    parents = []
    if len(parent_line) != 0:
        parents = Area.get_area_parents(parent_line)
    parents.append(self_area)

    topic = self_area.topics

    return render_template('area.html', itself=self_area, childs=children, parents=parents, topic=topic)


@app.route('/topic/<tpc_id>')
def topic(tpc_id):
    itself = Topic.get_topic(tpc_id)

    if not isinstance(itself, Topic):
        flash("找不到该话题")
        return render_template('error.html')

    user = itself.user

    node = itself.node
    nodes = []
    if node:
        parent_line = node.parent_line.split(',')
        nodes = Node.get_node_parent(parent_line)
        nodes.append(node)

    areas = []
    area = itself.area
    if area:
        area_line = area.parent_line.split(',')
        areas = Area.get_area_parents(area_line)
        areas.append(area)

    reply = itself.replies

    return render_template('topic.html', itself=itself, user=user, parents=nodes, areas=areas, reply=reply)


@app.route('/user/<int:user_id>')
def user(user_id):
    itself = User.get_user(user_id)
    status = 0
    topic = []
    if isinstance(itself, User):
        topic = itself.topics
        status = 1

    return render_template('user.html', status=status, itself=itself, topic=topic)
