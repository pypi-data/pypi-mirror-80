from PIL import Image
import numpy as np


class Three60Cube:
    
    def __init__(self, path=None, template=None):
        
        # The Image
        # =========
        self.image = None
        self.image_array = None
        self.width = None
        self.height = None

        if template == None:
            
            # open image
            self.open_image(path)
            
            # The Sphere
            # ==========
            # radius image sphere
            self.R = self.width / (2 * np.pi)
            self.offset = int(self.R + 100)
            
            # create projection template
            self.cube_pane_normals = {
                0: np.array([1, 0, 0]),
                1: np.array([0, -1, 0]),
                2: np.array([-1, 0, 0]),
                3: np.array([0, 1, 0]),
                4: np.array([0, 0, 1]),
                5: np.array([0, 0, -1])
            }

            # pane side and 3D coordinates sphere
            self.XYZ = self._get_spherical_coordinates()
            # get nearest panes of all spherical coordinates
            self.projection_panes = self._detect_nearest_pane()

            # project 3D to 2D
            self.projections = self._project_to_cube()
            
            self.template = np.stack((
                self.projection_panes,
                self.projections[:, :, 0],
                self.projections[:, :, 1]
            ), axis=2)

            np.save('three60cube_template.npy', self.template)
        else:
            self.template = np.load(template)
            
            
    def open_image(self, path):
        self.image = Image.open(path)
        self.image_array = np.array(self.image)
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        
            
    def _get_spherical_coordinates(self):
        # 180 deg over <height> pixels, divide angles
        # in vertical plane
        ver_res = np.pi / self.height
        phi = np.tile(
            np.linspace(0, np.pi, num=self.height).reshape(-1,1),          
            (1, self.width)
        )
        # angles in horizontal plane
        theta = np.tile(
            np.linspace(0.25*np.pi, -1.75*np.pi, num=self.width+1), 
            (self.height, 1)
        )[:, :-1]
        X, Y, Z = self._sphere_to_cartesian(self.R, theta, phi)
        
        # reshape for concatenation <r, c> -> <r, c, 1>
        X = X[:, :, np.newaxis]
        Y = Y[:, :, np.newaxis]
        Z = Z[:, :, np.newaxis]
        
        return np.concatenate((X, Y, Z), axis=2)
        
        
    
    def _detect_nearest_pane(self):
        """Detect which pane a ray from the sphere will intersect with.
        Method: closest distance between sphere point and normal 
        vectors of cube panes. These normal vectors are the midpoints
        of the panes
        """
        rows = self.XYZ.shape[0]
        cols = self.XYZ.shape[1]
        # 6 distances
        distances = np.zeros((rows, cols, 6))

        for pane in sorted(self.cube_pane_normals.keys()):
            mid_point = self.cube_pane_normals[pane]
            distances[:, :, pane] = np.linalg.norm(
                self.XYZ[:, :, :] - np.tile(mid_point, (rows, cols, 1)), 
                axis=2
            )
            
        # convert into 3d matrix
        return np.argmin(distances, axis=2)
        
    
    @staticmethod
    def _sphere_to_cartesian(R, theta, phi):
        # convert spherical to cartesian
        X = R * np.sin(phi) * np.cos(theta)
        Y = R * np.sin(phi) * np.sin(theta)
        Z = R * np.cos(phi)
        return (X, Y, Z)
    
    
    # https://gist.github.com/TimSC/8c25ca941d614bf48ebba6b473747d72
    # vectorized line plane collision
    # XYZ: points on sphere, NORMS: normal vectors of plane where 
    # XYZ will intersect, PLANEP: plane-points in which XYZ
    # will intersect
    @staticmethod
    def vec_line_plane_collision(XYZ, NORMS, PLANEP):
        # dot product between 3d matrixes
        ndotu = np.einsum('ijk,ijk->ij', XYZ, NORMS)
        w = XYZ - PLANEP
        # again, einsum is dot-product
        si = (np.einsum('ijk,ijk->ij', -NORMS, w) / ndotu)[:, :, np.newaxis]
        psi = w + si * XYZ + PLANEP
        return psi
    
    
    def _project_to_cube(self):
        # create 3d cube projections first
        shape = self.XYZ.shape
        projections = np.zeros((shape[0], shape[1], 2))

        for pane in sorted(self.cube_pane_normals.keys()):
            # copy XYZ
            XYZ_copy = np.copy(self.XYZ)
            # create a mask for all vectors that are
            # projecting on the pane in question
            mask = self.projection_panes == pane

            # create normal vectors of pane and a vector
            # that exists on the pane to define the projection
            # pane
            normal = self.cube_pane_normals[pane]
            # now I need a point on the pane: take the absolute 
            # normal and see where it is 1 (->bool), reverse it
            # and add to normal
            pane_point = normal + ~(np.abs(normal) == True)
            
            # create a self.image_array-shape of normals and pane_points
            normal_vecs = np.tile(normal, (self.XYZ.shape[0], self.XYZ.shape[1], 1))
            pane_point_vecs = np.tile(pane_point, (self.XYZ.shape[0], self.XYZ.shape[1], 1))
            
            # in xyz exist points who will not intersect with 
            # the currect pane, set all irrelevant sphere coordinates
            # to normal vector
            XYZ_copy[~mask] = np.tile(normal * 2, (XYZ_copy[~mask].shape[0], 1))
            
            # create the projections
            projections_3d = self.vec_line_plane_collision(
                XYZ_copy,
                normal_vecs,
                pane_point_vecs
            )
            
            # convert into 2d and transform, the np.abs everywehere are a bit much
            if pane == 0:
                projections_3d = projections_3d[:, :, [2, 1]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] - 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] - 1)
                projections[mask] = projections_3d[mask]
            elif pane == 1:
                projections_3d = projections_3d[:, :, [2, 0]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] - 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] - 1)
                projections[mask] = projections_3d[mask]
            elif pane == 2:
                projections_3d = projections_3d[:, :, [2, 1]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] - 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] + 1)
                projections[mask] = projections_3d[mask]
            elif pane == 3:
                projections_3d = projections_3d[:, :, [2, 0]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] - 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] + 1)
                projections[mask] = projections_3d[mask]
            elif pane == 4:
                projections_3d = projections_3d[:, :, [0, 1]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] + 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] - 1)
                projections[mask] = projections_3d[mask]
            elif pane == 5:
                projections_3d = projections_3d[:, :, [0, 1]]
                projections_3d[:, :, 0] = np.abs(projections_3d[:, :, 0] - 1)
                projections_3d[:, :, 1] = np.abs(projections_3d[:, :, 1] - 1)
                projections[mask] = projections_3d[mask]

        return projections
    
    
    def get_projected_pane(self, pane=0, dim=900, fast=True, output='image'):
        # projection cube has size 2
        res = 2.0 / dim
        # create new image
        new_img = np.zeros((dim, dim, 3))
        
        mask = self.template[:, :, 0] == pane
        rgbs = self.image_array[mask]
        projections = self.template[:, :, 1:][mask]
        rows = np.floor_divide(projections[:, 0], res).astype(int)
        cols = np.floor_divide(projections[:, 1], res).astype(int)
        
        if fast == True:
            for i in range(rows.shape[0]):
                r = rows[i]
                c = cols[i]
                color = rgbs[i]
                if r < dim and c < dim:
                    new_img[r, c] = color
        else:
            # x + l*y is unique if l > x and l > y
            l_indexes = cols + 2*dim*rows

            for c in range(dim):
                for r in range(dim):
                    l = c + 2*dim*r
                    # find these indexes
                    l_mask = (l_indexes == l)
                    color_cluster = rgbs[l_mask]
                    # assign pixel of new image the average 
                    # of color cluster
                    new_img[r, c] = np.mean(color_cluster, axis=0)
         
        new_img = new_img.astype(np.uint8)

        if output == 'image':
            # convert array into image
            return Image.fromarray(new_img, 'RGB')
        else:
            # return just the array
            return new_img
