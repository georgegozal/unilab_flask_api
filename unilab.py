from crypt import methods
from flask import Flask, jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

# https://overiq.com/flask-101/database-modelling-in-flask/

DB_NAME = "library.db"

app = Flask(__name__)
# api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# db.init_app(app)
# db.create_all(app=app)
# db.create_all()

def create_database():
    db.create_all()
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

class LibraryBook(db.Model):
    # __tablename__ = "library"
    __tablename__ = "library_book"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(150),nullable=False)
    author = db.Column(db.String(150))#,default='unknown')
    year = db.Column(db.Integer,nullable=False)
    genre = db.Column(db.String(150))

    def __repr__(self):
        return f"""
        Title: {self.title}
        Author: {self.author}
        Year: {self.year}
        Genre: {self.genre}"""

# create_database()

@app.route('/')
def home():
    return """
        Hello to Api
        /api/books
        /api/book/book_id
        """

# get single book by id
@app.route('/api/book/<int:book_id>',methods=['GET'])
def get(book_id):
    book = LibraryBook.query.filter_by(id=book_id).first()
    if not book:
        abort(404,message="Could not find a book with that ID")
    else:
        return jsonify(
            {
                "id":book.id,
                "title":book.title,
                "author":book.author,
                "year":book.year,
                "genre":book.genre
                }
        )

# get all books list
@app.route('/api/books',methods=['GET'])
def get_all_books():
    books = LibraryBook.query.all()
    book_list = []
    for book in books:
        b = {
                "id":book.id,
                "title":book.title,
                "author":book.author,
                "year":book.year,
                "genre":book.genre
                }
            
        book_list.append(b)
    return jsonify(book_list)

    
@app.route('/api/book',methods=['POST'])
def post():
    # book = LibraryBook.query.filter_by(id=book_id).first()
    # if book:
    #     abort(409,message="Book ID is taken...")
        
    request_data = request.get_json()
    book = LibraryBook(
        title = request_data['title'],
        author = request_data['author'],
        year = request_data['year'],
        genre = request_data['genre']
        )
    db.session.add(book)
    db.session.commit()
    # print(book)
    b = {
                "id":book.id,
                "title":book.title,
                "author":book.author,
                "year":book.year,
                "genre":book.genre
                }
    return jsonify(book), 201


    # @marshal_with(resource_fields)
    # def put(self,book_id):
    #     args = book_update_args.parse_args()
    #     result = LibraryBook.query.filter_by(id=book_id).first()
    #     if not result:
    #         abort(404,message="Book doesn`t exist, cannot update.")

    #     if args['title']:
    #         result.title = args['title']
    #     if args['author']:
    #         result.author = args['author']
    #     if args['year']:
    #         result.year = args['year']
    #     if args['genre']:
    #         result.genre = args['genre']

    #     db.session.commit()
    #     return result

    # def delete(self,book_id):
    #     result = LibraryBook.query.filter_by(id=book_id).first()
    #     db.session.delete(result)
    #     db.session.commit()
    #     return f"Book with id {bminimalook_id} has been deleted"

# api.add_resource(LibraryBook,"/book/<int:book_id>")

# @app.before_first_request
# def before_first_request():
#     create_database()
#     # pass

if __name__ == '__main__':
    # create_database()
    app.run(debug=True,port=5000)