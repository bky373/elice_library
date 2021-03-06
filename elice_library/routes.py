def add_namespaces(api):
    from elice_library.controllers.main_controller import api as main_ns
    from elice_library.controllers.auth_controller import api as auth_ns
    from elice_library.controllers.books_controller import api as books_ns
    from elice_library.controllers.comment_controller import api as comments_ns
    from elice_library.controllers.rental_controller import api as rental_ns

    api.add_namespace(main_ns, path="/")
    api.add_namespace(auth_ns)
    api.add_namespace(books_ns)
    api.add_namespace(comments_ns)
    api.add_namespace(rental_ns)
