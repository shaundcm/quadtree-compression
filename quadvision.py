import numpy as np
from google.colab.patches import cv2_imshow
import cv2

#height, width = pic.shape[0:2]
#blank_image = np.zeros((height, width, 3))
#cv2_imshow(blank_image)

class Node:
  def __init__(self,xst,xend,yst,yend,avg):
    self.xst=xst
    self.xend=xend
    self.yst=yst
    self.yend=yend
    self.avg=avg
    self.children=[]

class quadtree:
  def __init__(self,img):
    self.img=img
    self.edge_img = np.zeros((img.shape[0], img.shape[1], 3))
    self.new_img = img
    self.root=Node(0,img.shape[1],0,img.shape[0],cv2.mean(img)[0:3])

  def showcompressed(self):
    cv2_imshow(self.new_img)

  def showedgedetect(self):
    cv2_imshow(self.edge_img)

  def fill(self, node):
    self.new_img[node.yst:node.yend, node.xst:node.xend] = node.avg
  '''
  def calcavg(self,xs,xe,ys,ye):
    return cv2.mean(self.img[ys:ye,xs:xe])[0:3]
  '''
  def calcavg(self, xs, xe, ys, ye):
    region = self.img[ys:ye, xs:xe]
    avg_color = np.mean(region, axis=(0, 1)).astype(np.uint8)
    return avg_color

  def calc_variance(self, xs, xe, ys, ye):
        region = self.img[ys:ye, xs:xe]
        variances = [np.var(region[:, :, i]) for i in range(3)]
        return np.mean(variances)


  def divide(self,node):
    if (node.xend - node.xst <= 1 or node.yend - node.yst <= 1):
    #if(node.xst-node.xend>-3 or node.yst-node.yend>-3):
      return
    x=(node.xst+node.xend)//2
    y=(node.yst+node.yend)//2

    sw=Node(node.xst,x,y,node.yend,self.calcavg(node.xst,x,y,node.yend))
    se=Node(x,node.xend,y,node.yend,self.calcavg(x,node.xend,y,node.yend))
    ne=Node(x,node.xend,node.yst,y,self.calcavg(x,node.xend,node.yst,y))
    nw=Node(node.xst,x,node.yst,y,self.calcavg(node.xst,x,node.yst,y))
    node.children=[sw,se,ne,nw]
    '''
    self.fill(nw)
    self.fill(ne)
    self.fill(se)
    self.fill(sw)
    '''
    self.divide(sw)
    self.divide(se)
    self.divide(ne)
    self.divide(nw)

  def compresshelper(self,node,tol):
    if not node.children:
      return

    childdiff=[]
    for child in node.children:
      childdiff.append(np.linalg.norm(np.array(child.avg)-np.array(node.avg)))

    childavg=np.mean(childdiff)
    region_variance = self.calc_variance(node.xst, node.xend, node.yst, node.yend)

    if childavg < tol or region_variance <5:
      newavg=self.calcavg(node.xst, node.xend, node.yst, node.yend)
      '''
      #threshold_color = np.array([50, 50, 50])
      threshold_color = np.clip(newavg - np.sqrt(region_variance),0, 255)
      '''
      node.avg = newavg #np.maximum(newavg, threshold_color)
      #node.avg = self.calcavg(node.xst, node.xend, node.yst, node.yend)
      self.fill(node)
      node.children = []

    else:
      for child in node.children:
        self.compresshelper(child,tol)

  def compress(self):
    #self.new_img.fill(255)
    self.divide(self.root)
    self.compresshelper(self.root,10)

  def edgehelper(self,node,tol,vtol):
    if not node.children:
      return

    childdiff=[]
    for child in node.children:
      childdiff.append(np.linalg.norm(np.array(child.avg)-np.array(node.avg)))

    childavg=np.mean(childdiff)
    region_variance = self.calc_variance(node.xst, node.xend, node.yst, node.yend)

    if childavg < tol or region_variance < vtol:
      self.edge_img[node.yst:node.yend, node.xst:node.xend]=[255,255,255]
      node.children = []

    else:
      for child in node.children:
        self.edgehelper(child,tol,vtol)

  def edgedetect(self,tol,vtol):
    self.divide(self.root)
    self.edgehelper(self.root,tol,vtol)
'''
pic1 = cv2.imread("/content/Screenshot 2023-04-05 000154.png")
qt1=quadtree(pic1)
qt1.edgedetect(9,6) #10,5
qt1.showedgedetect()
'''
path=input("Enter image path: ")
pic2= cv2.imread(path)
print("\n\noriginal image")
cv2_imshow(pic2)
qt2=quadtree(pic2)
qt2.compress()
print("\n\ncompressed image")
qt2.showcompressed()
qt2.edgedetect(8,7)
print("\n\nedge detected image")
qt2.showedgedetect()
