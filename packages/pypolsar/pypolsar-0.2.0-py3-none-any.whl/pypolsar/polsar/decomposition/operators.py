import numpy as np


class lex_vec(*args, **kwargs):
    
    def __init__(self, *args, **kwargs):
        self.name = "Lexicographic Scattering Vector"
        self.allowed_ndim = [4]
        self.blockprocess = True

    def lexicographic_scattering_vector(self, S_Matrix, *args, **kwargs):
        """
        𝑘⃗_3𝐿 =[ 𝑆_𝐻𝐻, √2 𝑆_𝐻𝑉, 𝑆_𝑉𝑉 ]𝑇
        """ 
        if not np.array_equal(S_Matrix[:,:,1], S_Matrix[:,:,2]):
            '''
            3.2.2 BISTATIC SCATTERING CASE
            4-D Lexicographic feature vector
            '''
            print('4-D Lexicographic feature vector')
            lex_vector = np.zeros((S_Matrix.shape[0], S_Matrix.shape[1], 4), dtype=complex)
            lex_vector[:,:,0] = S_Matrix[:,:,0]
            lex_vector[:,:,1] = S_Matrix[:,:,1]
            lex_vector[:,:,2] = S_Matrix[:,:,2]
            lex_vector[:,:,3] = S_Matrix[:,:,3]

        else:
            '''
            3.2.3 MONOSTATIC BACKSCATTERING CASE
            3-D Lexicographic feature vector
            '''
            print('3-D Lexicographic feature vector')
            lex_vector = np.zeros((S_Matrix.shape[0], S_Matrix.shape[1], 3), dtype=complex)
            lex_vector[:,:,0] = S_Matrix[:,:,0]
            lex_vector[:,:,1] = np.sqrt(2) * S_Matrix[:,:,1]
            lex_vector[:,:,2] = S_Matrix[:,:,3]
        return lex_vector

class pauli_vec(*args, **kwargs):
    
    def __init__(self, *args, **kwargs):
        self.name = "Pauli Scattering Vector"
        self.allowed_ndim = [4]

    def pauli_scattering_vector(self, S_Matrix, *args, **kwargs):    
        '''
        Pauli scattering vector
        𝑘⃗_3𝑃 = 1/√2 [ 𝑆_𝐻𝐻+𝑆_𝑉𝑉, 𝑆_𝐻𝐻−𝑆_𝑉𝑉, 2𝑆_𝐻𝑉 ]𝑇
        '''
        if not np.array_equal(S_Matrix[:,:,1], S_Matrix[:,:,2]):
            '''
            3.2.2 BISTATIC SCATTERING CASE
            4-D Pauli feature vector
            '''
            print('4-D Pauli feature vector')
            pauli_vector = np.zeros((S_Matrix.shape[0], S_Matrix.shape[1], 4), dtype=complex)
            pauli_vector[:,:,0] = S_Matrix[:,:,0] + S_Matrix[:,:,3]
            pauli_vector[:,:,1] = S_Matrix[:,:,0] - S_Matrix[:,:,3]
            pauli_vector[:,:,2] = S_Matrix[:,:,1] + S_Matrix[:,:,2]
            pauli_vector[:,:,3] = 1j*(S_Matrix[:,:,1] - S_Matrix[:,:,2])
            pauli_vector = pauli_vector/np.sqrt(2)
        else:
            '''
            3.2.3 MONOSTATIC BACKSCATTERING CASE
            3-D Pauli feature vector
            '''
            print('3-D Pauli feature vector')
            pauli_vector = np.zeros((S_Matrix.shape[0], S_Matrix.shape[1], 3), dtype=complex)
            pauli_vector[:,:,0] = S_Matrix[:,:,0] + S_Matrix[:,:,3]
            pauli_vector[:,:,1] = S_Matrix[:,:,0] - S_Matrix[:,:,3]
            pauli_vector[:,:,2] = 2*S_Matrix[:,:,1]
            pauli_vector = pauli_vector/np.sqrt(2)
        return pauli_vector