class PageRank:
    def __init__(self, documents, random_probability, rank_threshold):
        self.documents = documents
        self.url_map = dict()
        self.create_url_map()
        self.alpha = random_probability
        self.threshold = rank_threshold

    def create_url_map(self):
        for i in self.documents:
            self.url_map[i.url] = i.id

    def rank_documents(self):
        vector = self.get_rank_vector()
        docs = list(self.documents)
        for doc in docs:
            doc.raw_text = vector[doc.id]
        return docs

    def get_rank_vector(self):
        random_matrix = self.get_random_walk_matrix()
        matrix = self.add_links(random_matrix)
        vector = self.get_initial_vector()
        round_count = 0
        while True:
            round_count += 1
            new_vector = PageRank.multiply(vector, matrix)
            diff = PageRank.max_vector_diff(vector, new_vector)
            if diff < self.threshold:
                return new_vector
            vector = new_vector

    def add_links(self, matrix):
        for doc in self.documents:
            links = self.get_valid_links(doc.links)
            cnt = len(links)
            for link in links:
                if link in self.url_map:
                    tid = self.url_map[link]
                    matrix[doc.id][tid] = matrix[doc.id][tid] + ((1 - self.alpha) * (1 / cnt))
        return matrix

    def get_random_walk_matrix(self):
        matrix = []
        for i in range(0, len(self.documents)):
            matrix.append([])
            for j in range(0, len(self.documents)):
                matrix[i].append(self.alpha * (1 / len(self.documents)))
        return matrix

    def get_valid_links(self, links):
        result = list()
        for link in links:
            if link in self.url_map:
                result.append(link)
        return result

    def get_initial_vector(self):
        vector = []
        for _ in self.documents:
            vector.append(0)
        vector[0] = 1
        return vector

    @staticmethod
    def multiply(vector, matrix):
        result = []
        for qi in range(0, len(vector)):
            qi_sum = 0
            for col in range(0, len(vector)):
                qi_sum = qi_sum + (vector[col] * matrix[col][qi])
            result.append(qi_sum)
        return result

    @staticmethod
    def max_vector_diff(v1, v2):
        max_diff = 0
        for i in range(0, len(v1)):
            diff = abs(v1[i] - v2[i])
            if diff > max_diff:
                max_diff = diff
        return max_diff
