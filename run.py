from arnis_app import app
# from arnis_app.camera_source import camera, vs
# import threading

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(debug=True, threaded=True, use_reloader=False)

