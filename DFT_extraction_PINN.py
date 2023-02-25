from  pymatgen.io import vasp
import os



def readInfo(filename):
     with open(filename,'r') as fo:
          info = fo.read().splitlines()
     return (info) 
         

def findElements(contar):
     ionTypesNumbers = []
     n = len(contcar[5].split())
     if(len(contcar[5].split())>2):
          print("Ions type are more than 2, this does not work please modified it!!!!!!")
          print("\n")
          abort()
     for i in range(n):
          ionTypesNumbers.append(contcar[5].split()[i])
     for j in range(n):     
          ionTypesNumbers.append(contcar[6].split()[j])
     return(ionTypesNumbers)



def findLatticesize(contar):
     return(contcar[1:5])



def findPositionForce(outcar):
     begin = 0
     ending = 0
     pos = []
     for lab1,line1 in enumerate(outcar):
          if "TOTAL-FORCE" in line1:
               begin = lab1 + 2
     for lab2,line2 in enumerate(outcar):
          if "total drift:" in line2:
               ending = lab2 - 1
     pos.append(begin)
     pos.append(ending)
     return(pos)





def ComponentPositionForce(outcar,pos):
     return(outcar[pos[0]:pos[1]])




def findTotalEnergy():
     return(vasp.Oszicar('OSZICAR'))




def wirteFile(filename,arrayPosForce,latbox,ionInfo,oszicar,systemInfo,dir):
     n = len(ionInfo)
     with open(filename,'a') as fw:
          fw.write(str(systemInfo)+str(" # Configuration name  "+str(dir)))
          fw.write("\n")
          for i in range(len(latbox)):
               for j in latbox[i].split():
                    fw.write(str(format(float(j),'.7f')))
                    fw.write(" ")
                    if(i==0):
                         fw.write(" # Universal scaling factor")
               fw.write("\n")
          if(n==4):
               fw.write(str(int(ionInfo[n-2])+int(ionInfo[n-1])))
          else:
               fw.write(str(int(ionInfo[1])))
          fw.write(" # number of species") 
          fw.write("\n")
          fw.write("C")   
          fw.write("  # Direct or Cartesian, only first letter is significant") 
          fw.write("\n")
          for k in range(len(arrayPosForce)):
               for l in arrayPosForce[k].split():
                    fw.write(str(format(float(l),'.7f')))
                    fw.write(" ")
               if(n==4):
                    if(k<=int(ionInfo[n-2])):
                         fw.write(str(ionInfo[0]))
                    else:
                         fw.write(str(ionInfo[n-3]))
               else:
                    fw.write(str(ionInfo[0]))
               

               fw.write("\n")    
          fw.write(str(format(float(oszicar.final_energy),'0.7f')))   
          fw.write(str(" # total energy"))  
          fw.write("\n")      
                    


if __name__ == '__main__':
     path = "/scratch/ikhatri/TaC_B1_SuperCells/MLTEST/DATA/"
     systemInfo = "t-Lammps-S111"
     dir_list = os.listdir(path)
     for dir in dir_list:
          print("working on:",dir)
          os.chdir(path+str(dir))
          contcar = readInfo("CONTCAR")
          outcar = readInfo("OUTCAR")
          print("Types of ions:",len(contcar[5].split()))
          print("ions are:",contcar[5].split()[0], contcar[5].split()[len(contcar[5].split())-1])
          print("number of ions of each type",contcar[6].split()[0], contcar[6].split()[len(contcar[5].split())-1])    
          ionInfo = findElements(contcar)
          latbox = findLatticesize(contcar)
          posInfo = findPositionForce(outcar)
          arrayPosForce = ComponentPositionForce(outcar,posInfo)
          oszicar = findTotalEnergy()
          print("energy:",oszicar.final_energy)
          os.chdir("../../")
          wirteFile("Info.dat",arrayPosForce,latbox,ionInfo,oszicar,systemInfo,dir)




