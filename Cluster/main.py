#chatbot에 많이 사용. hugging face에서 한국어 문장 슷지 벡터로 변환시켜 긍/부정을 판단해보자.
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import json
import matplotlib.pyplot as plt
import pandas as pd

model = SentenceTransformer('jhgan/ko-sroberta-multitask')
sentences = ["안녕하세요?", "한국어 문장 임베딩을 위한 버트 모델입니다."]
embeddings = model.encode(sentences)

#print(embeddings)

sentences = ['한 남자가 음식을 먹는다.',
          '한 남자가 빵 한 조각을 먹는다.',
          '그 여자가 아이를 돌본다.',
          '한 남자가 말을 탄다.',
          '한 여자가 바이올린을 연주한다.',
          '두 남자가 수레를 숲 속으로 밀었다.',
          '한 남자가 담으로 싸인 땅에서 백마를 타고 있다.',
          '원숭이 한 마리가 드럼을 연주한다.',
          '치타 한 마리가 먹이 뒤에서 달리고 있다.',
          '한 남자가 파스타를 먹는다.',
          '고릴라 의상을 입은 누군가가 드럼을 연주하고 있다.',
          '치타가 들판을 가로 질러 먹이를 쫓는다.']

embeddings = model.encode(sentences)

#kmeans 사용 위해 cluster 개수 지정
num_clusters = 5
clustering_model = KMeans(n_clusters=num_clusters)
#cluster 모델 학습
clustering_model.fit(embeddings)
#label 저장
cluster_assignment = clustering_model.labels_

clustered_sentences = [[] for i in range(num_clusters)]
# for sentence_id, cluster_id in enumerate(cluster_assignment):
#     clustered_sentences[cluster_id].append(sentences[sentence_id])
#
# for i, cluster in enumerate(clustered_sentences):
#     print("Cluster ", i+1)
#     print(cluster)
#     print("")

#본격적인 코드, Crawling.py에서 저장한 .csv 파일 불러와 monster hunter rise 댓글을 clustering한다.
df = pd.read_csv('../Cluster/reviews_ko.csv')

corpus = df['review'].values.tolist()

embeddings = model.encode(corpus)

num_clusters = 3
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(embeddings)
cluster_assignment = clustering_model.labels_

clustered_sentences = [[] for i in range(num_clusters)]
for sentence_id, cluster_id in enumerate(cluster_assignment):
    clustered_sentences[cluster_id].append(corpus[sentence_id])

for i, cluster in enumerate(clustered_sentences):
    print('Cluster %d (%d)' % (i+1, len(cluster)))
    print(cluster)
    print('')
df['voted_up'].value_counts().plot(kind='bar', title='Voted Up')
plt.title("Monster Hunter Rise Like/Hate")

plt.show()