__all__ = (
    'Area',
    'Node',
    'Reply',
    'Topic',
    'Tag',
    'User',
)
from application import Base
from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, BIGINT, TEXT, SMALLINT, LONGTEXT, DOUBLE
from application import session
from sqlalchemy.orm import relationship


class Area(Base):
    __tablename__ = 'babel_area'
    aid = Column(INTEGER(10), primary_key=True)
    area_id = Column(BIGINT(20, unsigned=True), index=True, nullable=False, server_default='0')
    area_level = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    area_pid = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    area_name = Column(String(20), nullable=False)
    area_title = Column(String(20), nullable=False)
    parent_line = Column(String(40), server_default='0')
    area_order = Column(INTEGER(4, unsigned=True), nullable=False, server_default='0')
    area_bak1 = Column(String(255))
    area_bak2 = Column(String(255))
    area_bak3 = Column(BIGINT(20))
    area_bak4 = Column(BIGINT(20))

    topics = relationship("Topic")

    @staticmethod
    def get_area_parents(parent_line):
        return session.query(Area).filter(Area.area_id.in_(parent_line)).order_by(Area.area_level).all()

    def get_area_child(self):
        return session.query(Area).filter_by(area_pid=self.area_id).all()

    @staticmethod
    def get_area(area_id):
        return session.query(Area).filter_by(area_id=area_id).first()


class Node(Base):
    __tablename__ = 'babel_node'
    nid = Column(Integer, primary_key=True)
    node_id = Column(INTEGER(10), index=True, nullable=False, server_default='0')
    nod_pid = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='5')
    nod_uid = Column(INTEGER(10, unsigned=True), nullable=False, server_default='1')
    nod_sid = Column(INTEGER(10, unsigned=True), nullable=False, server_default='5')
    nod_level = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='2')
    nod_name = Column(String(100), nullable=False, server_default='node')
    nod_title = Column(String(100), nullable=False, server_default='Untitled node')
    nod_description = Column(TEXT)
    nod_header = Column(TEXT)
    nod_footer = Column(TEXT)
    nod_portrait = Column(String(40))
    nod_topics = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    nod_favs = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    nod_created = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    nod_lastupdated = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    nod_masterid = Column(Unicode(255))
    nod_mastername = Column(Unicode(40))
    nod_areaid = Column(INTEGER(10), index=True, server_default='0')
    nod_areaname = Column(Unicode(100))
    nod_order = Column(INTEGER(10), index=True)
    nod_bak1 = Column(String(255))
    nod_bak2 = Column(String(255))
    nod_bak3 = Column(BIGINT(20))
    nod_bak4 = Column(BIGINT(20))
    parent_line = Column(String(40), server_default='0')

    tags = relationship("Tag")
    topics = relationship("Topic")

    @staticmethod
    def get_node_parent(parent_line):
        return session.query(Node).filter(Node.node_id.in_(parent_line)).order_by(Node.nod_level).all()

    def get_node_child(self):
        return session.query(Node).filter_by(nod_pid=self.node_id).all()

    @staticmethod
    def get_node(id):
        return session.query(Node).filter_by(node_id=id).first()


class Reply(Base):
    __tablename__ = 'babel_reply'
    rpl_id = Column(Integer, primary_key=True)
    rpl_tpc_id = Column(INTEGER(10, unsigned=True), ForeignKey('babel_topic.tpc_id'))
    rpl_usr_id = Column(INTEGER(10, unsigned=True), index=True, nullable=False)
    rpl_post_nick = Column(String(192), nullable=False)
    rpl_post_usr_id = Column(INTEGER(10, unsigned=True), ForeignKey('babel_user.usr_id'))
    rpl_content = Column(TEXT, nullable=False)
    rpl_reply_content = Column(TEXT, nullable=False)
    rpl_status = Column(INTEGER(4, unsigned=True), index=True, nullable=False)
    rpl_created = Column(INTEGER(10, unsigned=True), index=True, nullable=False)
    rpl_bak1 = Column(TEXT, nullable=False)
    rpl_bak2 = Column(Unicode(250), nullable=False)
    rpl_bak3 = Column(INTEGER(10, unsigned=True), nullable=False)

    user = relationship("User")


class Topic(Base):
    __tablename__ = 'babel_topic'
    tpc_id = Column(INTEGER(10, unsigned=True), primary_key=True)
    tpc_pid = Column(INTEGER(10), ForeignKey('babel_node.node_id'))
    tpc_ppid = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_pppid = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_pname = Column(String(255))
    tpc_uid = Column(INTEGER(10, unsigned=True), ForeignKey('babel_user.usr_id'))
    tpc_title = Column(String(100), nullable=False, server_default='Untitled topic')
    tpc_description = Column(TEXT)
    tpc_content = Column(TEXT)
    tpc_hits = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    tpc_refs = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    tpc_posts = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    tpc_flag = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_created = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_lastupdated = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_lasttouched = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    tpc_status = Column(INTEGER(4, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_modtimes = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    tpc_moddate = Column(INTEGER(10, unsigned=True))
    tpc_check = Column(INTEGER(4, unsigned=True), index=True, nullable=False, server_default='0')
    tpc_checkdate = Column(INTEGER(10), server_default='0')
    tpc_checkmaster = Column(String(40))
    tpc_uname = Column(String(192))
    tpc_img1 = Column(String(100))
    tpc_img2 = Column(String(100))
    tpc_img3 = Column(String(100))
    tpc_img4 = Column(String(100))
    tpc_imgflag = Column(INTEGER(4, unsigned=True), nullable=False, server_default='0')
    tpc_areatext = Column(String(255))
    tpc_area = Column(BIGINT(20, unsigned=True), ForeignKey('babel_area.area_id'))
    tpc_pparea = Column(BIGINT(20), index=True)
    tpc_ppparea = Column(BIGINT(20), index=True)
    tpc_userip = Column(Unicode(255))
    tpc_bak1 = Column(Unicode(255))
    tpc_bak2 = Column(Unicode(255))
    tpc_bak3 = Column(BIGINT(20))
    tpc_bak4 = Column(BIGINT(20))

    replies = relationship("Reply")
    user = relationship("User")
    node = relationship("Node")
    area = relationship("Area")

    @staticmethod
    def get_topic(tpc_id):
        return session.query(Topic).filter_by(tpc_id=tpc_id).first()


class Tag(Base):
    __tablename__ = "babel_tag"
    tag_id = Column(INTEGER(10), primary_key=True)
    tag_name = Column(String(60), nullable=False)
    tag_node = Column(INTEGER(10), ForeignKey('babel_node.node_id'))
    tag_pid = Column(INTEGER(10), index=True, nullable=False, server_default='0')
    tag_level = Column(INTEGER(10), index=True, server_default='1')

    def get_tag_child(self):
        return session.query(Tag).filter_by(tag_pid=self.tag_id).all()



class User(Base):
    __tablename__ = "babel_user"
    usr_id = Column(INTEGER(10, unsigned=True), primary_key=True)
    usr_gid = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    usr_nick = Column(String(192), index=True, server_default='0')
    usr_password = Column(String(64), server_default='0')
    usr_email = Column(String(100), index=True, server_default='0')
    usr_full = Column(String(40))
    usr_addr = Column(String(200))
    usr_telephone = Column(String(40))
    usr_identity = Column(String(18))
    usr_gender = Column(SMALLINT(6), nullable=False, server_default='0')
    usr_birthday = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    usr_portrait = Column(String(40))
    usr_brief = Column(LONGTEXT)
    usr_money = Column(INTEGER(11, unsigned=True), nullable=False, server_default='0')
    usr_hits = Column(INTEGER(10), nullable=False, server_default='0')
    usr_api = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    usr_editor = Column(String(20), nullable=False, server_default='default')
    usr_created = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    usr_lastupdated = Column(INTEGER(10, unsigned=True), index=True, nullable=False, server_default='0')
    usr_qq = Column(String(40))
    usr_skype = Column(String(40))
    usr_otherlink = Column(String(40))
    usr_mobile = Column(String(40))
    usr_type = Column(INTEGER(10), index=True, nullable=False, server_default='0')
    usr_nodeid = Column(TEXT)
    usr_areaid = Column(String(255))
    usr_areaname = Column(String(255))
    usr_topics = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    usr_check = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    usr_del = Column(INTEGER(10, unsigned=True), nullable=False, server_default='0')
    usr_zipcode = Column(INTEGER(10), server_default='0')
    usr_mailcheck = Column(INTEGER(4, unsigned=True), nullable=False, server_default='0')
    usr_validcode = Column(String(255))
    usr_regip = Column(String(255))
    usr_bak1 = Column(String(255))
    usr_bak2 = Column(String(255))
    usr_bak3 = Column(BIGINT(20))
    usr_bak4 = Column(BIGINT(20))

    replies = relationship("Reply")
    topics = relationship("Topic")

    @staticmethod
    def get_user(user_id):
        return session.query(User).filter_by(usr_id=user_id).first()

# Base.metadata.create_all(engine)
