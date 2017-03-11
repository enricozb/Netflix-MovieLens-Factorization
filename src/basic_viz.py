import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

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

def no_spines():
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)

def basic_1():
    ratings = defaultdict(int)
    for line in rating_data():
        r = int(line.split()[-1])
        ratings[r] += 1

    plt.plot(*zip(*list(sorted(ratings.items()))), '-o')

    no_spines()

    plt.grid(True)
    plt.xticks(list(range(1,6)))
    plt.yticks(list(range(5000, 35001, 5000)))
    plt.title('Distribution of all Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Number of Ratings')
    plt.show()

def basic_2():
    movie_ratings = defaultdict(lambda: [0, defaultdict(int)])
    movies = movie_dict()
    for line in rating_data():
        _, movie, rating = tuple(map(int, line.split()))
        movie_ratings[movie][0] += 1
        movie_ratings[movie][1][rating] += 1

    top_ten = list(sorted(movie_ratings.items(), key=lambda x:x[1][0],
                   reverse=True))[:10]
    for movie, ratings in top_ten:
        num = ratings[0]
        ratings = ratings[-1]
        plt.plot(*zip(*list(sorted(ratings.items()))), ',-',
                 label=movies[movie]['title'])
    no_spines()
    plt.grid(True)
    plt.xticks(list(range(1,6)))
    plt.title('Distribution of Top 10 Rated Films')
    plt.xlabel('Rating')
    plt.ylabel('Number of Ratings')
    plt.legend()
    plt.show()

def basic_3():
    movie_ratings = defaultdict(lambda: [0, 0, rating_dict()])
    movies = movie_dict()
    for line in rating_data():
        _, movie, rating = tuple(map(int, line.split()))
        movie_ratings[movie][0] += 1
        movie_ratings[movie][1] += rating
        movie_ratings[movie][2][rating] += 1

    top_ten = list(sorted(filter(lambda x:x[1][0] >= 50, movie_ratings.items()),
                   key=lambda x:(x[1][1]/x[1][0], x[1][0]), reverse=True))[:10]
    for movie, ratings in top_ten:
        num = ratings[0]
        rat = ratings[1]
        ratings = ratings[-1]
        plt.plot(*zip(*list(sorted(ratings.items()))), ',-',
                 label=str(rat/num)[:4] + ' ' + movies[movie]['title'], linewidth=num/50)
    no_spines()
    plt.grid(True)
    plt.xticks(list(range(1,6)))
    plt.title('Distribution of Top 10 Highest Avg. Rating with at least 50 Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Number of Ratings')
    plt.legend()
    plt.show()

def basic_4():
    romance, scifi, thriller = 14, 15, 16
    movie_ratings = defaultdict(list)
    movies = movie_dict()
    for r in rating_data():
        u_id, m_id, rating = tuple(map(int, r.split()))
        if movies[m_id]['vec'][romance] == 0:
            continue
        movie_ratings[m_id].append(rating)

    x = []
    y = []
    c = []
    s = []
    for k, v in movie_ratings.items():
        if len(v) <= 10:
            continue
        x.append(len(v))
        y.append(sum(v)/len(v))
        c.append(np.std(v) ** 2)
        s.append(sum(movies[k]['vec']) * 30)

    plt.scatter(x, y, c=c, s=s)
    no_spines()
    plt.title('Average Rating of Romance Films vs Number of Ratings')
    plt.xlabel('Number of Ratings')
    plt.ylabel('Average Rating')
    plt.show()
