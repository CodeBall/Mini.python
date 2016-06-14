from flask import render_template
from flask import flash
from .model import *
from application import app, session
from flask_restful import reqparse


@app.route('/admin/index')
def admin_index():
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

    return render_template('admin/index.html', start=21, rnt=rnt)


@app.route('/admin/show_tag/<int:node_id>')
def show_tag(node_id):
    node_title = Node.get_node(node_id)
    rnt = {}
    tags = session.query(Tag).filter_by(tag_node=node_id).filter_by(tag_level=1).all()
    rnt[node_id] = tags

    for i in tags:
        two = i.get_tag_child()
        if two:
            rnt[i.tag_id] = two

    return render_template('/admin/show_tag.html', node_title=node_title, start=node_id, rnt=rnt)


@app.route('/admin/add_tag/<int:tag_node>/<int:tag_id>/<int:tag_level>')
def admin_add(tag_node, tag_id, tag_level):
    return render_template('admin/add_tag.html', tag_pid=tag_id, tag_node=tag_node, tag_level=tag_level)


@app.route('/admin/add_tag', methods=['POST'])
def add_node():
    parser = reqparse.RequestParser()
    parser.add_argument('tag_pid', type=str, required=True)
    parser.add_argument('tag_level', type=str, required=True)
    parser.add_argument('tag_node', type=str, required=True)
    parser.add_argument('tag_name', type=str, required=True)
    args = parser.parse_args()

    if len(args['tag_pid']) == 0 or len(args['tag_level']) == 0 or len(args['tag_node']) == 0:
        flash("不能够为空目录添加属性,请走正确渠道")
        return render_template('error.html')
    if len(args['tag_name']) == 0:
        flash("属性名不能为空")
        return admin_add(args['tag_node'], args['tag_pid'], args['tag_level'])

    tag = Tag()
    tag.tag_pid = args['tag_pid']
    tag.tag_level = args['tag_level']
    tag.tag_node = args['tag_node']
    tag.tag_name = args['tag_name']

    session.add(tag)
    session.commit()

    return admin_index()
