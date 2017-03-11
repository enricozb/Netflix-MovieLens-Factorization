from mat_fac import train_model
from collections import defaultdict
import numpy as np

def rating_data():
    with open('../data/data.txt') as f:
        yield from f

def movie_data():
    with open('../data/movies.txt') as f:
        yield from f

def rating_dict():
    return {v : 0 for v in range(1, 6)}

def movie_dict():
    movies = defaultdict(dict)
    for line in movie_data():
        m_id, movie, *v = line.split('\t')
        movies[int(m_id)]['title'] = movie.replace('"', '')
        movies[int(m_id)]['vec'] = tuple(map(int, v))
    return movies

def train():
    Y = []
    users = set()
    for line in rating_data():
        u_id, m_id, rating = tuple(map(int, line.split()))
        users.add(u_id)
        Y.append((u_id, m_id, rating))
    M = len(users)
    N = len(movie_dict())
    K = 20
    U, V, err = train_model(M, N, K, 0.01, 10e-3, np.array(Y))
    return U, V

# U, V = train()

# m = [1, 2, 6, 22, 174, 179, 181, 185, 507, 1127]

# A, _, B = np.linalg.svd(V)

# V_proj = np.ndarray.tolist((np.matrix(A[:, :2]).T * np.matrix(V)).T)

# movies = movie_dict()
# romance, scifi, thriller = 14, 15, 16
# romance_lst = list(filter(lambda x: movies[x]['vec'][romance], movies.keys()))
# scifi_lst = list(filter(lambda x: movies[x]['vec'][scifi], movies.keys()))
# thriller_lst = list(filter(lambda x: movies[x]['vec'][thriller], movies.keys()))
