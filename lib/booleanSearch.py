class BooleanSearch:
    def __init__(self, index, documents):
        self.index = index
        self.documents = documents

    def b_and(self, left, right):
        # This is effective thanks to the fact that left and right are sorted
        intersection = [x for x in left if x in right]
        return intersection

    def b_or(self, left, right):
        union = list(set().union(left,right))
        return union

    def b_not(self, unwanted):
        result = list()
        # Locate all documents that are not in the unwanted list
        # This would be highly ineficient in real environment - result
        # list would have billions of entries
        for i in range(0, len(self.documents)):
            if i not in unwanted:
                result.append(i)
        return result

    def b_term(self, word):
        if word not in self.index:
            return []
        res = dict(self.index[word])
        res.pop('count', None)
        return res

    # def search(self, query):
    # 	qTerms = self.parseQuery(query)
    # 	return self.resolveQuery(qTerms)

    # def parseQuery(self, q):
    # 	words = q.split()
    # 	query = list()
    # 	for word in words:
    # 		i = len(query)
    # 		query.append(self.generateTerm(word, i, query))
    # 	return query

    # def generateTerm(self, word, i, query):
    # 	if word == "AND":
    # 		return query.append(BooleanAnd(query, i))
    # 	if word == "OR":
    # 		return query.append(BooleanOr(query, i))
    # 	if word == "NOT":
    # 		return query.append(BooleanNot(query, i))
    # 	return BooleanTerm(query, i, word)

    # def resolveQuery(self, q):
    # 	i = 0
    # 	while(len(q) > 1):
    # 		q = q[i].resolve(self.index)
    # 		i = (i + 1) % len(q)
    # 	res = q[0].resolve(self.index)
    # 	return res[0].getResult()


# I do no longer parse string query so I did not finish this part
# class BooleanTerm:
# 	def __init__(self, query, pos, word = None, result = None):
# 		print("new term")
# 		self.query = query
# 		self.pos = pos
# 		self.word = word
# 		self.result = result
#
# 	def resolve(self, index):
# 		print("resolveTerm")
# 		res = index[self.word]
# 		res.pop('count',None)
# 		return self.rebuild_query(res)
#
# 	def rebuild_query(self, result):
# 		print("rebuild")
# 		new_query = list()
# 		for i in range(0, self.get_previous()):
# 			new_query.append(self.query[i])
# 		new_query.append(BooleanTerm(new_query, self.get_previous() + 1, None, result))
# 		for i in range(self.get_next(), len(self.query)):
# 			new_query.append(self.query[i])
# 		return new_query
#
# 	def get_result(self):
# 		return self.result
#
# 	def get_previous(self):
# 		return self.pos - 1
#
# 	def get_next(self):
# 		return self.pos + 1
#
#
# class BooleanAnd(BooleanTerm):
# 	def resolve(self, index):
# 		left = self.query[self.pos - 1].get_result()
# 		right = self.query[self.pos + 1].get_result()
# 		intersection = [x for x in left if x in right]


# class BooleanOr(BooleanTerm):
#     def get_result(self, index):
#         left = self.query[self.pos - 1].get_result()
#         right = self.query[self.pos + 1].get_result()
#         union = list(set().union(left,right))
#         return union
#
# class BooleanNot(BooleanTerm):
#     def get_result(self, index):
#         right = self.query[self.pos + 1].get_result()
#         result = list()
#         for i in len(self.documents):
#             if i not in right:
#                 result.append(i)
#         return result