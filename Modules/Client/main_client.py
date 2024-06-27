import client


c = client.Client()
c.start(input("Host IP: "))


height = int(input('Height of Box: '))
width = int(input('width of Box: '))

for i in range(height*width):
    c.step()

