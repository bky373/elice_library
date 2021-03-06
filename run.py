from elice_library import create_app, blueprint

app = create_app()
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
