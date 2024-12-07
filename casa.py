import numpy as np
import matplotlib.pyplot as plt

po = np.array([[1,1,1,1],[3,1,1,1],[3,3,1,1],[2,4,1,1],[1,3,1,1], # house: front points
               [1,1,4,1],[3,1,4,1],[3,3,4,1],[2,4,4,1],[1,3,4,1], # house: back points
               [1.7,1,1,1],[1.7,2.3,1,1],[2.3,2.3,1,1],[2.3,1,1,1]]) # house: door points

pFront = np.array([po[0],po[1],po[2],po[3],po[4],po[0]])
pBack = np.array([po[5],po[6],po[7],po[8],po[9],po[5]])
pCeil = np.array([po[4],po[2],po[7],po[9],po[4]])
pFloor = np.array([po[0],po[1],po[6],po[5],po[0]])
pRoof = np.array([po[3],po[8]])
pDoor = np.array([po[10],po[11],po[12],po[13]])

pFront = np.transpose(pFront)
pBack = np.transpose(pBack)
pCeil = np.transpose(pCeil)
pFloor = np.transpose(pFloor)
pRoof = np.transpose(pRoof)
pDoor = np.transpose(pDoor)

end_loop = False
projection_plane = 'XY'
perspective_x = 0.
perspective_y = 0.
perspective_z = 0.
scale_object = 1.
theta_y = 0
theta_x = 0

def on_key(event):
    global end_loop
    global projection_plane
    global perspective_x
    global perspective_y
    global perspective_z
    global scale_object
    global points
    global theta_x
    global theta_y

    if event.key == 'escape': 
        end_loop = True
    elif event.key == '0': 
        print('you pressed', event.key)
    elif event.key == '1': 
        print('you pressed', event.key)
    elif event.key == '2': 
        print('you pressed', event.key)
    elif event.key == '3': 
        print('you pressed', event.key)
    elif event.key == 'x': 
        print('you pressed', event.key)
    elif event.key == 'X': 
        print('you pressed', event.key)
    elif event.key == 'y': 
        print('you pressed', event.key)
    elif event.key == 'Y': 
        print('you pressed', event.key)
    elif event.key == 'z': 
        print('you pressed', event.key)
    elif event.key == 'Z': 
        print('you pressed', event.key)
    elif event.key == 'up':
        print('you pressed', event.key)
        theta_x += 5
    elif event.key == 'down':  
        print('you pressed', event.key)
        theta_x -= 5
    elif event.key == 'left':     
        print('you pressed', event.key)
        theta_y += 5
    elif event.key == 'right': 
        print('you pressed', event.key)
        theta_y -= 5

def on_press(event):
    global scale_object
    if event.button==1: #pressed LEFT button
        print('you pressed left mouse button', event.xdata, event.ydata)
    elif event.button==3: #pressed RIGHT button
        print('you pressed right mouse button', event.xdata, event.ydata)

def find_house_center(pBack,pFront,pCeil,pFloor,pRoof,pDoor):
    xs = np.concatenate((pFront[0], pBack[0], pCeil[0], pFloor[0], pRoof[0], pDoor[0]))
    ys = np.concatenate((pFront[1], pBack[1], pCeil[1], pFloor[1], pRoof[1], pDoor[1]))
    zs = np.concatenate((pFront[2], pBack[2], pCeil[2], pFloor[2], pRoof[2], pDoor[2]))
    min_x = np.min(xs)
    max_x = np.max(xs)
    min_y = np.min(ys)
    max_y = np.max(ys)
    min_z = np.min(zs)
    max_z = np.max(zs)
    return np.array([(min_x+max_x)/2, (min_y+max_y)/2, (min_z+max_z)/2])

def translation_matrix(dx,dy,dz):
    return np.array([[1, 0, 0, dx],
                     [0, 1, 0, dy],
                     [0, 0, 1, dz],
                     [0, 0, 0, 1]])

def rotation_matrix_y(theta):
    # theta in radians
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[cos , 0, sin, 0],
                     [0   , 1, 0  , 0],
                     [-sin, 0, cos, 0],
                     [0   , 0, 0  , 1]])

def rotation_matrix_x(theta):
    # theta in radians
    cos = np.cos(theta)
    sin = np.sin(theta)
    return np.array([[1, 0  , 0   , 0],
                     [0, cos, -sin, 0],
                     [0, sin, cos , 0],
                     [0, 0  , 0   , 1]])

def deg_to_rad(deg):
    return deg*np.pi/180

def projection_matrix(x, y, z):
    return np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [x, y, z, 1]])

def normalize(face):
    m, n = face.shape
    for j in range(n):
        face[:, j] = face[:, j] / face[m-1, j]
    return face

def anima(pBack,pFront,pCeil,pFloor,pRoof,pDoor):
    # find house center
    house_center = find_house_center(pBack,pFront,pCeil,pFloor,pRoof,pDoor)

    # transformation to translate center of house to origin
    Tlc = translation_matrix(-house_center[0],-house_center[1],-house_center[2])

    # closes all existing figures
    plt.close('all')    
    fig, ax = plt.subplots()
   
    # register callback functions
    cid = fig.canvas.mpl_connect('key_press_event', on_key)
    cid = fig.canvas.mpl_connect('button_press_event', on_press)
    
    while not end_loop:
        # clear axis
        ax.cla()

        # assemble transformation matrixes
        Rx = rotation_matrix_x(deg_to_rad(theta_x))
        Ry = rotation_matrix_y(deg_to_rad(theta_y))
        P = projection_matrix(0, 0, 0.1)

        T = np.dot(Rx, Tlc)
        T = np.dot(Ry, T)
        T = np.dot(P , T)

        # apply transformations to house points
        pFront2 = normalize(np.dot(T, pFront))
        pBack2  = normalize(np.dot(T, pBack))
        pCeil2  = normalize(np.dot(T, pCeil))
        pFloor2 = normalize(np.dot(T, pFloor))
        pRoof2  = normalize(np.dot(T, pRoof))
        pDoor2  = normalize(np.dot(T, pDoor))

        # plot transformed house points
        ax.plot(pFront2[0], pFront2[1], 'r')
        ax.plot(pBack2[0] , pBack2[1] , 'r')
        ax.plot(pCeil2[0] , pCeil2[1] , 'r')
        ax.plot(pFloor2[0], pFloor2[1], 'r')
        ax.plot(pRoof2[0] , pRoof2[1] , 'r')
        ax.plot(pDoor2[0] , pDoor2[1] , 'r')
        ax.set_aspect('equal')

        # plt.show()
        fig.canvas.draw()
        plt.pause(0.01)

# execute animation
anima(pBack,pFront,pCeil,pFloor,pRoof,pDoor)
plt.close('all')    # Closes all existing figures
