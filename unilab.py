from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

DB_NAME = "library.db"

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
db.create_all(app=app)

books = [
    {'title':'In Search of Lost Time ','author':'Marcel Proust','year':1913,'genre':'Modernist'},
    {'title':'Pride and Prejudice','author':'Jane Austen','year': 1813,'genre':'Romance novel'},
    {'title':'1984','author':'George Orwell','year': 1949,'genre':'Dystopian'},
    {'title':'The Great Gatsby','author':'F. Scott Fitzgerald','year': 1925,'genre':'Tragedy'},
    {'title':'Crime and Punishment','author':'Fyodor Dostoevsky','year': 1866,'genre':'Philosophical novel'},
    {'title':'Wuthering Heights','author':'Emily Brontë','year': 1847,'genre':'Romance'},
    {'title':'Of Mice and Men','author':'John Steinbeck','year': 1937,'genre':'Novels'},
    {'title':'Brave New World','author':'Aldous Huxley','year':1932 ,'genre':'Science Fiction'},


]


class LibraryBook(db.Model):
    __tablename__ = "library"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    author = db.Column(db.String(150),default='unknown')
    year = db.Column(db.Integer,nullable=False)
    genre = db.Column(db.String(150))

    def __repr__(self):
        return f"""
        Book:
        Title: {self.title}
        Author: {self.author}
        Year: {self.year}
        Genre: {self.genre}"""

def add_books(books):

    # db.create_all()
    for book in books:
        library_book = LibraryBook(
            title=book['title'],
            author=book['author'],
            year=book['year'],
            genre=book['genre']
        )
        db.session.add(library_book)
        db.session.commit()


resource_fields = {
    'id':fields.Integer,
    'title':fields.String,
    'author':fields.String,
    'year':fields.Integer,
    'genre':fields.String
}

book_put_args = reqparse.RequestParser()
book_put_args.add_argument("title",type=str,help="Book name is required",required=True)
book_put_args.add_argument('author',type=int,help="author name",required=True)
book_put_args.add_argument('year',type=int,help="Publish year of the book",required=True)
book_put_args.add_argument('genre',type=str,help="Book genre")

book_update_args = reqparse.RequestParser()
book_update_args.add_argument("title",type=str,help="Book name is required")
book_update_args.add_argument('author',type=int,help="author name")
book_update_args.add_argument('year',type=int,help="Publish year of the book")
book_update_args.add_argument('genre',type=str,help="Book genre")




class Book(Resource):
    @marshal_with(resource_fields)
    def get(self,book_id):
        result = LibraryBook.query.filter_by(id=book_id).first()
        if not result:
            abort(404,message="Could not find a book with that ID")

    @marshal_with(resource_fields)
    def post(self,book_id):
        args = book_put_args.parse_args()
        result = LibraryBook.query.filter_by(id=book_id).first()
        if result:
            abort(409,message="Book ID is taken...")

        book = LibraryBook(
            id = book_id,
            title = args['title'],
            author = args['author'],
            year = args['year'],
            genre = args['genre']
            )
        db.session.add(book)
        db.session.commit()
        return book, 201

    @marshal_with(resource_fields)
    def put(self,book_id):
        args = book_update_args.parse_args()
        result = LibraryBook.query.filter_by(id=book_id).first()
        if not result:
            abort(404,message="Book doesn`t exist, cannot update.")

        if args['title']:
            result.title = args['title']
        if args['author']:
            result.author = args['author']
        if args['year']:
            result.year = args['year']
        if args['genre']:
            result.genre = args['genre']

        db.session.commit()
        return result

    def delete(self,book_id):
        result = LibraryBook.query.filter_by(id=book_id).first()
        db.session.delete(result)
        db.session.commit()
        return f"Book with id {book_id} has been deleted"

api.add_resource(LibraryBook,"/book/<int:book_id>")

@app.before_first_request
def create_table():
    add_books()

if __name__ == '__main__':
    app.run(debug=True)