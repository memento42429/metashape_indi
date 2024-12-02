import Metashape
import math

def get_marker_position(chunk, label):
    """指定されたラベルのマーカー位置を返します。"""
    for marker in chunk.markers:
        if marker.label == label:
            return marker.position
    raise ValueError(f"Marker with label {label} not found")

def calculate_rotation_matrix(axis_vector, angle):
    """指定された軸ベクトルと角度に基づいて回転行列を計算します。"""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    x, y, z = axis_vector
    rotation_matrix = Metashape.Matrix([[cos_angle + x**2 * (1 - cos_angle), x*y*(1-cos_angle) - z*sin_angle, x*z*(1-cos_angle) + y*sin_angle, 0],
                                         [y*x*(1-cos_angle) + z*sin_angle, cos_angle + y**2*(1-cos_angle), y*z*(1-cos_angle) - x*sin_angle, 0],
                                         [z*x*(1-cos_angle) - y*sin_angle, z*y*(1-cos_angle) + x*sin_angle, cos_angle + z**2*(1-cos_angle), 0],
                                         [0, 0, 0, 1]])
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
print(point1)
print(point2)
print(point3)
print(point4)

# 点1から点2へのベクトルを計算し、X軸方向ベクトルとして使用
axis_vector = [point2.x - point1.x, point2.y - point1.y, point2.z - point1.z]
# ベクトルの長さを計算
vector_length = math.sqrt(sum(coord**2 for coord in axis_vector))
# 正規化
axis_vector = [coord / vector_length for coord in axis_vector]

# X軸方向ベクトルが正しいことを確認
print("Axis vector:", axis_vector)

# X軸方向ベクトルを使用して回転角度を計算
angle_x = math.atan2(axis_vector[2], axis_vector[1])
rotation_matrix_x = calculate_rotation_matrix(axis_vector, angle_x)
apply_rotation(chunk, rotation_matrix_x)

print("Rotation around X-axis applied successfully.")
