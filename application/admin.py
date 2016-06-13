from flask import render_template
from flask import request

from .model import *
from application import app,session


@app.route('/admin/index')
def admin_index():
    rnt = {}
    nodes = session.query(Node).filter_by(nod_pid=21).all()
    rnt[21] = nodes
    list = [21, ]

    for x in list:
        for i in rnt[x]:
            two = session.query(Node).filter_by(nod_pid=i.node_id).all()
            if (two):
                rnt[i.node_id] = two
                list.append(i.node_id)

    return render_template('admin/index.html', start=21, rnt=rnt)


@app.route('/admin/show_tag/<int:node_id>')
def show_tag(node_id):
    node_title = session.query(Node).filter_by(node_id=node_id).first()
    rnt = {}
    tags = session.query(Tag).filter_by(tag_node=node_id).filter_by(tag_level=1).all()
    rnt[node_id] = tags

    for i in tags:
        two = session.query(Tag).filter_by(tag_pid=i.tag_id).all()
        if(two):
            rnt[i.tag_id] = two

    return render_template('/admin/show_tag.html',node_title = node_title,start = node_id,rnt = rnt)


@app.route('/admin/add_tag/<int:tag_node>/<int:tag_id>/<int:tag_level>')
def admin_add(tag_node,tag_id,tag_level):
    return render_template('admin/add_tag.html',tag_pid = tag_id, tag_node = tag_node,tag_level = tag_level)

@app.route('/admin/add_tag',methods=['POST'])
def add_node():
    tag = Tag()
    tag.tag_pid = request.form['tag_pid']
    tag.tag_level = request.form['tag_level']
    tag.tag_node = request.form['tag_node']
    tag.tag_name = request.form['tag_name']

    session.add(tag)
    session.commit()

    return admin_index()

