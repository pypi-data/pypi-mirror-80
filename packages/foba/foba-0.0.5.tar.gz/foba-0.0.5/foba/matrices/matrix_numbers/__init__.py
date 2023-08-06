from foba.matrices.matrix_numbers.functions.identity_matrix import identity_matrix
from foba.matrices.matrix_numbers.functions.pascal_matrix import \
    lower_pascal_matrix, \
    symmetric_pascal_matrix, \
    upper_pascal_matrix
from foba.matrices.matrix_numbers.functions.zig_zag_matrix import zig_zag_matrix
from foba.utils import FooDict

matrix_collection = FooDict({
    'identity_matrix': identity_matrix,
    'upper_pascal_matrix': upper_pascal_matrix,
    'lower_pascal_matrix': lower_pascal_matrix,
    'symmetric_pascal_matrix': symmetric_pascal_matrix,
    'zig_zag_matrix': zig_zag_matrix,
})
