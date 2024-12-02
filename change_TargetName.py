import Metashape

# 現在のプロジェクトのドキュメントを取得
doc = Metashape.app.document

# 接頭辞の開始番号
prefix_number = 0

# プロジェクト内のすべてのチャンクをループ処理
for chunk in doc.chunks:
    # チャンク内のすべてのマーカー（ターゲット）に対してループ処理
    for marker in chunk.markers:
        # マーカーの名前に"Target"が含まれていて、"Point"が含まれていない場合にのみ名前を変更
        if "target" in marker.label and "point" not in marker.label:
            if "_" not in marker.label:
                # 新しい名前の設定（接頭辞_既存のマーカー名）
                new_name = f"{prefix_number}_{marker.label}"
                marker.label = new_name
        
    # 次のチャンク用に接頭辞の番号を更新
    prefix_number += 1

print("条件に一致するマーカー（ターゲット）の名前の更新が完了しました。")