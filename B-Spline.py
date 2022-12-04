import numpy as np
from matplotlib import pyplot as plt

class BSpline:
    def __init__(self, control_points: np.array, p: int) -> None:
        self.knots_vector: np.array = None
        self.control_points: np.array = control_points
        self.points_fitted: np.array = None
        self.dim = self.control_points.shape[1]
        self.n = control_points.shape[0] - 1
        self.p = p
        self.m = self.n + self.p + 1

    def basis_function(self, i, p, u):
        vec = self.knots_vector
        if u >= vec[i] and u < vec[i+p+1]:
            if p == 0:
                return 1
            else:
                coefficient1 = (u - vec[i]) / (vec[i+p] - vec[i]) if vec[i+p] - vec[i] != 0 else 0
                coefficient2 = (vec[i+p+1] - u) / (vec[i+p+1] - vec[i+1]) if vec[i+p+1] - vec[i+1] != 0 else 0
                return coefficient1 * self.basis_function(i, p-1, u) + coefficient2 * self.basis_function(i+1, p-1, u)
        else:
            return 0
    
    def recursion_fit(self):
        #Definition Domain of Open B-Spline: [u_p, u_{m-p}] 
        domain_len = self.knots_vector[self.m-self.p]- self.knots_vector[self.p] 
        delta_u = domain_len / 10000
        fitted_num = int(domain_len / delta_u)+1
        self.points_fitted = np.zeros((fitted_num, self.dim)) 
        
        for idx in range(fitted_num):
            u = self.knots_vector[self.p] + idx * delta_u 
            point = np.zeros((self.dim))
            for i in range(self.n + 1):
                point += self.basis_function(i, self.p, u) * self.control_points[i]
            self.points_fitted[idx] =  point
        return self.points_fitted
    
    def plot(self):
        fig  = plt.figure()
        
        if self.dim == 2:     
            ax = fig.add_subplot()
            control_plot  = ax.scatter(self.control_points[:, 0], self.control_points[:, 1], c='red')
            fitted_plot = ax.scatter(self.points_fitted[:, 0], self.points_fitted[:, 1], c='green', s=3)
        if self.dim == 3:
            ax = fig.add_subplot(projection='3d')
            control_plot  = ax.scatter(self.control_points[:, 0], self.control_points[:, 1], self.control_points[:, 2],c='red')
            fitted_plot = ax.scatter(self.points_fitted[:, 0], self.points_fitted[:, 1], self.points_fitted[:, 2], c='green', s=3)
        
        plt.legend((control_plot, fitted_plot), ('control points', 'fitted points'), loc='best')
        
class ClampedBSpline(BSpline):
    def __init__(self, control_points: np.array, p: int) -> None:
        super().__init__(control_points, p)
        self.generate_knots_vector()

    def generate_knots_vector(self):
        self.knots_vector = np.zeros((self.m+1), dtype=float)
        uniform_num = self.m - 2 * self.p
        for i in range(uniform_num):
            self.knots_vector[i+self.p] = float(i) / float(uniform_num)
        self.knots_vector[self.p+uniform_num:] = 1
    
    def plot(self):
        super().plot()
        plt.title(f"Clamped BSpilne n={self.n} p={self.p} dim={self.dim}")
        plt.show()


class UniformBSpline(BSpline):
    def __init__(self, control_points: np.array, p: int) -> None:
        super().__init__(control_points, p)
        self.generate_knots_vector()

    def generate_knots_vector(self):
        self.knots_vector = np.array([i for i in range(self.m + 1)])
    
    def plot(self):
        super().plot()
        plt.title(f"Uniform BSpilne n={self.n} p={self.p} dim={self.dim}")
        plt.show()

if __name__ == '__main__':
    p = 3
    control_points_2d = np.array([[0, 0],[1, 0],[6, 5],[10, 8], [12, 8], [15, 6], [20, 6]])
    control_points_3d = np.array([[0, 0, 0],[1, 0, 5],[6, 5, 8],[10, 8, 6], [12, 8, 9], [15, 6, 2], [20, 6, 1]])
    print('-----TEST 2D UNIFORM BSPILINE------')
    uniform_bspline_2d = UniformBSpline(control_points_2d, p)
    uniform_bspline_2d.recursion_fit()
    uniform_bspline_2d.plot()
    print('------TEST 3D UNIFORM BSPILINE-----')
    uniform_bspline_3d = UniformBSpline(control_points_3d, p)
    uniform_bspline_3d.recursion_fit()
    uniform_bspline_3d.plot()
    print('-----TEST 2D CLAMPED BSPILINE------')
    clamped_bspline_2d = ClampedBSpline(control_points_2d, p)
    clamped_bspline_2d.recursion_fit()
    clamped_bspline_2d.plot()
    print('------TEST 3D CLAMPED BSPILINE-----')
    clamped_bspline_3d = ClampedBSpline(control_points_3d, p)
    clamped_bspline_3d.recursion_fit()
    clamped_bspline_3d.plot()
