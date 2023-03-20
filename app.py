"""Flask app for Cupcakes"""
from flask import Flask,request,render_template,flash,jsonify
from models import connect_db, db, Cupcake
from forms import AddCupcake

app = Flask(__name__)

app.config['SECRET_KEY'] ="azertyqwerty"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


with app.app_context():
     connect_db(app)
     db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    form = AddCupcake()
    
    return render_template('index.html', form=form)

@app.route("/api/cupcakes", methods=["GET"])
def getAll_cupcakes():
    """Return all cupcakes in jason format."""

    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return (jsonify(cupcakes=cupcakes),200)


@app.route("/api/cupcakes", methods=["POST"])
def add_cupcake():
    """Add cupcake, and return data about new cupcake in json format."""
    new_cupcake = request.json

    cupcake = Cupcake(
        flavor=new_cupcake['flavor'],
        rating=new_cupcake['rating'],
        size=new_cupcake['size'],
        image=new_cupcake['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake in json format."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake and return updated data in json format."""

    new_cupcake = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = new_cupcake['flavor']
    cupcake.rating = new_cupcake['rating']
    cupcake.size = new_cupcake['size']
    cupcake.image = new_cupcake['image']

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message in json."""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

