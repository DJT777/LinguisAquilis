import laUSE as aq
import json

p1 = aq.useLite()
sampleQuery = "AFRC 311 Africana Studies Perspectives"
embedding = p1.create_embeddings(sampleQuery)
#print(p1.name)
#print(embedding)
#print("Alhamdullilah")
print("Your results for your search of " + sampleQuery + " returned these results...")
sampleRecommendation = p1.query_embedding(embedding, sampleQuery)



list_of_recommendations = []
print("TESTING CLASS FUNCTIONALITY")
for i, usiCourse in enumerate(p1.class_data):
        dictTitleRecommendations = dict()
        dictTitleRecommendations = {"user_input": None, "user_input_embedding": None, "labels": None, "recommendation_labels": None,
                                        "recommendation0": None, "recommendation1": None, "recommendation2": None,
                                        "recommendation3": None, "recommendation4": None}
        print(usiCourse['course_title'])
        embedding = p1.create_embeddings(usiCourse['course_title'])
        recommendation = p1.query_embedding(embedding, usiCourse['course_title'])
        #print(embedding)
        dictTitleRecommendations['labels'] = recommendation.userQueryLabels
        dictTitleRecommendations['user_input'] = usiCourse['course_title']
        dictTitleRecommendations['user_input_embedding'] = embedding
        dictTitleRecommendations['recommendation_labels'] = recommendation.userQueryLabels[0]
        for k, label in enumerate(recommendation.userQueryLabels[0]):
            dictTitleRecommendations['recommendation'+str(k)] = p1.class_data[label]
            #print(p1.class_data[label])
        list_of_recommendations.append(dictTitleRecommendations)

with open('quickRecSelect.json', 'w') as fp:
    json.dump(list_of_recommendations, fp)

index_course_list = open('quickRecSelect.json')
index_course_list = json.load(index_course_list)
print(index_course_list[420])




