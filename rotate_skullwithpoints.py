import Metashape
import math

def get_marker_position(chunk, label):
    """指定されたラベルのマーカー位置を返します。"""
    for marker in chunk.markers:
        if marker.label == label:
            return marker.position
    raise ValueError(f"Marker with label {label} not found")

def calculate_rotation_matrix(axis, angle):
    """指定された軸と角度に基づいて回転行列を計算します。"""
    if axis == 'x':
        rotation_matrix = Metashape.Matrix([[1, 0, 0, 0],
                                             [0, math.cos(angle), -math.sin(angle), 0],
                                             [0, math.sin(angle), math.cos(angle), 0],
                                             [0, 0, 0, 1]])
    elif axis == 'y':
        rotation_matrix = Metashape.Matrix([[math.cos(angle), 0, math.sin(angle), 0],
                                             [0, 1, 0, 0],
                                             [-math.sin(angle), 0, math.cos(angle), 0],
                                             [0, 0, 0, 1]])
    else:
        raise ValueError("Invalid axis")
    return rotation_matrix

def apply_rotation(chunk, rotation_matrix):
    """指定された回転行列をチャンクの変換行列に適用します。"""
    # チャンクの変換行列に適用
    chunk.transform.matrix = rotation_matrix * chunk.transform.matrix

# ドキュメントとアクティブなチャンクを取得
doc = Metashape.app.document
chunk = doc.chunk

# マーカーの位置を取得
point1 = get_marker_position(chunk, "point 1")
point2 = get_marker_position(chunk, "point 2")
point3 = get_marker_position(chunk, "point 3")
point4 = get_marker_position(chunk, "point 4")

# point 1とpoint 2のY,Z座標を揃えるためにX軸周りに回転
angle_x = math.atan2(point2.z - point1.z, point2.y - point1.y)
rotation_matrix_x = calculate_rotation_matrix('x', angle_x)
apply_rotation(chunk, rotation_matrix_x)

# point 3とpoint 4のY座標を揃えるためにY軸周りに再度回転
#angle_y = math.atan2(point4.x - point3.x, point4.z - point3.z)
#rotation_matrix_y = calculate_rotation_matrix('y', angle_y)
#apply_rotation(chunk, rotation_matrix_y)

print("Rotation applied successfully.")
