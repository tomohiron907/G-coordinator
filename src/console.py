
def print( message):
    #global main_window
    from window.main_window import app, main_window

    main_window.print_console(str(message))
    app.processEvents()