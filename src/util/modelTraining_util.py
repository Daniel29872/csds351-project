import pandas as pd
from sklearn.model_selection import train_test_split

def load_and_split_data(file_path, column_to_drop=None):

    data = pd.read_csv(file_path)

    if column_to_drop and column_to_drop in data.columns:
        data = data.drop(columns=[column_to_drop])

    data = data.sample(frac=1).reset_index(drop=True)

    train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

    return train_data, test_data

file_path = 'IMDB Dataset.csv'
train_data, test_data = load_and_split_data(file_path, column_to_drop='index')

import spacy
from spacy.training import Example
import pandas as pd
import random

def train_model(data):
    nlp = spacy.blank("en")
    if "textcat" not in nlp.pipe_names:
        textcat = nlp.add_pipe("textcat", last=True)
        textcat.add_label("POSITIVE")
        textcat.add_label("NEGATIVE")

    nlp.initialize()

    train_data = data.to_dict(orient='records')

    examples = []
    for item in train_data:
        text = item['review']
        label = {'cats': {
            'POSITIVE': item['sentiment'] == 'positive',
            'NEGATIVE': item['sentiment'] == 'negative'
        }}
        doc = nlp.make_doc(text)
        examples.append(Example.from_dict(doc, label))


    random.shuffle(examples)
    print("Starting training...")
    for i in range(10):
        losses = {}
        batches = spacy.util.minibatch(examples, size=2)
        for batch in batches:
            nlp.update(batch, losses=losses)
        print(f"Iteration {i + 1}/{10} complete. Losses: {losses}")

def save_model(nlp, output_dir):
    nlp.to_disk(output_dir)
    print(f"Saved model to {output_dir}")

if __name__ == "__main__":
    trained_model = train_model()

    output_dir = './saved_model'
    save_model(trained_model, output_dir)
