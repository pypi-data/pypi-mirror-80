import math
import pandas as pd

def valconf(x,eiknx):
  z=list(x)
  val=0
  i=0
  for x in z:
    j = int(x)
    val+=eiknx[i][j]
    i+=1
  return val

def DPAlgo(tau,aikn,eiknx):
  
  n = len(aikn) # no of devices
  C = round((math.log(1-tau))*100) # Required Accuracy
  #print(C)
  # compute aiknlog 
  aiknlog = [[0 for x in range(len(aikn[y]))] for y in range(n)]  
  for i in range(len(aikn)):
    for j in range(len(aikn[i])):
      aiknlog[i][j] = round((math.log(1-aikn[i][j]))*100)
    
  #print(aiknlog)
  
  # initialise configuration table 
  confi = [['' for x in range(-C+1)] for x in range(n+1)]
  z = [[0 for x in range(-C+1)] for x in range(n+1)] 
  con = ['','']
  
  # map negative values to positive index
  xi = []
  l = C
  for i in range(-C+1):
    xi.append(l)
    l+=1

  # Dynamic Programming
  for l in range(1,n+1):
    for d in range(-C+1):

      maxi = 0
      fcon = ''

      for x in range(len(eiknx[l-1])):

        val1=val2=val3=0

        # if accuracy of current configuration is greater than required accuracy
        # xi[d] is required accuracy
        
        if(xi[d]-aiknlog[l-1][x])>=0:
          val1 = z[l-1][xi.index(aiknlog[l-1][x]-xi[d])] + eiknx[l-1][x]
          con[0] = confi[l-1][xi.index(aiknlog[l-1][x]-xi[d])] + str(x)

        # if accuracy is less than combine with previous configuration  
        
        elif(z[l-1][xi.index(xi[d]-aiknlog[l-1][x])]>0):

          val2 = z[l-1][xi.index(xi[d]-aiknlog[l-1][x])]+eiknx[l-1][x]
          con[1] = confi[l-1][xi.index(xi[d]-aiknlog[l-1][x])] + str(x)

        val = max(val1,val2,val3)

        if(val>=maxi):
           for c in con: 
            if(val==valconf(c,eiknx)):
              fcon = c
            maxi = val

      z[l][d] = maxi
      confi[l][d] = fcon

  df1 = pd.DataFrame(z,columns=xi)
  df2 = pd.DataFrame(confi,columns=xi)
  #print(df1)
  final_confi = confi[n][xi.index(C)]
  final_configuration = list(final_confi)
  
  power = 0
  j = 0
  pacc = 1;
  for i in final_configuration:
    power += 1/eiknx[j][int(i)]
    j+=1
  j=0;
  
  for i in final_configuration:
    if aikn[j][int(i)]:
      pacc = pacc*(1-aikn[j][int(i)])
    j+=1
  
  #print("Power consumption")
  #print(power)
  
  #print("\nfinal configuration")
  #print("final",final_configuration)
  #print(1-pacc)
  return power,(1-pacc),final_configuration

def demo():
  c,a,b=DPAlgo(0.8,[[0.75,0.52, 0.49],[0.67, 0.57],[0.69, 0.52]],[[16, 54, 60],[14, 19],[39, 44]])
  print("DEMO : 3 Devices and 2 configurations")
  print("Accuracies list : [[0.75,0.52, 0.49],[0.67, 0.57],[0.69, 0.52]]")
  print("Energy consumption list : [[16, 54, 60],[14, 19],[39, 44]]")
  print("Energy :"+str(c))
  print("Accuracy :"+str(a))
  print("Config :"+str(b))