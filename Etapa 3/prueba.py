
from Oper.build.PR import *
from Oper.build.PT import *
from Oper.build.MEM import *
from Oper.build.DISK import *
from Oper.build.MMU import *

pt = PageTable()


pr = PageReplacement()
pr.imprimir()

mem = Memoria()
mem.imprimir()

disk = Disco()
disk.imprimir()

mmu = ManejoMemoria(disk,pt,mem,pr)
mmu.imprimir()

mmu.addOP("2+2")
mmu.addOP("3+1")
mmu.addOP("4+1")

mmu.addOP("14+1")

mmu.addOP("14+12")
