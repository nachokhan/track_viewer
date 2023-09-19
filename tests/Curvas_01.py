import matplotlib.pyplot as plt

from tests.prob_curvas import puntos_1 as pts1
from tests.prob_curvas import puntos_2 as pts2
from tests.prob_curvas import puntos_3 as pts3
from tests.prob_curvas import puntos_4 as pts4
from tests.prob_curvas import contar_curvas as contar

def RevisarCurvas(pts):
    a,b,c = contar(pts, 45)
    print("Curvas: ", a)
    return c

def main():

    fig = plt.figure(figsize=(55, 25))
    fig.suptitle("CURVES", size="xx-large")
    grid = plt.GridSpec(2, 2, wspace=0.5, hspace=0.5)
    ax1 = fig.add_subplot(grid[0, 1])
    ax2 = fig.add_subplot(grid[1, 1])
    ax3 = fig.add_subplot(grid[1, 0])
    ax4 = fig.add_subplot(grid[0, 0])
    
    a1 = RevisarCurvas(pts1)
    a2 = RevisarCurvas(pts2)
    a3 = RevisarCurvas(pts3)
    a4 = RevisarCurvas(pts4)

    ejex1 = [(p[0]) for p in pts1]
    ejey1 = [(p[1]) for p in pts1]
    ejex2 = [(p[0]) for p in pts2]
    ejey2 = [(p[1]) for p in pts2]
    ejex3 = [(p[0]) for p in pts3]
    ejey3 = [(p[1]) for p in pts3]
    ejex4 = [(p[0]) for p in pts4]
    ejey4 = [(p[1]) for p in pts4]

    ax1.plot(ejex1, ejey1, color = "blue")
    ax2.plot(ejex2, ejey2, color = "blue")
    ax3.plot(ejex3, ejey3, color = "blue")
    ax4.plot(ejex4, ejey4, color = "blue")

    scat1x = [(pts1[p][0]) for p in a1]
    scat1y = [(pts1[p][1]) for p in a1]
    scat2x = [(pts2[p][0]) for p in a2]
    scat2y = [(pts2[p][1]) for p in a2]
    scat3x = [(pts3[p][0]) for p in a3]
    scat3y = [(pts3[p][1]) for p in a3]
    scat4x = [(pts4[p][0]) for p in a4]
    scat4y = [(pts4[p][1]) for p in a4]

    ax1.scatter(scat1x, scat1y, color = "green")
    ax2.scatter(scat2x, scat2y, color = "green")
    ax3.scatter(scat3x, scat3y, color = "green")
    ax4.scatter(scat4x, scat4y, color = "green")

    plt.show()
