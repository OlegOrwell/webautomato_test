import pandas as pd
import tiktoken


#  Average length of a row in source table, tokens
AVERAGE_TABLE_ROW_LENGTH = 40

#  Average length of model's response by row, tokens
AVERAGE_GENERATED_ROW_LENGTH = 20

#  ~ Length of text in PROMPT, tokens
STATIC_PROMPT = 140

# The context length of 3.5 model I guess somewhere around 4096 tokens.
CONTEXT_WINDOW = 4096

SAFETY_THRESHOLD = 200

# Since we know all this parameters we can define how many rows put in batch.
# Though In real life most likely if maximise prompt size we send to model - will result in increased hallucinating chance
# So the real batch size should be determined experimentally.

batch_max_size = (CONTEXT_WINDOW - SAFETY_THRESHOLD - STATIC_PROMPT) // (AVERAGE_TABLE_ROW_LENGTH + AVERAGE_GENERATED_ROW_LENGTH)

# So batch_max_size is about 62 examples.


def batcher(dataframe):
    dataframe_len = len(dataframe.index.tolist())
    if dataframe_len < batch_max_size:
        return [dataframe]
    else:
        batch_list = []
        for i in range(0, dataframe_len, batch_max_size):
            slice = dataframe.iloc[i: i + batch_max_size]
            batch_list.append(slice)
        return batch_list
