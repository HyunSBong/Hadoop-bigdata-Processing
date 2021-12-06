from mrjob.job import MRJob
from mrjob.step import MRStep

class checkLocation(MRJob):
    def steps(self):
        return [
            # 감성지수를 지자체별로 모두 더하고 통계치를 곱하는 단계
            MRStep(
                mapper=self.mapper,
                reducer=self.reduce_rating),
            # 통계치를 기준으로 내림차순 정렬을 하는 단계
            MRStep(
                reducer=self.reduce_sort)
        ]

    # 감성지수 데이터.csv, 전국지자체별_통계데이터.csv 처리
    # input은 감성지수 데이터.csv, 전국지자체별_통계데이터.csv 순이다.
    def mapper(self, _, line):
        data = line.split(',')
        if data[1] != '지자체명':
            # 지자체명과 감성지수,통계치
            yield data[1], float(data[2])

    def reduce_rating(self, govName, ratings):
        # generator object를 list로 형변환
        l = list(ratings) 
        # 통계치는 따로 곱할 값이므로 제외
        num = l[-1]
        del l[-1]
        # 감성지수의 총합
        sumRating = sum(l)

        # 감정지수에 통계치 곱하기
        combined = sumRating * num
        yield None, (combined, govName)

    def reduce_sort(self, _, datas):
        # rating을 기준으로하여 오름차순 정렬을 한다. 
        for rating, govName in sorted(datas):
            yield govName , rating

if __name__ == "__main__":
    checkLocation.run()
