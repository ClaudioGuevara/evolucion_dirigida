import pandas as pd
class Landscape:
	def __init__(self):
		#sequence is a string of residues
		self.array_residues = ["A","R","N","D","C","Q","E","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
	def run(self, sequence):
		data = []
		index_pos=1

		for index_pos,residue in enumerate(sequence):
			index_pos+=1
			if(residue in self.array_residues):
				for mutation in self.array_residues:
					if residue != mutation:
						data.append({"wild": residue, "position": index_pos, "mutant": mutation,
						"seq": self.__create_variant(sequence, residue, index_pos, mutation)})
		self.landscape = pd.DataFrame(data)
		return self.landscape
	def __create_variant(self, sequence, wild, position, mutated):
		if(sequence[position-1] == wild):
			sequence = sequence[:position-1] + mutated + sequence[position:]
			return sequence
		print("ERROR: {position} reside is not {wild}".format(position = position, wild = wild))
		return None