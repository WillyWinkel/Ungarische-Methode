#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def findFreeNode(M, n):
	for x in xrange(0, n):
		frei = True
		for y in M:
			if x == y[0]:
				frei = False
		if frei:
			print "freier Knoten:", x
			return x

def frei(knoten, M, left=True):
	for (a,b) in M:
		if left:
			if a == knoten:
				return (b,a)
		else:
			if b == knoten:
				return (b,a)
	return True

def getPfad(B, r, w, Bad=True):
	ret = []
	for kante in B:
		if kante[0] == r:
			if Bad and kante[1] == w:
				return [r,w]
			reta = getPfad(B,kante[1], w, not Bad)
			if reta != []:
				print reta
				ret += [r] + reta
	return ret

def searchMvW(El, r, M, S, T, n):
	if r not in S:
		S.append(r)
	B = []
	# print "el:", El
	# print "S:", S
	# finde freien knoten aus S der kante aus El nach W-T hat
	for u in S:
		for (a,w) in El:
			if a == u:
				if w in range(0,n) and w not in T:
					# print "free edge:", (u,w)
					B.append((u,w))
					T.append(w)
					free = frei(w, M)
					if free == True:
						#abbruch und pfad melden
						return getPfad(B, r, w)
					else:
						B.append(free)
						S.append(free[1])
	return []

def method(matrix):
	maxCuw = 0
	n = len(matrix)
	for x in xrange(0,n):
		for y in xrange(0,n):
			if matrix.item(x, y) > maxCuw:
				maxCuw = matrix.item(x, y)
	
	U = dict((x,"u"+str(x)) for x in xrange(0,n))
	W = dict((x,"w"+str(x)) for x in xrange(0,n))
	Uinv = dict(("u"+str(x),x) for x in xrange(0,n))
	Winv = dict(("w"+str(x),x) for x in xrange(0,n))

	lU = [ 0 for x in xrange(0, n)]
	lW = [ maxCuw for x in xrange(0, n)]
	M = []
	S = []
	T = []
	Q = []

	print "Schleife zeile 4"
	while len(M) < n:
		for x in xrange(0, n):
			frei = True
			for y in M:
				if U[x] == y[0]:
					frei = False
			if frei:
				print x, "ist frei"
				S = [x]
				Q = [x]
				T = []
				B = []
				break
		print "Schleife zeile 9"
		none = False # damit wird der goto befehl aus zeile 19 realisiert
		assert len(Q) != 0
		while len(Q) > 0 and not none:
			r = Q[0]
			print "r:", r
			Q = Q[1:]
			print "Q:", Q
			# ganz El = [(x,y) for x in xrange(0,n) for y in xrange(0,n) if matrix.item(x,y) == lU[x] + lW[y]]
			print "lU", lU
			print "lW", lW
			El = [(x,y) for x in xrange(r,r+1) for y in xrange(0,n) if matrix.item(x,y) == lU[x] + lW[y]]
			print "El:", El
			for x in El:
				print "prüfe kante", x
				print "S:", S
				print "T:", T
				if x[1] not in T:
					w = x[1]
					print "Fall aus Zeile 12 trifft zu"
					T.append(w)
					B.append((U[x[0]],W[w]))
					none = True
					for (uu,ww) in M:
						if W[w] == ww:
							print "muss. weiter. rechnen."
							none = False
							S.append(Uinv[uu])
							B.append((W[w],uu))
							Q.append(Uinv[uu])
					if none:
						print "Vergrößere Matching"
						print "B:",B
						pfad = getPfad(B,U[r],W[w])
						print "mv weg von", r, "nach", w, "ist", pfad
						neu = [(pfad[x],pfad[x+1]) for x in xrange(0, len(pfad) - 1, 2)]
						alt = [(pfad[x],pfad[x+1]) for x in xrange(1, len(pfad) - 1, 2)]
						for x in alt:
							M.remove(x)
						for x in neu:
							M.append(x)
						print "neued M:", M
			if len(Q) == 0 and not none:
				alpha = min([lU[x] + lW[y] - matrix.item(x,y) for x in S for y in xrange(0,n) if y not in T])
				print "alpha:", alpha
				for u in S:
					for w in xrange(0,n):
						if w not in T:
							if lU[u] + lW[w] - matrix.item(u,w) == alpha:
								print "add", "U" + str(u), "to Q"
								Q.append(u)
				for u in S:
					lU[u] -= alpha
				for w in T:
					lW[w] += alpha
			print

		# ende schleife zeile 9
		# vergrossere M um p
	mm = [(Uinv[x],Winv[y]) for (x,y) in M]
	return mm

def auktion(matrix): # klappt nur für symetrische matrizen
	nb = len(matrix)
	n = nb
	delta = 1 / (1.0 * nb + 1)
	pj = [0] * nb
	owner = [-1] * nb
	Q = [x for x in xrange(0,n)]
	counter = 0
	while len(Q) > 0:
		i = Q[0]
		Q = Q[1:]
		print "betrachte bieter", i
		maxi = -1
		maxiJ = -1
		for j in xrange(0,n):
			wert = matrix.item(i,j) - pj[j]
			if wert > maxi:
				maxi = wert
				maxiJ = j
		assert maxiJ != -1
		print "biete jetzt auf", maxiJ, "mit", maxi
		if maxi > 0:
			if owner[maxiJ] != -1:
				Q.append(owner[maxiJ])
			owner[maxiJ] = i
			pj[maxiJ] += delta
		counter += 1
	print "brauchte", counter, "Runden"
	for x in xrange(0,n):
		if owner[x] != -1:
			yield (owner[x],x)



a = np.matrix('45 0 0 30; 50 55 15 0; 0 60 25 75; 45 0 5 35')
# a = np.matrix('3 4 5; 6 7 2; 2 1 3')
print a
print

# print "Ausgabe Auktion:"
# for x in auktion(a):
#	print x


m = method(a)
print "Ausgabe Ungarische Methode:"
print "Matching", m
suma = 0
for (x,y) in m:
	suma += a.item(x,y)
print "Gewicht des gefundenen Matchings:", suma



