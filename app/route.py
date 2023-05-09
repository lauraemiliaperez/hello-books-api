from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request, abort


books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

#helper functions


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model



@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    # new_book = Book(title=request_body["title"],
    #                 description=request_body["description"])
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response)

    # books_response = []

    # title_query = request.args.get("title")
    # title_query_id = request.args.get("id")
    # if title_query:
    #     books = Book.query.filter_by(title = title_query)
    # elif title_query_id:
    #     books = Book.query.filter_by(id=title_query_id)
    # else:
    #     books = Book.query.all()

    
    # for book in books:
    #     books_response.append(
    #         {
    #             "id": book.id,
    #             "title": book.title,
    #             "description": book.description
    #         }
    #     )
    # return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book,book_id)
    return book.to_dict()


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book,book_id)
    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully updated"))


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book,book_id)

    db.session.delete(book)
    db.session.commit()
#no jsonify:
    return make_response(jsonify(f"Book #{book_id} successfully deleted"))




#Author routes:

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"])

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)


@authors_bp.route("", methods=["GET"])
def read_all_authors():

    authors = Author.query.all()

    authors_response = []
    for author in authors:
        authors_response.append(
            {
                "name": author.name
            }
        )
    return jsonify(authors_response)

#this route creates a book for an author
@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book_for_author(author_id):
    #validation for id
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"],
                    author=author)
    # new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)


#this route gets all books from an author
@authors_bp.route("/<author_id>/books", methods=["GET"])
def get_all_books_from_author(author_id):
    author = validate_model(Author, author_id)

    books_response = []
    for book in author.books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return jsonify(books_response)

