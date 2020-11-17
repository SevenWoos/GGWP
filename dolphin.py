import datetime
import time
import numpy as np
import re
import random
import string
import os
from urllib.request import urlopen

class Dolphins():
	#Creates the initial variables of the Dolphin
	def __init__(self, name, sex, mother, father, age = 0):
		self.name = name
		self.sex = sex
		self.mother = mother
		self.father = father
		self.death = np.random.randn()*5 + 35
		self.dead = False
		self.age = age
		self.years_since_procreation = 0
	
	#Increases age until death
	def age_record(self):
		#Increases age
		self.age += 1
		self.years_since_procreation += 1

		#If older than predicted death age, he/she dies
		if (self.age > self.death):
			self.dead = True
		return self.dead

	#Sees if this Dolphin and Second Dolphin can procreate
	def request_procreation(self, dolphin2):
		if (self.age >= 8 and dolphin2.age >= 8): #Both dolphins starting at the age of 8
			if (self.years_since_procreation >= 5 and dolphin2.years_since_procreation >= 5): #Both dolphins' years since procreation greater than or equal to 5
				if (dolphin2.mother != self.mother or dolphin2.father != self.father): #Their mothers and fathers are not the same
					if (10 >= np.abs(dolphin2.age - self.age)): #dolphins' age difference is less than or equal to 10 
						if (dolphin2.sex != self.sex): #Not same sex
							if (self.mother != dolphin2.name or self.father != dolphin2.name): #Dolphin's mother and father is not the second Dolphin
								if (self.dead == False and dolphin2.dead == False): #Cannot be dead
									self.years_since_procreation = 0
									dolphin2.years_since_procreation = 0
									return True
		return False

def get_names():
	os.remove("male_name_file.dat")
	os.remove("female_name_file.dat")

	#String to search for in HTML
	string = "name-details boy-names"
	stringf = "name-details girl-names"

	count = 1
	while (count <= 38):
		#Male and Female HTML Files
		url = "http://www.prokerala.com/kids/baby-names/boy/page-" + str(count) + ".html"
		urlf = "http://www.prokerala.com/kids/baby-names/girl/page-" + str(count) + ".html"
		infile = urlopen(url)
		infilef = urlopen(urlf)
		name_text = infile.read().decode("utf-8")
		name_textf = infilef.read().decode("utf-8")

		#Find Male names using male string
		text_idx = [(m.start(0), m.end(0)) for m in re.finditer(string, name_text)]
		temp = [re.search(">.*<", name_text[text_idx[x][0] + 40:text_idx[x][1] + 100]) for x in range(len(text_idx))]
		names = [m.group()[1:-1] for m in temp]

		#Find Female names using female string
		text_idxf = [(m.start(0), m.end(0)) for m in re.finditer(stringf, name_textf)]
		tempf = [re.search(">.*<", name_textf[text_idxf[x][0] + 40:text_idxf[x][1] + 200]) for x in range(len(text_idxf))]
		namesf = [m.group()[1:-1] for m in tempf]
		
		#This is because there are special characters not recognized by python on page 33 for girl names, on the 93rd name...
		if(count == 33):
			namesf[93] = namesf[93].strip("ÃÂ¸")

		#Write names into male and female files
		name_file = open("male_name_file.dat", "a")
		name_file.write("\n".join(names))
		name_filef = open("female_name_file.dat", "a")
		name_filef.write("\n".join(namesf))

		#Fix the bug that every 100 lines, 2 names are on the same line
		name_file.write("\n")
		name_filef.write("\n")

		count += 1

	#Close both files
	name_file.close()
	name_filef.close()

def gen_name(sex):
	#Choose name gender
	if (sex == "M"):
		file = "male_name_file.dat"
	else:
		file = "female_name_file.dat"
	
	name_file = open(file, "r")
	names = name_file.readlines()

	#Keep returning next name
	count = 0
	while (count < len(names)):
		yield names[count].rstrip("\n")
		count += 1

	#If we run out of names, make middle names
	count = 0
	while (count < len(names)):
		yield names[count].rstrip("\n") + " " + "".join([random.choice(string.ascii_letters) for n in range(10)])
	name_file.close()
