"By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above."

temp = open(r'../problem_data/p096_sudoku.txt')
raw_file = temp.read().splitlines()

sud = []
for i in range(50):
    sud.append(raw_file[1 + 10 * i:10 * (i + 1)])

# def sudoku_solver(x):
#	"""Inputs list of strings which when vertically stacked make a sudoku. Outputs the solution."""
#	r = set(x[0])
#	poss = []
#	j = x[0].find('0')
#	for j in xrange(9):
#		for i in xrange(9):
#			if x[j][i] != '0':
#				poss.append()


# Boris Borcic 2006
# Quick and concise Python 2.5 sudoku solver
# TODO: NEED TO CONVERT TO PYTHON 3 syntax

w2q = [[n / 9, n / 81 * 9 + n % 9 + 81, n % 81 + 162, n % 9 * 9 + n / 243 * 3 + n / 27 % 3 + 243] for n in range(729)]
q2w = (z[1] for z in sorted((x, y) for y, s in enumerate(w2q) for x in s))
q2w = map(set, zip(*9 * [q2w]))
w2q2w = [set(w for q in qL for w in q2w[q]) for qL in w2q]


class Completed(Exception): pass


def sudoku99(problem):
    givens = list(9 * j + int(k) - 1 for j, k in enumerate(problem[:81]) if '0' < k)
    try:
        search(givens, [9] * len(q2w), set(), set())
    except Completed as ws:
        return ''.join([str(w % 9 + 1) for w in sorted(ws.message)])


def search(w0s, q2nw, takens, ws):
    while 1:
        while w0s:
            w0 = w0s.pop()
            takens.add(w0)
            ws.add(w0)
            for q in w2q[w0]: q2nw[q] += 100
            for w in w2q2w[w0] - takens:
                takens.add(w)
                for q in w2q[w]:
                    n = q2nw[q] = q2nw[q] - 1
                    if n < 2:
                        w0s.append((q2w[q] - takens).pop())
        if len(ws) > 80:
            raise Completed(ws)
        w1, w0 = q2w[q2nw.index(2)] - takens
        try:
            search([w1], q2nw[:], takens.copy(), ws.copy())
        except KeyError:
            w0s.append(w0)


ans = 0

if __name__ == '__main__':
    for n in range(len(sud)):
        line = ''
        for i in range(9):
            line = line + sud[n][i]
        ans += int(sudoku99(line)[0:3])
print(ans)

