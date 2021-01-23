import threading,time ,sys, random, webview,io



html = open('GUI/index.html').read()

"""
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }

    label {
        margin-left: 0.3rem;
        margin-right: 0.3rem;
    }

    button {
        font-size: 100%;
        padding: 0.5rem;
        margin: 0.3rem;
        text-transform: uppercase;
    }

</style>
</head>
<body>


<h1>JS API Example</h1>
<p id='pywebview-status'><i>pywebview</i> is not ready</p>

<button onClick="initialize()">Hello Python</button><br/>
<button id="heavy-stuff-btn" onClick="doHeavyStuff()">Perform a heavy operation</button><br/>
<button onClick="getRandomNumber()">Get a random number</button><br/>
<label for="name_input">Say hello to:</label><input id="name_input" placeholder="put a name here">
<button onClick="greet()">Greet</button><br/>
<button onClick="catchException()">Catch Exception</button><br/>


<div id="response-container"></div>

</body>
</html>
"""


class WebApi:
    def __init__(self):
        pass

    def error(self):
        raise Exception('This is a Python exception')

    def quit(self):
        window.destroy()
        print('quiting python')
        exit()



if __name__ == '__main__':
    api = WebApi()
    window = webview.create_window('API example', url="./GUI/index.html",frameless=True,resizable=False,width=772, height=556,easy_drag=True,js_api=api)
    webview.start(debug=True,http_server=True)