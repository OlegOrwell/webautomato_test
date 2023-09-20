FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install pandas && pip install openai && pip install tiktoken

CMD ["python", "convert_table.py", "-s", "table_B"]