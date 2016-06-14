from flask import render_template
from .model import *
from application import app, session


@app.route('/area/parent_line')
def update_area():
    area = session.query(Area).filter_by(area_level=3).all()

    for area_child in area:
        parent_id = area_child.area_pid
        parent_line = []
        while parent_id != 21:
            parent = session.query(Area).filter_by(area_id=parent_id).first()
            if parent:
                parent_line.append(parent.area_id)
                parent_id = parent.area_pid

        if len(parent_line) > 1:
            parent_line = ','.join(parent_line)
        area_child.parent_line = parent_line
        session.commit()

    return render_template('status.html')


@app.route('/node/parent_line')
def update_node():
    node = session.query(Node).filter_by(nod_level=101).all()

    for node_child in node:
        parent_id = node_child.nod_pid
        parent_line = []
        while parent_id != 21:
            parent = session.query(Node).filter_by(node_id=parent_id).first()
            if parent:
                parent_line.append(parent.node_id)
                parent_id = parent.nod_pid

        if len(parent_line) > 1:
            parent_line = ','.join(parent_line)

        node_child.parent_line = parent_line

    session.commit()
    return render_template('status.html')
