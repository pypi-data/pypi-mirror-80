def gdrive():
    try:
        from google.colab import drive
        drive.mount(os.path.join(os.getcwd(), "gdrive"))
    except:
        print('It only works with colab!!')
    
