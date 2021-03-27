from flask import *
import pygame

#pygame.init()
#win = pygame.display.set_mode((500,500))

app = Flask(__name__)   #creates the application flask



#image = pygame.image.load("logo.jpg")


'''
while True:
    win.blit(image,(0,0))
    pygame.display.update()
'''

@app.route("/")
def test2():
    return render_template("imageTest.html", logoImage = "logo.jpg")



if __name__ == "__main__":      #runs the application
    app.run()     #debug allows us to not have to refresh every time 


