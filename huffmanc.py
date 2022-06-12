import heapq
import os
import json
import ast
import math
import sys
import pickle

from numpy.distutils.fcompiler import none

"""
author: Bhrigu Srivastava
website: https:bhrigu.me
"""


class HuffmanCoding:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, self.HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text



	def pad_huffman_tree_text(self, huffman_tree_text):
		extra_padding = 8 - len(huffman_tree_text) % 8
		for i in range(extra_padding):
			huffman_tree_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		tree_text =  huffman_tree_text + padded_info
		return tree_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b

	def get_tree_info(self):
		dict_encode_data = pickle.dumps(self.reverse_mapping)

		tree= bytearray(dict_encode_data)
		return tree

	def calculate_size(self, size, huffmantree):
		if (size > 255):
			loop = math.floor(size / 255)
			huffmantree.append(size % 255)
			huffmantree.append(loop)
			flag = 1
			huffmantree.append(flag)
		else:
			flag = 0
			huffmantree.append(size)
			huffmantree.append(flag)
		return huffmantree

	def compress(self):
		text = self.path
		text = text.rstrip()

		frequency = self.make_frequency_dict(text)
		self.make_heap(frequency)
		self.merge_nodes()
		self.make_codes()

		encoded_text = self.get_encoded_text(text)
		padded_encoded_text = self.pad_encoded_text(encoded_text)

		huffmantreedata = self.get_tree_info()

		b = self.get_byte_array(padded_encoded_text) # bu byteları embede
		huffmantreedata = self.calculate_size(len(huffmantreedata), huffmantreedata)

		bytelar = b + huffmantreedata

		return bytelar


	""" functions for decompression: """


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1 * extra_padding]

		return encoded_text

	def remove_huffman_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[-8:]

		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1 * extra_padding]
		return encoded_text


	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""
		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text

	def reconstruct_tree(self,huffmantree):
		res_dict = pickle.loads(huffmantree)
		self.reverse_mapping = res_dict

	def decompress(self, bytelar):
		output_path = "_decompressed" + ".txt"
		if(int.from_bytes(bytelar[-1:], "big") == 1):
			loop = int.from_bytes(bytelar[-2: -1], "big")
			mod =  int.from_bytes(bytelar[-3:-2], "big")
			huffmantreesize = loop * 255 + mod + 2
			huffmantree = bytelar[-huffmantreesize -1:-3]
		elif(int.from_bytes(bytelar[-1:], "big") == 0):
			print("elseteiym")
			huffmantreesize = int.from_bytes(bytelar[-2: -1], "big")
			huffmantree = bytelar[-huffmantreesize - 2:-2]

		input_bytes = bytelar[:-huffmantreesize-1]
		bit_string = ''.join(format(byte, '08b') for byte in input_bytes)

		self.reconstruct_tree(huffmantree)
		encoded_text = self.remove_padding(bit_string)

		decompressed_text = self.decode_text(encoded_text)
		return decompressed_text

