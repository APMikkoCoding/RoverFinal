import server

s = server.Server()
s.start()

height = int(input('Height of Box: '))
width = int(input('width of Box: '))

for i in range(height*width):
    s.step()