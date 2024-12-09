from tarfile import data_filter
import Metashape
import csv
import os
import pprint

compatible_major_version = "2.1"
found_major_version = ".".join(Metashape.app.version.split('.')[:2])
if found_major_version != compatible_major_version:
	raise Exception("Incompatible Metashape version: {} != {}".format(found_major_version, compatible_major_version))

doc = Metashape.app.document
chunks = doc.chunks

"""
with open('I:\Scales.csv') as file:  
	reader = csv.reader(file)
	list = [row for row in reader] #listのなかに行ごとの集合として格納される。
	print(list)
"""
	
scale_data = [
	("target 1", "target 3", 200, 1),
	("target 2", "target 4", 200, 1),
	("target 5", "target 6", 200, 1),
	("target 5", "target 7", 282.8427, 1),
	("target 5", "target 8", 200, 1),
	("target 6", "target 8", 282.8427, 1),
	("target 7", "target 6", 200, 1),
	("target 7", "target 8", 200, 1),
	("target 9", "target 10", 70.45, 1),
	("target 10", "target 11", 70.45, 1),
	("target 11", "target 12", 70.45, 1),
	("target 12", "target 9", 70.45, 1),
	("target 16", "target 13", 100, 1),
	("target 13", "target 14", 100, 1),
	("target 14", "target 15", 100, 1),
	("target 15", "target 16", 99.6, 1),
	("target 10", "target 12", 100, 1),
	("target 9", "target 11", 100.1, 1),
	("target 13", "target 15", 141, 1),
	("target 14", "target 16", 141.4, 1),
	("target 17", "target 18", 99.6, 1),
	("target 19", "target 20", 99.8, 1),
	("target 21", "target 22", 49.6, 1),
	("target 23", "target 24", 49.6, 1),
]

new_marker_positions = {
	"target 1": (0, 0, 100),
	"target 2": (100, 0, 0),
	"target 3": (0, 0, -100),
	"target 4": (-100, 0, 0),
	"target 5": (100, 0, 100),
	"target 6": (100, 0, -100),
	"target 7": (-100, 0, -100),
	"target 8": (-100, 0, 100),
	"target 9": (0, 0, 50),
	"target 10": (50, 0, 0),
	"target 11": (0, 0, -50),
	"target 12": (-50, 0, 0),
	"target 13": (-50, 0, 50),
	"target 14": (50, 0, 50),
	"target 15": (50, 0, -50),
	"target 16": (-50, 0, -50),
	#"target 17": (0, 0, 0),
	#"target 18": (10, 0, 0),
	#"target 19": (0, 0, 0),
	#"target 20": (10, 0, 0),
	#"target 21": (0, 0, 0),
	#"target 22": (10, 0, 0),
	#"target 23": (0, 0, 0),
	#"target 24": (10, 0, 0),
	"target 157": (0, 0, 0)
}

accuracy = 2	#座標データ用の正確性。スケールバーより緩くしている

for chunk in doc.chunks:
	if chunk.enabled:
		print(f"Processing chunk: {chunk.label}")
		for p1_label, p2_label, dist, acc in scale_data:
			# マーカー検索
			scale1 = None
			scale2 = None
			for marker in chunk.markers:
				if marker.label == p1_label:
					scale1 = marker
				elif marker.label == p2_label:
					scale2 = marker
				if scale1 and scale2:
					break

			# スケールバーの追加
			if scale1 and scale2:
				scalebar = chunk.addScalebar(scale1, scale2)
				scalebar.reference.distance = float(dist)
				scalebar.reference.accuracy = float(acc)
				print(f"Added scalebar between {scale1.label} and {scale2.label}")
			else:
				print(f"Markers not found for: {p1_label}, {p2_label}")

		chunk.updateTransform()

for chunk in doc.chunks:
	if chunk.enabled:
		print(f"Processing chunk: {chunk.label}")
		for marker in chunk.markers:
			if marker.label in new_marker_positions:
				# 新しい座標を設定
				new_pos = new_marker_positions[marker.label]
				marker.position = Metashape.Vector([new_pos[0], new_pos[1], new_pos[2]])
				marker.accuracy = Metashape.Vector([accuracy, accuracy, accuracy])
				print(f"Updated marker {marker.label} position to {new_pos} with accuracy {accuracy}")
		
		chunk.updateTransform()
		print("Chunk transform updated.")