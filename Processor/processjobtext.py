import tagme

def getTageMeAnnotations(sentence):
    sentence_annotation = tagme.annotate(sentence)
    annot_index = [x.entity_id for x in sentence_annotation.annotations]
    return annot_index


def getTageMeAnnotationsOfList(listOfSentences):
    sent_annot = []
    for i in range(len(listOfSentences)):
        sent_annot[i] = getTageMeAnnotations(listOfSentences[i])
    return sent_annot


def generate_tag_cloud(freq, image_filename):
	wc = WordCloud(background_color="white").generate_from_frequencies(freq)
	image = wc.to_image()
	image.save(image_filename)