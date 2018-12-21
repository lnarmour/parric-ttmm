import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime as dt


class AnimatedScatter(object):
    def __init__(self, N=10, interval=100, loop_order='ijk', TS=(10,10,10)):
        self.N = N
        self.fig = plt.figure()
        loop_str = '{}{}{}'.format(loop_order[0].upper(), loop_order[1].upper(), loop_order[2].upper())
        self.fig.suptitle('Matrix Multiplication (C=A*B), Loop Ordering {}, Tile Sizes {}'.format(loop_str, TS))
        self.ax1 = self.fig.add_subplot(131, aspect='equal')
        self.ax2 = self.fig.add_subplot(132, aspect='equal')
        self.ax3 = self.fig.add_subplot(133, aspect='equal')
        self.anim = FuncAnimation(self.fig, self.animate, init_func=self.setup_plot, interval=interval)
        self.stream = self.data_stream()
        self.Is = []
        self.Js = []
        self.Ks = []
        self.gen_points(N=N, loop_order=loop_order, TS=TS)

    def data_stream(self):
        for i,j,k in zip(self.Is, self.Js, self.Ks):
            yield (i,j,k)
            
    def setup_plot(self):    
        self.scatC_history = self.ax1.scatter([], [], marker='.')    
        self.scatC = self.ax1.scatter([], [])
        
        self.scatA_history = self.ax2.scatter([], [], marker='.')
        self.scatA = self.ax2.scatter([], [])
        
        self.scatB_history = self.ax3.scatter([], [], marker='.')
        self.scatB = self.ax3.scatter([], [])
        self.ax1.set_xlim([-1,self.N])
        self.ax1.set_ylim([-1*self.N,1])
        self.ax2.set_xlim([-1,self.N])
        self.ax2.set_ylim([-1*self.N,1])
        self.ax3.set_xlim([-1,self.N])
        self.ax3.set_ylim([-1*self.N,1])
        self.ax1.set_title('C')
        self.ax2.set_title('A')
        self.ax3.set_title('B')

    def animate(self, step):
        i,j,k = next(self.stream)
        A_pts = self.scatA.get_offsets()
        B_pts = self.scatB.get_offsets()
        C_pts = self.scatC.get_offsets()
        A_hist_pts = self.scatA_history.get_offsets()
        B_hist_pts = self.scatB_history.get_offsets()
        C_hist_pts = self.scatC_history.get_offsets()
        
        # plot next new point
        self.scatA.set_offsets(np.array([k,-1*i]))
        self.scatB.set_offsets(np.array([j,-1*k]))
        self.scatC.set_offsets(np.array([j,-1*i]))
        
        # update history points
        self.scatA_history.set_offsets(np.vstack((A_hist_pts, np.array([k,-1*i]))))
        self.scatB_history.set_offsets(np.vstack((B_hist_pts, np.array([j,-1*k]))))
        self.scatC_history.set_offsets(np.vstack((C_hist_pts, np.array([j,-1*i]))))
        
        
        self.ax1.set_title('C[{}][{}]'.format(i,j))
        self.ax2.set_title('A[{}][{}]'.format(i,k))
        self.ax3.set_title('B[{}][{}]'.format(k,j))
        
    def gen_points(self, N=10, step=1, loop_order='ijk', TS=(10,10,10)):
        mapping = {}
        ti_step,tj_step,tk_step = TS
        for ti in range(0,N,ti_step):
            for tj in range(0,N,tj_step):
                for tk in range(0,N,tk_step):
                    for i in range(ti, np.min([ti+ti_step, N]), step):
                        mapping['i'] = i
                        for j in range(tj, np.min([tj+tj_step, N]), step):
                            mapping['j'] = j
                            for k in range(tk, np.min([tk+tk_step, N]), step):
                                mapping['k'] = k
                                self.Is.append(mapping[loop_order[0]])
                                self.Js.append(mapping[loop_order[1]])
                                self.Ks.append(mapping[loop_order[2]])
        
    def show(self):
        plt.show()

# try the following examples:
#
# main(N=20, loop_order='ijk', TS=(5,5,5))
# main(N=20, loop_order='kji', TS=(5,5,5))
# main(loop_order=ikj', TS=(3,3,3))
# main(N=100, loop_order='ikj', TS=(10,5,20))
#
def main(N=10, interval=100, loop_order='ijk', TS=(10,10,10)):   
    a = AnimatedScatter(N=N, interval=interval, loop_order=loop_order, TS=TS)
    a.show()

