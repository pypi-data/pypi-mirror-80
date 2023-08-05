import random
import time


class KNearestNeighbour:
    def train(self, data):
        print('Training...')
        self.data = data
        print('Done Training.')
    def predict(self, point, k=1):
        distances = {}
        for datapoint in self.data:
            distance = 0
            for x, y in zip(datapoint, point):
                if x - y > 0:
                    distance += x - y
                else:
                    distance += y - x
            distances[tuple(datapoint)[:-1]] = distance
        if k != 1:
            lowests_keys = []
            lowests_v = sorted(set(distances.values()), reverse=True)[:k]
            for x in distances.keys:
                if distances[x] in lowests_v:
                    lowests_keys.append(x)
            for x in lowests:
                for y in self.data:
                    counter = 0
                    for z, a in zip(x,y[:-1]):
                        if z == a:
                            counter += 1
                    if counter == len(x):
                        labels_p.append(y[-1])
            results = {}
            for x in set(labels_p):
                results[x] = labels_p.count(x)
            i = 0
            for x in results.values():
                if i == 0:
                    i += 1
                    max_value = x
                    continue
                if max_value < x:
                    max_value = x
            tops = []
            for x in results.keys():
                if results[x] == max_value:
                    tops.append(x)
            return random.choice(tops)
        i = 0
        for x in distances.values():
            if i == 0:
                lowest = x
                i += 1
                continue
            if lowest > x:
                lowest = x
        lowests = []
        labels_p = []
        for x, y in zip(distances.keys(), distances.values()):
            if y == lowest:
                lowests.append(x)
        for x in lowests:
            for y in self.data:
                counter = 0
                for z, a in zip(x,y[:-1]):
                    if z == a:
                        counter += 1
                if counter == len(x):
                    labels_p.append(y[-1])
        results = {}
        for x in set(labels_p):
            results[x] = labels_p.count(x) 
        i = 0
        for x in results.values():
            if i == 0:
                i +=1
                max_value = x
                continue
            if max_value < x:
                max_value = x
        equals = []
        for x in results.keys():
            if results[x] == max_value:
                equals.append(x)
        return random.choice(equals)


    def test(self, data):
        data1 = []
        for x in data:
            data1.append(x[:-1])
        correct = 0
        wrong = 0
        for x, y in zip(data1, data):
            if self.predict(x) == y[-1]:
                correct += 1
            else:
                wrong += 1
        print(f'Correct predictions: {correct}')
        print(f'Incorrect predictions: {wrong}')
        print(f'Accuracy: {(correct/(wrong + correct)) * 100}%')



class Regression:
    def train(self, data):
        if len(data) == 1:
            raise Exception('Cannot have only one data point! Add more data.')
        startime = time.time()
        print('Training...')
        x_total = 0
        x_amount = 0
        y_total = 0
        y_amount = 0
        for x in data:
            x_total += x[0]
            x_amount += 1
            y_total += x[1]
            y_amount += 1
        x_mean = x_total / x_amount
        y_mean = y_total / y_amount
        x_x = [] 
        y_y = []
        x_x2 = []
        x_xy_y = []
        for x in data:
            x_x.append(x[0] - x_mean)
            y_y.append(x[1] - y_mean)
        for x in x_x:
            x_x2.append(x * x)
        for x, y in zip(x_x, y_y):
            x_xy_y.append(x * y)
        sumx_x2 = 0
        sumx_xy_y = 0
        for x in x_x2:
            sumx_x2 += x
        for x in x_xy_y:
            sumx_xy_y += x
        self.m = sumx_xy_y / sumx_x2
        self.c = y_mean - (self.m * x_mean)
        print('Done Training.')
        print(f'Time took to train: {time.time() - startime} seconds.')
    def predict(self, x):
        return self.m * x + self.c


class KMeansClustering:
    def train(self, k, datapoints):
        st = time.time()
        print('Started Training...')
        centers = []
        for y in range(k):
            center = []
            for x in range(len(datapoints[0])):
                center.append(random.random() * 100)
            centers.append(center)
        while True:
            mappings = {}
            for x in centers:
                mappings[tuple(x)] = []
            for x in datapoints:
                center_distances = {}
                for y in centers:
                    center_distances[tuple(y)] = 0
                    for a, b in zip(x, y):
                        center_distances[tuple(y)] += a - b if a - b > 0 else b - a
                mappings[min(center_distances, key=center_distances.get)] += [x]
            self.mappings = mappings
            new_centers = []
            for x in mappings:
                sums = {}
                for z in range(len(centers[0])):
                    sums[z] = 0
                for h in mappings[x]:
                    for y, a in zip(h, range(len(centers[0]))):
                        sums[a] += y / len(datapoints)
                new_centers.append(sums.values())
            new_centers2 = []
            for x in new_centers:
                new_centers2.append(list(x))
            if list(new_centers2) == list(centers):
                self.centers = new_centers2
                print('Done Training.')
                print(f'Time took to train: {time.time() - st}')
                return None
            else:
                centers = new_centers2
