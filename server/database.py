from utils import *

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = SQLAlchemy(app)
app.app_context().push()


#TODO: oauthentication
@dataclass 
class User(database.Model):
    uid: str = database.Column("uid", database.String(128), primary_key=True)
    username: str = database.Column("username", database.String(100), nullable=False)
    password: str = database.Column("password", database.String(100), nullable=False)
    is_admin: bool = database.Column("is_admin", database.Boolean, nullable=False)
    created: datetime = database.Column("created", database.DateTime(timezone=True), default=database.func.now())
    sid: str = database.Column(database.String(128), database.ForeignKey("namespace.sid"), nullable=False)

class Oauth4User(database.Model):
    uid: str = database.Column("uid", database.String(128), database.ForeignKey("user.uid"), primary_key=True)
    token_type: str = database.Column("token_type", database.String(100), nullable=False)
    access_token: str = database.Column("access_token", database.String(100), nullable=False)
    refresh_token: str = database.Column("refresh_token", database.String(100), nullable=False)
    expires_in: int = database.Column("expires_in", database.Integer, nullable=False)

@dataclass
class Node(database.Model):
    nid: str = database.Column("nid", database.String(128), primary_key=True)
    Name: str = database.Column("Name", database.String(100), nullable=False)
    v4Address: str = database.Column("v4Address", database.String(100), nullable=False)
    v6Address: str = database.Column("v6Address", database.String(100), nullable=False)
    wgAddress: str = database.Column("wgAddress", database.String(100), nullable=False)
    MTU: int = database.Column("MTU", database.Integer, nullable=False)
    ListenPort: int = database.Column("ListenPort", database.Integer, nullable=False)
    #PrivateKey = database.Column("PrivateKey", database.String(100), nullable=False)
    PublicKey: str = database.Column("PublicKey", database.String(100), nullable=False)
    Endpoint: str = database.Column("Endpoint", database.String(100), nullable=True)
    AllowedIPs: str = database.Column("AllowedIPs", database.String(100), nullable=False)
    PersistentKeepalive: str = database.Column("PersistentKeepalive", database.Integer, nullable=False)
    sid: int = database.Column(database.Integer, database.ForeignKey("namespace.sid"), nullable=False)
    created: datetime = database.Column("created", database.DateTime(timezone=True), default=database.func.now())

@dataclass
class Namespace(database.Model):
    sid: str = database.Column("sid", database.String(128), primary_key=True)
    name: str = database.Column("Name", database.String(100), nullable=False)
    nodes: Node = database.relationship("Node", backref="namespace", lazy=True)